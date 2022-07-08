from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery
from .languageNames import LANGUAGE_NAMES
from .utils import parse_wmi_date
from .valueLookups import INSTALL_STATES_LU

TYPE_NAME = "installed_software"
QUERY = """
    SELECT
    Description, InstallDate, InstallDate2, InstallLocation, InstallSource,
    InstallState, Language, Name, PackageCache, PackageCode, PackageName,
    ProductID, RegCompany, RegOwner, SKUNumber, Transforms, URLInfoAbout,
    URLUpdateInfo, Vendor, Version
    FROM Win32_Product
"""


def on_item(itm: dict) -> Tuple[str, dict]:
    try:
        language = int(itm['Language'])
        language_name = LANGUAGE_NAMES.get(language, language)
    except Exception:
        language_name = None
    install_date = itm.pop('InstallDate2', None) or \
        parse_wmi_date(itm['InstallDate'])
    install_state_number = itm['InstallState']
    install_state = INSTALL_STATES_LU.get(
        install_state_number, install_state_number)

    return itm.pop('PackageCode'), {
        **itm,
        'InstallDate': install_date,
        'InstallState': install_state,
        'Language': language_name,
    }


async def check_installed_software(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
