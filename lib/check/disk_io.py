from libprobe.asset import Asset
from ..wmiquery import wmiquery
from ..utils import get_state


TYPE_NAME = "disk"
QUERY = """
    SELECT
    Name, DiskReadsPersec, DiskWritesPersec
    FROM Win32_PerfFormattedData_PerfDisk_LogicalDisk
    WHERE name != "_Total"
"""


async def check_disk_io(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(QUERY, asset, asset_config, check_config)
    state = get_state(TYPE_NAME, rows)
    return state
