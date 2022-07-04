from .base import Base


class CheckIp4RouteTable(Base):

    qry = '''
    SELECT
    Name, Age, Caption, Description, Destination, Information, InterfaceIndex,
    Mask, Metric1, Metric2, Metric3, Metric4, Metric5, NextHop, Protocol,
    Status, InstallDate, Type
    FROM Win32_IP4RouteTable
    '''
    type_name = 'route'
    interval = 300

    @staticmethod
    def on_item(itm):
        return {
            'name': '{Destination} [{InterfaceIndex}]'.format_map(itm),
            'age': itm['Age'],
            'caption': itm['Caption'],
            'description': itm['Description'],
            'destination': itm['Destination'],
            'information': itm['Information'],
            'interfaceIndex': itm['InterfaceIndex'],
            'mask': itm['Mask'],
            'metric1': itm['Metric1'],
            'metric2': itm['Metric2'],
            'metric3': itm['Metric3'],
            'metric4': itm['Metric4'],
            'metric5': itm['Metric5'],
            'nextHop': itm['NextHop'],
            'protocol': itm['Protocol'],
            'status': itm['Status'],
            'installDate': itm['InstallDate'],
            'type': itm['Type'],
        }
