from .base import Base
from .languageNames import LANGUAGE_NAMES
from .utils import parse_wmi_date


INSTALL_STATES_LU = {
    -6: 'Bad Configuration',
    -2: 'Invalid Argument',
    -1: 'Unknown Package',
    1: 'Advertised',
    2: 'Absent',
    5: 'Installed'
}


class CheckInstalledSoftware(Base):

    qry = 'SELECT Caption, Description, InstallDate, InstallDate2, InstallLocation, InstallSource, InstallState, ' \
          'Language, LocalPackage, Name, PackageCache, PackageCode, PackageName, ProductID, RegCompany, RegOwner, ' \
          'SKUNumber, Transforms, URLInfoAbout, URLUpdateInfo, Vendor, Version FROM Win32_Product'
    type_name = 'win32product'
    defaultCheckInterval = 11 * 3600

    def on_item(self, itm):
        try:
            language_number = int(itm['Language'])
            language_name = LANGUAGE_NAMES.get(language_number, language_number)
        except Exception:
            language_name = None
        install_date = itm['InstallDate2'] or parse_wmi_date(itm['InstallDate'])
        install_state_number = itm['InstallState']
        install_state = INSTALL_STATES_LU.get(install_state_number, install_state_number)

        return {
            'name': itm['PackageCode'],
            'caption': itm['Caption'],
            'description': itm['Description'],
            'installDate': install_date,
            'installLocation': itm['InstallLocation'],
            'installSource': itm['InstallSource'],
            'installState': install_state,
            'language': language_name,
            'localPackage': itm['LocalPackage'],
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
