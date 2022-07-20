from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "route"
QUERY = Query("""
    SELECT
    Name, Age, Caption, Description, Destination, Information, InterfaceIndex,
    Mask, Metric1, Metric2, Metric3, Metric4, Metric5, NextHop, Protocol,
    Status, InstallDate, Type
    FROM Win32_IP4RouteTable
""")


def on_item(itm: dict) -> dict:
    itm['name'] = '{Destination} [{InterfaceIndex}]'.format_map(itm)
    return itm


async def check_ip4_route_table(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
