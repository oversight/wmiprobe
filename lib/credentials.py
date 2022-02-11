import base64
import configparser
import logging
import os
from Crypto.Cipher import AES
from hashlib import md5
from .config import CONFIG_FOLDER


CREDENTIALS = {}


def get_key(agentcore_uuid):
    flipped = 'tt{0}'.format(agentcore_uuid[::-1]).encode('utf-8')
    return md5(flipped).hexdigest().encode('utf-8')


def unpad(s):
    return s[0:-bytearray(s)[-1]]


def decrypt(key, data):
    enc = base64.b64decode(data)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec = cipher.decrypt(enc[AES.block_size:])
    return unpad(dec).decode('utf-8')


def on_credentials_file(fn, agentcore_uuid):
    config = configparser.ConfigParser()
    config.read(fn)

    try:
        section = config['credentials']
    except configparser.NoSectionError:
        raise Exception(f'Missing section [credentials] in {fn}')

    try:
        username = section.get('username')
    except configparser.NoOptionError:
        raise Exception(f'Missing username in {fn}')

    try:
        password_encryped = section.get('password')
    except configparser.NoOptionError:
        raise Exception(f'Missing password in {fn}')

    try:
        password = decrypt(agentcore_uuid, password_encryped)
    except Exception:
        raise Exception(f'Failed to decrypt password in {fn}')

    return {
        'username': username,
        'password': password,
    }


def load_credentials(agentcore_uuid):
    decrypt_key = get_key(agentcore_uuid)

    for fn in os.listdir(CONFIG_FOLDER):
        if fn.endswith('.ini'):
            try:
                CREDENTIALS[fn[:-4]] = on_credentials_file(
                    os.path.join(CONFIG_FOLDER, fn), decrypt_key)
            except Exception as e:
                logging.error(e)
