from genericpath import exists
import re

from aiowmi.query import Query
from libprobe.asset import Asset
from libprobe.exceptions import IgnoreCheckException
from typing import Tuple

from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "cim_datafile"


def on_item(itm: dict) -> dict:
    return {
        'name': itm['Name'],  # str
        'FileSize': itm['FileSize'],  # int
        'Hidden': itm['Hidden'],  # bool
        'LastAccessed': int(itm['LastAccessed']),  # time?
        'LastModified': int(itm['LastModified']),  # time?
        'Readable': itm['Readable'],  # bool
        'System': itm['System'],  # bool
        'Writeable': itm['Writeable'],  # bool
        'Exists': True,  # itm['Name'], {bool
    }


async def check_cim_datafile(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    cim_datafiles = check_config.get('cim_datafiles')
    if not cim_datafiles:
        raise IgnoreCheckException()

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

    rows = await wmiquery(asset, asset_config, check_config, Query(qry))
    state = get_state(TYPE_NAME, rows, on_item)
    item_list = state[TYPE_NAME]
    names = set(item['name'] for item in item_list)

    # Append non-existing files to the state
    for fn in cim_datafiles:
        if fn not in names:
            item_list.append({
                'name': fn,
                'Exists': False
            })

    return state
