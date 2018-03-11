import sys
import argparse

# Ployalphabetic Cipher
# Choose a special word  as the key to encrypt/decrypt the plain text/cipher text
# Just to encrypt a text which contains only letters and some special characters:'[', '\', ']', '^', '_', '`'


def encrypt(plain_text, key):
    key_len = len(key)
    plain_len = len(plain_text)
    cipher_list = list()
    cipher_text = ''
    new_key = ''
    if key_len >= plain_len:
        for i in range(plain_len):
            cipher_numeric = (ord(plain_text[i]) + ord(key[i]) - 64 * 2)
            # Gap between 'A' to 'z': ASCII 65-122
            if cipher_numeric > 58:
                cipher_numeric %= 58
            cipher_list.append(cipher_numeric)
    else:

        round = plain_len // key_len
        remain = plain_len % key_len
        for r in range(round):
            new_key += key
        for m in range(remain):
            new_key += key[m]
        for i in range(plain_len):
            cipher_numeric = (ord(plain_text[i]) + ord(new_key[i]) - 64 * 2)
            if cipher_numeric > 58:
                cipher_numeric %= 58
            cipher_list.append(cipher_numeric)
    for letter in cipher_list:
        cipher_text += chr(letter + 64)
    # return cipher_text
    print(cipher_text)


def decrypt(cipher_text, key):
    cipher_len = len(cipher_text)
    key_len = len(key)
    new_key = ''
    plain_text = ''
    plain_list = list()
    if cipher_len <= key_len:
        for i in range(cipher_len):
            plain_numeric = (ord(cipher_text[i]) - ord(key[i]))
            if plain_numeric < 0:
                plain_numeric %= 58
            plain_list.append(plain_numeric)
    else:
        round = cipher_len // key_len
        remain = cipher_len % key_len
        for r in range(round):
            new_key += key
        for m in range(remain):
            new_key += key[m]
        for i in range(cipher_len):
            plain_numeric = (ord(cipher_text[i]) - ord(new_key[i]))
            if plain_numeric < 0:
                plain_numeric %= 58
            plain_list.append(plain_numeric)
    for number in plain_list:
        plain_text += chr(number + 64)
    # return plain_text
    print(plain_text)


def parse_argument():
    parser = argparse.ArgumentParser(description='Enter Plain/Cipher to Encrypt/Decrypt. Only apply to polyalphabetic shift cipher, ASCII number between 65 and 122')
    arg_gourp = parser.add_mutually_exclusive_group()
    arg_gourp.add_argument('--encrypt', '-e', action='store_true', help='Choose Encryption Mode')
    arg_gourp.add_argument('--decrypt', '-d', action='store_true', help='Choose Decryption Mode')

    parser.add_argument('--key', '-k', help='Pick a encryption key')
    parser.add_argument('--text', '-t', help='Enter the text you want to encrypt/decrypt')

    args = parser.parse_args(sys.argv[1:])
    if args.encrypt == True:
        encrypt(args.text, args.key)
    elif args.decrypt == True:
        decrypt(args.text, args.key)
    else:
        print('Arg param wrong, please retry. format: [-e|-d -k "your_key" -t "your_text"]')


if __name__ == '__main__':
    parse_argument()
