from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..wmiquery import wmiquery
from ..utils import get_state


TYPE_NAME = "uptime"
QUERY = Query("""
    SELECT
    SystemUpTime
    FROM Win32_PerfFormattedData_PerfOS_System
""")


def on_item(itm: dict) -> Tuple[str, dict]:
    # TODO proper item and metric names
    return 'system', {
        'uptime': itm['SystemUpTime']
    }


async def check_uptime(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
