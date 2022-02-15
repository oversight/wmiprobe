from .base import Base


class CheckOsMemory(Base):

    qry = (
        'SELECT '
        'CommitLimit, CommittedBytes, PercentCommittedBytesInUse '
        'from Win32_PerfFormattedData_PerfOS_Memory'
    )
    type_name = 'perfOSMemory'

    @staticmethod
    def on_item(itm):
        return {
            'name': 'OSMemory',
            'commitLimit': itm['CommitLimit'],
            'committedBytes': itm['CommittedBytes'],
            'percentCommittedBytesInUse': itm['PercentCommittedBytesInUse'],
        }
