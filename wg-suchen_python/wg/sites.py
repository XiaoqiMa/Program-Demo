from bs4 import BeautifulSoup
import requests
from six import iteritems
import re
from fake_useragent import UserAgent
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

ua = UserAgent()
base_url = "http://www.wg-gesucht.de/"
# base_filter = {
#     'category': '1',
#     'rent_type': '0',
#     'sMin': '15',
#     'rMax': '350'
# }


def get_all_sites():
    sites = set()
    # filterd_site = "http://www.wg-gesucht.de/1-zimmer-wohnungen-in-Aachen.1.1.1.0.html?offer_filter=1&noDeact=1&city_id=1&category=1&rent_type=0&sMin={min}&rMax={max}".format(min=base_filter['sMin'], max=base_filter['rMax'])
    # sites = get_sites(filterd_site, sites)
    for page in range(3):
        site_url = "http://www.wg-gesucht.de/1-zimmer-wohnungen-in-Aachen.1.1.1.{pageNum}.html".format(pageNum=str(page))
        sites = get_sites(site_url, sites)
    return sites


def get_sites(site_url, sites):
    headers = {'User-Agent': ua.random}
    response = requests.get(site_url, headers=headers)
    response.raise_for_status()
    print(response.status_code)
    bsObject = BeautifulSoup(response.content, 'html.parser')
    for box in bsObject.findAll('div', {'class': 'col-xs-10'}):
        for a in box.findAll('a'):
            site = "{base}{href}".format(base=base_url, href=a.attrs['href'])
            sites.add(site)
    return sites


def get_results(sites):
    result_list = list()
    for page_url in sites:
        result_list.append(get_contents(page_url))
    return result_list


def get_contents(page_url):
    values_dic = {}
    response = requests.get(page_url)
    response.raise_for_status()
    values_dic['url'] = page_url
    bsObject = BeautifulSoup(response.content, 'html.parser')
    for box in bsObject.findAll('div', {'class': 'row bg-grey-box'}):
        round = 0
        for a in box.findAll('h2', {'class': 'headline headline-key-facts'}):
            try:
                if(round == 0):
                    values_dic['size'] = a.contents[0].strip()
                    round += 1
                else:
                    values_dic['price'] = a.contents[0].strip()
            except Exception as e:
                pass

    for box in bsObject.findAll('div', {'class': 'col-sm-4 mb10'}):
        for a in box.findAll('a', {'href': '#'}):
            try:
                values_dic['address'] = '%s %s' % (a.contents[0].strip(), a.contents[2].strip())
            except Exception as e:
                pass

    for box in bsObject.findAll('div', {'class': 'col-sm-3'}):
        for a in box.findAll('p'):
            for date in a.find('b'):
                values_dic['start_date'] = date
    return values_dic


def filter_result(minSize, maxPrice, sites_list):
    filter_list = list()
    for sites in sites_list:
        if len(sites) == 5:
            if int(re.findall(r'\d+', sites['size'])[0]) >= minSize and int(re.findall(r'\d+', sites['price'])[0]) <= maxPrice:
                filter_list.append(sites)
    return filter_list


def save_database(apartment_list):
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
    dbname = 'WG_Suchen'
    try:
        cursor = cnx.cursor()
        sql_cdb = 'Create Database {name}'.format(name=dbname)
        # cursor.execute(sql_cdb)
    except mysql.connector.Error as err:
        print('Failed to create database: {}'.format(err))
        exit(1)

    try:
        cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database=dbname)
        cursor = cnx.cursor()
        sql_ctb = '''Create Table WG(
                    id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    url varchar(200) NOT NULL UNIQUE,
                    size varchar(10) NOT NULL,
                    price varchar(10) NOT NULL,
                    address varchar(50) NOT NULL,
                    start_date date NOT NULL )
                '''
        cursor.execute(sql_ctb)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exist")
        else:
            print(err.msg)

    try:
        for apartment in apartment_list:
            url = apartment['url']
            size = apartment['size']
            price = apartment['price']
            address = apartment['address']
            start_date = apartment['start_date']
            date_object = datetime.strptime(start_date, '%d.%m.%Y')
            new_date = date_object.strftime('%Y-%m-%d')
            sql_insert = '''INSERT INTO WG (url, size, price, address, start_date)
                            VALUES (%s, %s, %s, %s, %s)
                        '''
            args = (url, size, price, address, new_date)
            cursor.execute(sql_insert, args)
            cnx.commit()
        cnx.close()
    except mysql.connector.Error as err:
        print(err.msg)


sites = get_all_sites()
sites_list = get_results(sites)
# print(sites_list)
# minSize = input('What is the minimum size do you expect for the apartment?\n')
# maxPrice = input('What is the maximum price do you expect for the apartment?\n')
minSize = 15
maxPrice = 350
filter_apartment_list = filter_result(minSize, maxPrice, sites_list)
print("Filter_apartment_list\n", filter_apartment_list)
save_database(filter_apartment_list)
