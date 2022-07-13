import re
from agentcoreclient import IgnoreResultException
from aiowmi.query import Query

from .base import Base


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

        # This sub will guarantee that the `file` string is created with 4
        # backslashes, in the `join` the 4 are escaped to 2, which are required
        # in the `Query`.
        files = ['name=\'' + re.sub(r"\\+", "\\\\\\\\", file) + '\''
            for file in files]
        where_itms = ' OR '.join(files)
        qry = f'{select_from} WHERE {where_itms}'
        return Query(qry, namespace=cls.namespace)

    @staticmethod
    def on_item(itm):
        return {
            'fileSize': itm['FileSize'],  # int
            'hidden': itm['Hidden'],  # bool
            'lastAccessed': int(itm['LastAccessed']),  # time?
            'lastModified': int(itm['LastModified']),  # time?
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