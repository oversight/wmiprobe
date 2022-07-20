from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state, parse_wmi_date, parse_wmi_date_1600
from ..wmiquery import wmiquery


TYPE_NAME = "updates"
QUERY = Query("""
    SELECT
    Description, Name, CSName, FixComments,
    HotFixID, InstalledBy, InstalledOn, ServicePackInEffect
    FROM Win32_QuickFixEngineering
""")


def on_item(itm: dict) -> dict:
    # InstalledOn can be multiple datestring formats or windows timestamp
    # i.e. (nanoseconds from 1600)
    installed_on_str = itm['InstalledOn']
    installed_on = parse_wmi_date(installed_on_str, '%m/%d/%Y') or \
        parse_wmi_date(installed_on_str, '%m-%d-%Y') or \
        parse_wmi_date(installed_on_str) or \
        parse_wmi_date_1600(installed_on_str)

    itm['name'] = itm.pop('HotFixID')
    return {
        **itm,
        'InstalledOn': installed_on,
    }


async def check_updates(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)

    state['last_update'] = last = None
    for itm in state[TYPE_NAME].values():
        if itm['InstalledOn'] and (
            not last or itm['InstalledOn'] > last['InstalledOn']
        ):
            last = itm

    return state
