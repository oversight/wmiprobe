from .base import Base


class CheckPageFile(Base):

    qry = 'SELECT Name, AllocatedBaseSize, CurrentUsage FROM Win32_PageFileUsage'
    type_name = 'pageFile'

    def on_item(self, itm):
        total = itm['AllocatedBaseSize'] * 1024 * 1024
        used = itm['CurrentUsage'] * 1024 * 1024
        free = total - used
        percentage = 100. * used / total if total else 0.

        return {
            'name': itm['Name'],
            'bytesTotal': total,
            'bytesFree': free,
            'bytesUsed': used,
            'percentUsed': percentage
        }

    def iterate_results(self, wmi_data):
        itms = self.on_items(wmi_data)
        total_itm = {
            'name': '_Total',
            'bytesTotal': 0,
            'bytesFree': 0,
            'bytesUsed': 0
        }

        for itm in itms.values():
            total_itm['bytesTotal'] += itm['bytesTotal']
            total_itm['bytesFree'] += itm['bytesFree']
            total_itm['bytesUsed'] += itm['bytesUsed']

        total = total_itm['bytesTotal']
        used = total_itm['bytesUsed']
        total_itm['percentUsed'] = 100. * used / total if total else 0.
        return {
            self.type_name: itms,
            self.type_name + '_Total': [total_itm],
        }
