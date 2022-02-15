from .base import Base


class CheckOsMemory(Base):

    qry = (
        'SELECT '
        'CommitLimit, CommittedBytes, PercentCommittedBytesInUse '
        'from Win32_PerfFormattedData_PerfOS_Memory'
    )
    type_name = 'perfOSMemory'

    def on_item(self, itm):
        return {
            'name': 'OSMemory',
            'commitLimit': itm['CommitLimit'],
            'committedBytes': itm['CommittedBytes'],
            'percentCommittedBytesInUse': itm['PercentCommittedBytesInUse'],
        }
