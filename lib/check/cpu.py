from libprobe.asset import Asset
from ..wmiquery import wmiquery
from ..utils import get_state


TYPE_NAME = "cpu"
QUERY = """
    SELECT
    Name, PercentProcessorTime
    FROM Win32_PerfFormattedData_PerfOS_Processor
"""


async def check_cpu(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(QUERY, asset, asset_config, check_config)
    state = get_state(TYPE_NAME, rows)  # Includes type cpuTotal
    return state
