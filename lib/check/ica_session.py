from libprobe.asset import Asset
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "ica_session"
QUERY = """
    SELECT
    Name, LatencySessionAverage
    FROM Win32_PerfFormattedData_CitrixICA_ICASession
"""


async def check_ica_session(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows)
    return state
