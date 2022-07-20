from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state, add_total_item
from ..wmiquery import wmiquery


TYPE_NAME = "pageFile"
QUERY = Query("""
    SELECT
    Name, AllocatedBaseSize, CurrentUsage
    FROM Win32_PageFileUsage
""")


def on_item(itm: dict) -> dict:
    total = itm['AllocatedBaseSize'] * 1024 * 1024
    used = itm['CurrentUsage'] * 1024 * 1024
    free = total - used
    percentage = 100 * used / total if total else 0.

    return {
        'name': itm.pop('Name'),
        'BytesTotal': total,
        'BytesFree': free,
        'BytesUsed': used,
        'PercentUsed': percentage
    }


async def check_page_file(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    total = {
        'AllocatedBaseSize': sum(itm['AllocatedBaseSize'] for itm in rows),
        'CurrentUsage': sum(itm['CurrentUsage'] for itm in rows),
    }
    add_total_item(state, total, TYPE_NAME)
    return state
