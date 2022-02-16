from .base import Base


class CheckWindowsServices(Base):

    qry = '''
    SELECT
    Caption, DesktopInteract, ExitCode, PathName, ServiceSpecificExitCode,
    ServiceType, State, Status, Name, DisplayName, Description, ProcessId,
    StartMode, StartName, Started
    FROM Win32_Service
    '''
    type_name = 'services'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'],
            'displayName': itm['DisplayName'],
            'description': itm['Description'],
            'processId': itm['ProcessId'],
            'started': itm['Started'],
            'startMode': itm['StartMode'],
            'startName': itm['StartName'],
            'caption': itm['Caption'],
            'desktopInteract': itm['DesktopInteract'],
            'exitCode': itm['ExitCode'],
            'pathName': itm['PathName'],
            'serviceSpecificExitCode': itm['ServiceSpecificExitCode'],
            'serviceType': itm['ServiceType'],
            'state': itm['State'],
            'status': itm['Status'],
        }
