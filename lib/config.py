from configparser import ConfigParser, NoSectionError, NoOptionError


def read_asset_config(config: ConfigParser, key, decrypt):
    try:
        section = config['credentials']
    except NoSectionError:
        raise Exception(f'Missing section [credentials]')

    try:
        username = section.get('username')
    except NoOptionError:
        raise Exception(f'Missing username')

    if '\\' in username:
        # Replace double back-slash with single if required
        username = username.replace('\\\\', '\\')
        domain, username = username.split('\\')
    elif '@' in username:
        username, domain = username.split('@')
    else:
        domain = ''

    try:
        password_encryped = section.get('password')
    except NoOptionError:
        raise Exception(f'Missing password')

    try:
        password = decrypt(key, password_encryped)
    except Exception:
        raise Exception(f'Failed to decrypt password')

    return {
        'credentials': {
            'username': username,
            'password': password,
            'domain': domain,
        }
    }
