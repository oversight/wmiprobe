from .base import Base
from .valueLookups import STATUS_INFO
from .valueLookups import CONFIG_MAN_ERR_CODE
from .valueLookups import AVAILABILITY_LU


class CheckNetworkAdapter(Base):

    qry = '''
    SELECT
    AdapterType, AutoSense, Availability, ConfigManagerErrorCode,
    ConfigManagerUserConfig, Description, InstallDate, Installed,
    InterfaceIndex, LastErrorCode, MACAddress, Manufacturer,
    MaxNumberControlled, MaxSpeed, NetConnectionID, NetConnectionStatus,
    NetEnabled, NetworkAddresses, PermanentAddress, PhysicalAdapter,
    PNPDeviceID, PowerManagementSupported, ProductName, ServiceName, Speed,
    Status, StatusInfo, SystemCreationClassName, SystemName, TimeOfLastReset
    FROM Win32_NetworkAdapter
    '''
    type_name = 'adapter'
    interval = 300

    @staticmethod
    def on_item(itm):

        return {
            'name': itm['PNPDeviceID'],
            'adapterType': itm['AdapterType'],
            'autoSense': itm['AutoSense'],
            'availability': AVAILABILITY_LU.get(itm['Availability']),
            'configManagerErrorCode':
                CONFIG_MAN_ERR_CODE.get(itm['ConfigManagerErrorCode']),
            'configManagerUserConfig': itm['ConfigManagerUserConfig'],
            'description': itm['Description'],
            'installDate': itm['InstallDate'],
            'installed': itm['Installed'],
            'interfaceIndex': itm['InterfaceIndex'],
            'lastErrorCode': itm['LastErrorCode'],
            'MACAddress': itm['MACAddress'],
            'manufacturer': itm['Manufacturer'],
            'maxNumberControlled': itm['MaxNumberControlled'],
            'maxSpeed': itm['MaxSpeed'],
            'netConnectionID': itm['NetConnectionID'],
            'netConnectionStatus': itm['NetConnectionStatus'],
            'netEnabled': itm['NetEnabled'],
            'networkAddresses': itm['NetworkAddresses'],
            'permanentAddress': itm['PermanentAddress'],
            'physicalAdapter': itm['PhysicalAdapter'],
            'PNPDeviceID': itm['PNPDeviceID'],
            'powerManagementSupported': itm['PowerManagementSupported'],
            'productName': itm['ProductName'],
            'serviceName': itm['ServiceName'],
            'speed': itm['Speed'],
            'status': itm['Status'],
            'statusInfo': STATUS_INFO.get(itm['StatusInfo']),
            'timeOfLastReset': itm['TimeOfLastReset'],
        }
