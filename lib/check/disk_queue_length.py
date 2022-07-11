from aiowmi.query import Query
from libprobe.asset import Asset
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "disk"
QUERY = Query("""
    SELECT
    Name, AvgDiskQueueLength, AvgDiskReadQueueLength, AvgDiskWriteQueueLength,
    CurrentDiskQueueLength, DiskReadBytesPersec, DiskReadsPersec,
    DiskWriteBytesPersec, DiskWritesPersec, PercentDiskReadTime,
    PercentDiskWriteTime
    FROM Win32_PerfFormattedData_PerfDisk_PhysicalDisk
""")


async def check_disk_queue_length(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows)
    return state
