from .base import Base
from .utils import parse_wmi_date, parse_wmi_date_1600


class CheckUpdates(Base):

    qry = 'SELECT Caption, Description, InstallDate, Name, Status, CSName, FixComments, HotFixID, InstalledBy, ' \
          'InstalledOn, ServicePackInEffect FROM Win32_QuickFixEngineering'
    type_name = 'updates'
    defaultCheckInterval = 11 * 3600

    def on_item(self, itm):
        # InstalledOn can be multiple datestring formats or windows timestamp (nanoseconds FROM 1600)
        installed_on_str = itm['InstalledOn']
        installed_on = parse_wmi_date(installed_on_str, '%m/%d/%Y') or \
            parse_wmi_date(installed_on_str, '%m-%d-%Y') or \
            parse_wmi_date(installed_on_str) or \
            parse_wmi_date_1600(installed_on_str)

        return {
            'name': itm['HotFixID'],
            'Caption': itm['Caption'],
            'Description': itm['Description'],
            'InstallDate': itm['InstallDate'],
            'Status': itm['Status'],
            'CSName': itm['CSName'],
            'FixComments': itm['FixComments'],
            'HotFixID': itm['HotFixID'],
            'InstalledBy': itm['InstalledBy'],
            'InstalledOn': installed_on,
            'ServicePackInEffect': itm['ServicePackInEffect'],
        }

    def iterate_results(self, wmi_data):
        state = {}
        state[self.typeName] = itms = self.on_items(wmi_data)
        last = None
        for itm in itms.values():
            if itm['InstalledOn'] and (not last or itm['InstalledOn'] > last['InstalledOn']):
                last = itm
        if last:
            state['last_update'] = [{
                'name': 'last_update',
                'last_update': last['HotFixID'],
                'last_up_date': last['InstalledOn']
            }]

        return state
