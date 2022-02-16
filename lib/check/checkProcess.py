from .base import Base


NON_SUMMABLES = {
    'description',
    'creatingProcessID',
    'IdProcess',
    'priorityBase',
    'name',
    'pageFileBytesPeak',
    'virtualBytesPeak',
    'workingSetPeak'
}


class CheckProcess(Base):

    qry = '''
    SELECT
    Name, Description, CreatingProcessID, ElapsedTime, HandleCount, IDProcess,
    IODataBytesPersec, IODataOperationsPersec, IOOtherBytesPersec,
    IOOtherOperationsPersec, IOReadBytesPersec, IOReadOperationsPersec,
    IOWriteBytesPersec, IOWriteOperationsPersec, PageFaultsPersec,
    PageFileBytes, PageFileBytesPeak, PercentPrivilegedTime,
    PercentProcessorTime, PercentUserTime, PoolNonpagedBytes, PoolPagedBytes,
    PriorityBase, PrivateBytes, ThreadCount, VirtualBytes, VirtualBytesPeak,
    WorkingSet, WorkingSetPeak
    FROM Win32_PerfFormattedData_PerfProc_Process
    '''
    type_name = 'process'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'],
            'description': itm['Description'],
            'creatingProcessID': itm['CreatingProcessID'],
            'elapsedTime': itm['ElapsedTime'],
            'handleCount': itm['HandleCount'],
            'IdProcess': itm['IDProcess'],
            'IoDataBytesPersec': itm['IODataBytesPersec'],
            'IoDataOperationsPersec': itm['IODataOperationsPersec'],
            'IoOtherBytesPersec': itm['IOOtherBytesPersec'],
            'IoOtherOperationsPersec': itm['IOOtherOperationsPersec'],
            'IoReadBytesPersec': itm['IOReadBytesPersec'],
            'IoReadOperationsPersec': itm['IOReadOperationsPersec'],
            'IoWriteBytesPersec': itm['IOWriteBytesPersec'],
            'IoWriteOperationsPersec': itm['IOWriteOperationsPersec'],
            'pageFaultsPersec': itm['PageFaultsPersec'],
            'pageFileBytes': itm['PageFileBytes'],
            'pageFileBytesPeak': itm['PageFileBytesPeak'],
            'percentPrivilegedTime': itm['PercentPrivilegedTime'],
            'percentProcessorTime': itm['PercentProcessorTime'],
            'percentUserTime': itm['PercentUserTime'],
            'poolNonpagedBytes': itm['PoolNonpagedBytes'],
            'poolPagedBytes': itm['PoolPagedBytes'],
            'priorityBase': itm['PriorityBase'],
            'privateBytes': itm['PrivateBytes'],
            'threadCount': itm['ThreadCount'],
            'virtualBytes': itm['VirtualBytes'],
            'virtualBytesPeak': itm['VirtualBytesPeak'],
            'workingSet': itm['WorkingSet'],
            'workingSetPeak': itm['WorkingSetPeak'],
        }

    @classmethod
    def iterate_results(cls, wmi_data):
        itms = cls.on_items(wmi_data)
        total_itm = itms.pop('_Total')

        hash_names = [name for name in itms if '#' in name]
        for hash_name in hash_names:
            name = hash_name.split('#')[0]
            if name not in itms:
                continue
            hash_dct = itms.pop(hash_name)
            itm = itms[name]
            if 'processCount' in itm:
                itm['processCount'] += 1
            else:
                itm['processCount'] = 2  # this is the second instance
            for ky in set(hash_dct) - NON_SUMMABLES:
                itm[ky] += hash_dct[ky]

        for itm in itms.values():
            if 'processCount' in itm:
                itm['privateBytesAvg'] = \
                    itm['privateBytes'] / itm['processCount']
            else:
                itm['privateBytesAvg'] = itm['privateBytes']

        return {
            cls.type_name: itms,
            cls.type_name + '_Total': [total_itm],
        }
