import logging
from aiowmi.query import Query
from collections import defaultdict
from libprobe.asset import Asset
from ..wmiquery import wmiquery


TYPE_NAME = "users"
QUERY = Query("""
    SELECT
    Antecedent, Dependent
    FROM Win32_LoggedOnUser
""")


def get_itemname(itm):
    try:
        splitted = itm['Antecedent'].split('"')
        return splitted[1] + '\\' + splitted[3]
    except Exception as e:
        logging.error(e)
        return None


def get_logonid(itm):
    try:
        splitted = itm['Dependent'].split('"')
        return splitted[1]
    except Exception as e:
        logging.error(e)
        return None


async def check_logged_on_users(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)

    name_login = defaultdict(list)
    for itm in rows:
        name = get_itemname(itm)
        logon_id = get_logonid(itm)
        name_login[name].append(logon_id)

    return {
        TYPE_NAME: {
            name: {
                'logonIds': logon_ids,
                'sessionCount': len(logon_ids)
            }
            for name, logon_ids in name_login.items()
        },
        # TODO proper type, itm and metric name
        f'{TYPE_NAME}Total': {
            '_Total': {
                'count': len(rows)
            }
        }
    }
