import datetime
import logging


def parse_wmi_date(val, fmt='%Y%m%d'):
    if not val:
        return None
    try:
        val = int(datetime.datetime.strptime(val, fmt).timestamp())
        if val <= 0:
            return None
        return val
    except Exception:
        logging.exception('DateStr: {}\n'.format(val))
        return None


def parse_wmi_date_1600(val):
    if not val:
        return None
    seconds1600 = 11644473600  # seconds from 1600
    try:
        val = int(val, 16) // 10000000 - seconds1600
        if val <= 0:
            return None
        return val
    except Exception:
        return None


def format_list(val):
    joined = ' ,'.join(map(str, val))
    return f'[{joined}]'
