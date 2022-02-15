from .base import Base


class CheckWindowsCountRemoteUsers(Base):

    qry = 'SELECT Caption FROM Win32_Process WHERE Caption=\'winlogon.exe\''
    type_name = 'remote_users'

    def iterate_results(self, wmi_data):
        user_count = len(wmi_data) - 1
        return {
            self.type_name: [{'name': 'system', 'userCount': user_count}]
        }
