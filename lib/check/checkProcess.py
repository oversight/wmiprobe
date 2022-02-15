from .base import Base


NON_SUMMABLES = {
    'description',
    'creatingProcessID',
    'frequency_Object',
    'frequency_PerfTime',
    'frequency_Sys100NS',
    'timestamp_Object',
    'timestamp_PerfTime',
    'timestamp_Sys100NS',
    'IdProcess',
    'priorityBase',
    'name',
    'pageFileBytesPeak',
    'virtualBytesPeak',
    'workingSetPeak'
}


class CheckProcess(Base):

    qry = 'SELECT * FROM Win32_PerfFormattedData_PerfProc_Process'
    type_name = 'process'

    def on_item(self, itm):
        return {
            'name': itm['Name'],
            'description': itm['Description'],
            'creatingProcessID': itm['CreatingProcessID'],
            'elapsedTime': itm['ElapsedTime'],
            'frequency_Object': itm['Frequency_Object'],
            'frequency_PerfTime': itm['Frequency_PerfTime'],
            'frequency_Sys100NS': itm['Frequency_Sys100NS'],
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
            'timestamp_Object': itm['Timestamp_Object'],
            'timestamp_PerfTime': itm['Timestamp_PerfTime'],
            'timestamp_Sys100NS': itm['Timestamp_Sys100NS'],
            'virtualBytes': itm['VirtualBytes'],
            'virtualBytesPeak': itm['VirtualBytesPeak'],
            'workingSet': itm['WorkingSet'],
            'workingSetPeak': itm['WorkingSetPeak'],
        }

    def iterate_results(self, wmi_data):
        itms = self.on_items(wmi_data)
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
                itm['privateBytesAvg'] = itm['privateBytes'] / itm['processCount']
            else:
                itm['privateBytesAvg'] = itm['privateBytes']

        return {
            self.type_name: itms,
            self.type_name + '_Total': total_itm,
        }
