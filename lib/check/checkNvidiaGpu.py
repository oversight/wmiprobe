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

    qry = (
        'SELECT '
        'uname, archName, coreCount, count, deviceInfo, gpuCoreClockCurrent, '
        'handle, id, memoryBusWidth, memoryClockCurrent, memorySizeAvailable, '
        'memorySizePhysical, memorySizeVirtual, memoryType, nvapiId, ordinal, '
        'pcieDownstreamWidth, pcieGpu, percentGpuMemoryUsage, percentGpuUsage, '
        'power, powerSampleCount, powerSamplingPeriod, productName, '
        'productType, ver, verVBIOS, videoCodec '
        'FROM Gpu'
    )

    type_name = 'gpu'
    namespace = 'root/cimv2/nv'

    @staticmethod
    def on_item(itm):
        gpu_freq = itm['gpuCoreClockCurrent']
        gpu_freq = gpu_freq if gpu_freq != -1 else None

        mem_freq = itm['memoryClockCurrent']
        mem_freq = mem_freq if mem_freq != -1 else None

        return {
            'name': itm['uname'],  # {str} 'Quadro K620'
            'archName': itm['archName'],  # {str} 'Maxwell'
            'coreCount': itm['coreCount'],  # {str} '384'
            'count': itm['count'],  # {str} '1'
            'deviceInfo': itm['deviceInfo'],  # {str} ''
            'gpuCoreClockCurrent': gpu_freq,  # {str} '-1'
            'handle': itm['handle'],  # {str} '33024'
            'id': itm['id'],  # {str} '1'
            'memoryBusWidth': itm['memoryBusWidth'],  # {str} '128'
            'memoryClockCurrent': mem_freq,  # {str} '900'
            'memorySizeAvailable': itm['memorySizeAvailable'] * MB_FACTOR,  # {str} '108'
            'memorySizePhysical': itm['memorySizePhysical'] * MB_FACTOR,  # {str} '2048'
            'memorySizeVirtual': itm['memorySizeVirtual'] * MB_FACTOR,  # {str} '67230'
            'memoryType': MEM_TYPE_LU.get(itm['memoryType'], '???'),  # {str} '7'
            'nvapiId': itm['nvapiId'],  # {str} '33024'
            'ordinal': itm['ordinal'],  # {str} '1'
            'pcieDownstreamWidth': itm['pcieDownstreamWidth'],  # {str} '16'
            'pcieGpu': itm['pcieGpu'],  # {str} 'Unsupported'
            'percentGpuMemoryUsage': itm['percentGpuMemoryUsage'],  # {str} '94'
            'percentGpuUsage': itm['percentGpuUsage'],  # {str} '21'
            'power': itm['power'] / WATT_FACTOR,  # {str} '1085731242.000000'
            'powerSampleCount': itm['powerSampleCount'],  # {str} '3'
            'powerSamplingPeriod': itm['powerSamplingPeriod'] / 1000.,  # {str} '33'
            'productName': itm['productName'],  # {str} 'Quadro K620'
            'productType': PROD_TYPE_LU.get(itm['productType'], '???'),  # {str} '2'
            'uname': itm['uname'],  # {str} 'Quadro K620'
            'ver': itm['ver'],  # {str} 'Unsupported'
            'verVBIOS': itm['verVBIOS'],  # {str} 'Unsupported'
            'videoCodec': itm['videoCodec'],  # {str} 'Unsupported'
        }
