from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "gpu"
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
NAMESPACE = "root/cimv2/nv"

MEM_TYPE_LU = {
    '0': 'unknown',
    '1': 'SDRAM',
    '2': 'DDR1',
    '3': 'DDR2',
    '4': 'GDDR2',
    '5': 'GDDR3',
    '6': 'GDDR4',
    '7': 'DDR3',
    '8': 'GDDR5',
    '9': 'LPDDR2',
    '10': 'GDDR5X',
    '11': 'HBM1',
    '12': 'HBM2'
}
PROD_TYPE_LU = {
    '0': 'unknown',
    '1': 'GeForce',
    '2': 'Quadro',
    '3': 'NVS',
    '4': 'Tesla'
}


def on_item(itm: dict) -> Tuple[str, dict]:
    gpu_freq = itm['gpuCoreClockCurrent']
    gpu_freq = gpu_freq if gpu_freq != -1 else None

    mem_freq = itm['memoryClockCurrent']
    mem_freq = mem_freq if mem_freq != -1 else None

    return itm.pop('uname'), {
        **itm,
        'gpuCoreClockCurrent': gpu_freq,
        'memoryClockCurrent': mem_freq,
        'memorySizeAvailable': itm['memorySizeAvailable'] * 1000_000,
        'memorySizePhysical': itm['memorySizePhysical'] * 1000_000,
        'memorySizeVirtual': itm['memorySizeVirtual'] * 1000_000,
        'memoryType': MEM_TYPE_LU.get(itm['memoryType']),
        'power': itm['power'] / 1000_000,
        'powerSamplingPeriod': itm['powerSamplingPeriod'] / 1000,
        'productName': itm['productName'],
        'productType': PROD_TYPE_LU.get(itm['productType']),
    }


async def check_nvidia_gpu(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY, NAMESPACE)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
