from .checkCitrixLogonTimings import CheckCitrixLogonTimings
from .checkDiskIo import CheckDiskIo
from .checkDiskQueueLength import CheckDiskQueueLength
from .checkExchangeQueue import CheckExchangeQueue
from .checkICAlatency import CheckICAlatency
from .checkInstalledSoftware import CheckInstalledSoftware
from .checkInterface import CheckInterface
from .checkIp4RouteTable import CheckIp4RouteTable
from .checkLoggedOnUsers import CheckLoggedOnUsers
from .checkMemory import CheckMemory
from .checkNetworkAdapter import CheckNetworkAdapter
from .checkNvidiaGpu import CheckNvidiaGpu
from .checkNvidiaGpuTemperature import CheckNvidiaGpuTemperature
from .checkOsMemory import CheckOsMemory
from .checkPageFile import CheckPageFile
from .checkPnpEntity import CheckPnpEntity
from .checkProcess import CheckProcess
from .checkSystemTime import CheckSystemTime
from .checkUpdates import CheckUpdates
from .checkUptime import CheckUptime
from .checkVolume import CheckVolume
from .checkWindowsCountRemoteUsers import CheckWindowsCountRemoteUsers
from .checkWindowsNTDomain import CheckWindowsNTDomain
from .checkWindowsNTEventLog import CheckWindowsNTEventLog
from .checkWindowsPerfData import CheckWindowsPerfData
from .checkWindowsServices import CheckWindowsServices


CHECKS = {
    # 'CheckCitrixLogonTimings': CheckCitrixLogonTimings,
    'CheckDiskIo': CheckDiskIo,
    'CheckDiskQueueLength': CheckDiskQueueLength,
    # 'CheckExchangeQueue': CheckExchangeQueue,
    # 'CheckICAlatency': CheckICAlatency,
    'CheckInstalledSoftware': CheckInstalledSoftware,
    'CheckInterface': CheckInterface,
    'CheckIp4RouteTable': CheckIp4RouteTable,
    'CheckLoggedOnUsers': CheckLoggedOnUsers,
    'CheckMemory': CheckMemory,
    'CheckNetworkAdapter': CheckNetworkAdapter,
    'CheckOsMemory': CheckOsMemory,
    'CheckPageFile': CheckPageFile,
    'CheckPnpEntity': CheckPnpEntity,
    'CheckProcess': CheckProcess,
    'CheckSystemTime': CheckSystemTime,
    'CheckUpdates': CheckUpdates,
    'CheckUptime': CheckUptime,
    'CheckVolume': CheckVolume,
    'CheckWindowsCountRemoteUsers': CheckWindowsCountRemoteUsers,
    'CheckWindowsNTDomain': CheckWindowsNTDomain,
    'CheckWindowsNTEventLog': CheckWindowsNTEventLog,
    'CheckWindowsPerfData': CheckWindowsPerfData,
    'CheckWindowsServices': CheckWindowsServices,
    # 'CheckNvidiaGpu': CheckNvidiaGpu,
    # 'CheckNvidiaGpuTemperature': CheckNvidiaGpuTemperature
}
