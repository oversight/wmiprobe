import logging
from collections import defaultdict
from .base import Base


class CheckLoggedOnUsers(Base):

    qry = 'SELECT Antecedent, Dependent FROM Win32_LoggedOnUser'
    type_name = 'users'

    @staticmethod
    def _get_itemname(itm):
        try:
            splitted = itm['Antecedent'].split('"')
            return splitted[1] + '\\' + splitted[3]
        except Exception as e:
            logging.error(e)
            return None

    @staticmethod
    def _get_logonid(itm):
        try:
            splitted = itm['Dependent'].split('"')
            return splitted[1]
        except Exception as e:
            logging.error(e)
            return None

    @classmethod
    def iterate_results(cls, wmi_data):
        name_login = defaultdict(list)
        for itm in wmi_data:
            name = cls._get_itemname(itm)
            logon_id = cls._get_logonid(itm)
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
            cls.type_name: itms,
            cls.type_name + '_Total': [total_itm]
        }
