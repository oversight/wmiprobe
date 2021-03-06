from .base import Base


class CheckMemory(Base):

    qry = '''
    SELECT
    Name, Caption, FreePhysicalMemory, TotalVisibleMemorySize
    FROM Win32_OperatingSystem
    '''
    type_name = 'memory'

    @staticmethod
    def on_item(itm):
        free = itm['FreePhysicalMemory']
        total = itm['TotalVisibleMemorySize']
        used = total - free
        pct = 100. * used / total if total else 0.

        return {
            'name': 'memory',
            'osVersion': itm['Caption'].strip(),
            'freePhysicalMemory': free,
            'totalVisibleMemorySize': total,
            'percentUsed': pct
        }
