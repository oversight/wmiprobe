from .base import Base


class CheckWindowsCountRemoteUsers(Base):

    qry = '''
    SELECT
    Caption
    FROM Win32_Process
    WHERE Caption=\'winlogon.exe\'
    '''
    type_name = 'remote_users'

    @classmethod
    def iterate_results(cls, wmi_data):
        user_count = len(wmi_data) - 1
        return {
            cls.type_name: [{'name': 'system', 'userCount': user_count}]
        }
