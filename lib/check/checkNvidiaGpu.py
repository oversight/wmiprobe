from .base import Base

# https://www.nvidia.com/content/quadro_fx_product_literature/wp-06953-001-v02.pdf


MB_FACTOR = 1000 * 1000


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


WATT_FACTOR = 1000. * 1000. * 100.


class CheckNvidiaGpu(Base):

    qry = '''
    SELECT
    uname, archName, coreCount, count, deviceInfo, gpuCoreClockCurrent,
    handle, id, memoryBusWidth, memoryClockCurrent, memorySizeAvailable,
    memorySizePhysical, memorySizeVirtual, memoryType, nvapiId, ordinal,
    pcieDownstreamWidth, pcieGpu, percentGpuMemoryUsage, percentGpuUsage,
    power, powerSampleCount, powerSamplingPeriod, productName,
    productType, ver, verVBIOS, videoCodec
    FROM Gpu
    '''

    type_name = 'gpu'
    namespace = 'root/cimv2/nv'

    @staticmethod
    def on_item(itm):
        gpu_freq = itm['gpuCoreClockCurrent']
        gpu_freq = gpu_freq if gpu_freq != -1 else None

        mem_freq = itm['memoryClockCurrent']
        mem_freq = mem_freq if mem_freq != -1 else None

        return {
            'name': itm['uname'],
            'archName': itm['archName'],
            'coreCount': itm['coreCount'],
            'count': itm['count'],
            'deviceInfo': itm['deviceInfo'],
            'gpuCoreClockCurrent': gpu_freq,
            'handle': itm['handle'],
            'id': itm['id'],
            'memoryBusWidth': itm['memoryBusWidth'],
            'memoryClockCurrent': mem_freq,
            'memorySizeAvailable': itm['memorySizeAvailable'] * MB_FACTOR,
            'memorySizePhysical': itm['memorySizePhysical'] * MB_FACTOR,
            'memorySizeVirtual': itm['memorySizeVirtual'] * MB_FACTOR,
            'memoryType': MEM_TYPE_LU.get(itm['memoryType'], '???'),
            'nvapiId': itm['nvapiId'],
            'ordinal': itm['ordinal'],
            'pcieDownstreamWidth': itm['pcieDownstreamWidth'],
            'pcieGpu': itm['pcieGpu'],
            'percentGpuMemoryUsage': itm['percentGpuMemoryUsage'],
            'percentGpuUsage': itm['percentGpuUsage'],
            'power': itm['power'] / WATT_FACTOR,
            'powerSampleCount': itm['powerSampleCount'],
            'powerSamplingPeriod': itm['powerSamplingPeriod'] / 1000.,
            'productName': itm['productName'],
            'productType': PROD_TYPE_LU.get(itm['productType'], '???'),
            'uname': itm['uname'],
            'ver': itm['ver'],
            'verVBIOS': itm['verVBIOS'],
            'videoCodec': itm['videoCodec'],
        }
