# Ployalphabetic Cipher

#'[', '\', ']', '^', '_', '`'


def encrypt(plain_text, key):
    key_len = len(key)
    plain_len = len(plain_text)
    cipher_list = list()
    cipher_text = ''
    new_key = ''
    if key_len >= plain_len:
        for i in range(plain_len):
            cipher_numeric = (ord(plain_text[i]) + ord(key[i]) - 96 * 2)
            if cipher_numeric > 26:
                cipher_numeric %= 26
            cipher_list.append(cipher_numeric)
    else:
        round = plain_len // key_len
        remain = plain_len % key_len
        for r in range(round):
            new_key += key
        for m in range(remain):
            new_key += key[m]
        for i in range(plain_len):
            cipher_numeric = (ord(plain_text[i]) + ord(new_key[i]) - 96 * 2)
            if cipher_numeric > 26:
                cipher_numeric %= 26
            cipher_list.append(cipher_numeric)
    for number in cipher_list:
        cipher_text += chr(number + 96)

    return cipher_text


def decrypt(cipher_text, key):
    cipher_len = len(cipher_text)
    key_len = len(key)
    cipher = ''
    new_key = ''
    plain_text = ''
    plain_list = list()
    if cipher_len <= key_len:
        for i in range(cipher_len):
            plain_numeric = (ord(cipher_text[i]) - ord(key[i]))
            if plain_numeric < 26:
                plain_numeric %= 26
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
            if plain_numeric < 26:
                plain_numeric %= 26
            plain_list.append(plain_numeric)
    for number in plain_list:
        plain_text += chr(number + 96)
    return plain_text
