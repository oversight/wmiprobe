from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = ""
QUERY = """
    SELECT
    uname, archName, coreCount, count, deviceInfo, gpuCoreClockCurrent,
    handle, id, memoryBusWidth, memoryClockCurrent, memorySizeAvailable,
    memorySizePhysical, memorySizeVirtual, memoryType, nvapiId, ordinal,
    pcieDownstreamWidth, pcieGpu, percentGpuMemoryUsage, percentGpuUsage,
    power, powerSampleCount, powerSamplingPeriod, productName,
    productType, ver, verVBIOS, videoCodec
    FROM Gpu
"""


def on_item(itm: dict) -> Tuple[str, dict]:
    # TODO
    return None, itm


async def check_nvidia_gpu(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
