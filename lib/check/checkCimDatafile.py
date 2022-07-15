import re
from typing import Optional
from agentcoreclient import IgnoreResultException
from aiowmi.query import Query

from .base import Base


class CheckCimDatafile(Base):
    type_name = 'cimDatafile'

    @staticmethod
    def get_cim_datafiles(data: dict) -> Optional[list]:
        try:
            cim_datafiles = \
                data['hostConfig']['probeConfig']['wmiProbe']['cimDatafiles']
        except KeyError:
            return []
        else:
            return cim_datafiles

    @classmethod
    def _get_query(cls, data):
        cim_datafiles = cls.get_cim_datafiles(data)
        if not cim_datafiles:
            raise IgnoreResultException(
                f'{cls.__name__} did not run; no files are provided')

        select_from = (
            'SELECT Name, LastAccessed, LastModified, FileSize, Readable, '
            'Writeable, Hidden, System FROM cim_datafile'
        )

        # This sub will guarantee that the `file` string is created with 4
        # backslashes, in the `join` the 4 are escaped to 2, which are required
        # in the `Query`.
        files = (
            'name=\'' + re.sub(r"\\+", r"\\\\", fn) + '\''
            for fn in cim_datafiles)
        where_itms = ' OR '.join(files)
        qry = select_from + ' WHERE ' + where_itms
        return Query(qry, namespace=cls.namespace)

    @staticmethod
    def on_item(itm):
        return {
            'fileSize': itm['FileSize'],  # int
            'hidden': itm['Hidden'],  # bool
            'lastAccessed': int(itm['LastAccessed']),  # timestamp
            'lastModified': int(itm['LastModified']),  # timestamp
            'name': itm['Name'],  # str
            'readable': itm['Readable'],  # bool
            'system': itm['System'],  # bool
            'writeable': itm['Writeable'],  # bool
            'exists': True,  # bool
        }

    @classmethod
    def iterate_results(cls, wmi_data, data):
        itms = cls.on_items(wmi_data)

        # Append non-existing files to the state
        cim_datafiles = cls.get_cim_datafiles(data)
        if cim_datafiles:
            for fn in cim_datafiles:
                if fn not in itms:
                    itms[fn] = {'exists': False}

        state = {}
        state[cls.type_name] = itms
        return state
