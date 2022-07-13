from agentcoreclient import IgnoreResultException
from aiowmi.query import Query

from .base import Base
from .utils import parse_wmi_date


class CheckCimDatafile(Base):  # TODO what check_name should this check get?
    type_name = 'cimDatafile'  # TODO what type_name should this check get?

    @classmethod
    def _get_query(cls, data):
        files = data.get('files')  # TODO are files already escaped properly?
        if not files:
            raise IgnoreResultException(
                f'{cls.__name__} did not run; no files are provided')

        select_from = '''\
        SELECT Name, LastAccessed, LastModified, FileSize, Readable, \
        Writeable, Hidden, System FROM cim_datafile\
        '''
        files = [f'name=\'{file}\'' for file in files]
        where_itms = ' OR '.join(files)
        qry = f'{select_from} WHERE {where_itms}'
        return Query(qry, namespace=cls.namespace)

    @staticmethod
    def on_item(itm):
        return {
            'fileSize': itm['FileSize'],  # int
            'hidden': itm['Hidden'],  # bool
            'lastAccessed': parse_wmi_date(itm['LastAccessed']),  # time?
            'lastModified': parse_wmi_date(itm['LastModified']),  # time?
            'name': itm['Name'],  # str
            'readable': itm['Readable'],  # bool
            'system': itm['System'],  # bool
            'writeable': itm['Writeable'],  # bool
        }

# Example output:

# FileSize: 738197504
# Hidden: True
# LastAccessed: 2022-06-15 23:58:22.954782+02:00
# LastModified: 2022-06-15 23:58:22.954782+02:00
# Name: c:\pagefile.sys
# Readable: True
# System: True
# Writeable: True