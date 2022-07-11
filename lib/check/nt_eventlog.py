from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..wmiquery import wmiquery
from ..utils import get_state


TYPE_NAME = "eventlog"
QUERY = Query("""
    SELECT
    FileName, Name, NumberOfRecords, Status
    FROM Win32_NTEventlogFile
""")


async def check_nt_eventlog(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows)
    return state
