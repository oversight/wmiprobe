from .base import Base
from .languageNames import LANGUAGE_NAMES
from .valueLookups import INSTALL_STATES_LU
from .utils import parse_wmi_date


class CheckInstalledSoftware(Base):

    qry = '''
    SELECT
    Description, InstallDate, InstallDate2, InstallLocation, InstallSource,
    InstallState, Language, Name, PackageCache, PackageCode, PackageName,
    ProductID, RegCompany, RegOwner, SKUNumber, Transforms, URLInfoAbout,
    URLUpdateInfo, Vendor, Version
    FROM Win32_Product
    '''
    type_name = 'win32product'
    interval = 39600

    @staticmethod
    def on_item(itm):
        try:
            language = int(itm['Language'])
            language_name = LANGUAGE_NAMES.get(language, language)
        except Exception:
            language_name = None
        install_date = itm['InstallDate2'] or \
            parse_wmi_date(itm['InstallDate'])
        install_state_number = itm['InstallState']
        install_state = INSTALL_STATES_LU.get(
            install_state_number, install_state_number)

        return {
            'name': itm['PackageCode'],
            'description': itm['Description'],
            'installDate': install_date,
            'installLocation': itm['InstallLocation'],
            'installSource': itm['InstallSource'],
            'installState': install_state,
            'language': language_name,
            'packageCache': itm['PackageCache'],
            'packageCode': itm['PackageCode'],
            'packageName': itm['PackageName'],
            'productID': itm['ProductID'],
            'regCompany': itm['RegCompany'],
            'regOwner': itm['RegOwner'],
            'SKUNumber': itm['SKUNumber'],
            'transforms': itm['Transforms'],
            'URLInfoAbout': itm['URLInfoAbout'],
            'URLUpdateInfo': itm['URLUpdateInfo'],
            'vendor': itm['Vendor'],
            'version': itm['Version'],
        }
