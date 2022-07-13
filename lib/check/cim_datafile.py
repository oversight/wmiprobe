import re

from aiowmi.query import Query
from libprobe.asset import Asset
from libprobe.exceptions import IgnoreCheckException
from typing import Tuple

from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "cim_datafile"  # TODO what type_name should this check get?


def on_item(itm: dict) -> Tuple[str, dict]:
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


async def check_cim_datafile(  # TODO what check_name should this check get?
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    # TODO are files already escaped properly?
    files = check_config.get('files')
    if not files:
        raise IgnoreCheckException(
            f'{check_cim_datafile.__name__} did not run; no files are provided')

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
    qry = select_from + ' WHERE ' + where_itms
    rows = await wmiquery(asset, asset_config, check_config, Query(qry))
    state = get_state(TYPE_NAME, rows, on_item)
    return state

# Example output:

# FileSize: 738197504
# Hidden: True
# LastAccessed: 2022-06-15 23:58:22.954782+02:00
# LastModified: 2022-06-15 23:58:22.954782+02:00
# Name: c:\pagefile.sys
# Readable: True
# System: True
# Writeable: True