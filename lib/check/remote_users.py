from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..wmiquery import wmiquery
from ..utils import get_state


TYPE_NAME = "remote_users"
QUERY = Query("""
    SELECT
    Caption
    FROM Win32_Process
    WHERE Caption=\'winlogon.exe\'
""")


async def check_remote_users(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    # TODO proper item and metric names
    return {
        TYPE_NAME: {
            'system': {
                'userCount': len(rows) - 1,
            }
        }
    }
