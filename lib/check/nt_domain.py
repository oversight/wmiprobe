from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "domain"
QUERY = Query("""
    SELECT
    DomainName, DnsForestName, DomainControllerName
    FROM Win32_NTDomain
    WHERE DomainName IS NOT NULL
""")


def on_item(itm: dict) -> dict:
    itm['DomainControllerName'] = itm['DomainControllerName'].strip('\\\\')
    itm['name'] = itm.pop('DomainName')
    return itm


async def check_nt_domain(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
