from configparser import ConfigParser, NoSectionError, NoOptionError


def read_credentials(config: ConfigParser, key, decrypt):
    try:
        section = config['credentials']
    except NoSectionError:
        raise Exception(f'Missing section [credentials]')

    try:
        username = section.get('username')
    except NoOptionError:
        raise Exception(f'Missing username')

    try:
        password_encryped = section.get('password')
    except NoOptionError:
        raise Exception(f'Missing password')

    try:
        password = decrypt(key, password_encryped)
    except Exception:
        raise Exception(f'Failed to decrypt password')

    return {
        'username': username,
        'password': password,
    }
