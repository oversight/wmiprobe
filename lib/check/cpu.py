from aiowmi.query import Query
from libprobe.asset import Asset
from ..utils import get_state
from ..wmiquery import wmiquery

TYPE_NAME = "cpu"
QUERY = Query("""
    SELECT
    Name, PercentProcessorTime
    FROM Win32_PerfFormattedData_PerfOS_Processor
""")


async def check_cpu(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows)  # Includes type cpuTotal
    return state
