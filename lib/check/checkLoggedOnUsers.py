import logging
from collections import defaultdict
from .base import Base


class CheckLoggedOnUsers(Base):

    qry = 'SELECT * FROM Win32_LoggedOnUser'
    type_name = 'users'

    def _get_itemname(self, itm):
        try:
            splitted = itm['Antecedent'].split('"')
            return splitted[1] + '\\' + splitted[3]
        except Exception as e:
            logging.error(e)
            return None

    def _get_logonid(self, itm):
        try:
            splitted = itm['Dependent'].split('"')
            return splitted[1]
        except Exception as e:
            logging.error(e)
            return None

    def iterate_results(self, wmi_data):
        name_login = defaultdict(list)
        for itm in wmi_data:
            name = self._get_itemname(itm)
            logon_id = self._get_logonid(itm)
            name_login[name].append(logon_id)

        itms = [
            {
                'name': name,
                'logonIds': ','.join(logon_ids),
                'sessionCount': len(logon_ids)
            }
            for name, logon_ids in name_login.items()
        ]

        total_itm = {'name': '_Total', 'count': len(wmi_data)}

        return {
            self.type_name: itms,
            self.type_name + '_Total': [total_itm]
        }
