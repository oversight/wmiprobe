from .base import Base


class CheckExchangeQueue(Base):

    qry = '''
    SELECT * FROM
    Win32_PerfFormattedData_MSExchangeTransportQueues_MSExchangeTransportQueues
    '''

    type_name = 'exchangeQueue'

    @staticmethod
    def on_item(itm):
        """Parse item.

        We lack information about the Win32_PerfFormattedData_MSExch.. class.
        It seems that at least exchange version 14.x is returning a single
        metric, for example `LargestDeliveryQueueLength` while (at least)
        version 15.x is returning two metrics for both Internal/External.
        Since no documentation can be found (at the time of writing) what the
        content of these metrics really are, we just test and merge them
        together to make the values compatible with earlier versions.

        Issue #4 (wmiprobe) is related.
        """

        a = itm.get('InternalAggregateDeliveryQueueLengthAllInternalQueues')
        b = itm.get('ExternalAggregateDeliveryQueueLengthAllExternalQueues')
        if a is not None and b is not None:
            itm['AggregateDeliveryQueueLengthAllQueues'] = a + b

        a = itm.get('InternalActiveRemoteDeliveryQueueLength')
        b = itm.get('ExternalActiveRemoteDeliveryQueueLength')
        if a is not None and b is not None:
            itm['ActiveRemoteDeliveryQueueLength'] = a + b

        a = itm.get('InternalRetryRemoteDeliveryQueueLength')
        b = itm.get('ExternalRetryRemoteDeliveryQueueLength')
        if a is not None and b is not None:
            itm['RetryRemoteDeliveryQueueLength'] = a + b

        a = itm.get('InternalLargestDeliveryQueueLength')
        b = itm.get('ExternalLargestDeliveryQueueLength')
        if a is not None and b is not None:
            itm['LargestDeliveryQueueLength'] = a + b

        return {
            'name':
                itm['Name'],
            'aggregateDeliveryQueueLengthAllQueues':
                itm['AggregateDeliveryQueueLengthAllQueues'],
            'activeMailboxDeliveryQueueLength':
                itm['ActiveMailboxDeliveryQueueLength'],
            'activeRemoteDeliveryQueueLength':
                itm['ActiveRemoteDeliveryQueueLength'],
            'submissionQueueLength':
                itm['SubmissionQueueLength'],
            'activeNonSmtpDeliveryQueueLength':
                itm['ActiveNonSmtpDeliveryQueueLength'],
            'retryMailboxDeliveryQueueLength':
                itm['RetryMailboxDeliveryQueueLength'],
            'retryNonSmtpDeliveryQueueLength':
                itm['RetryNonSmtpDeliveryQueueLength'],
            'retryRemoteDeliveryQueueLength':
                itm['RetryRemoteDeliveryQueueLength'],
            'unreachableQueueLength':
                itm['UnreachableQueueLength'],
            'largestDeliveryQueueLength':
                itm['LargestDeliveryQueueLength'],
            'poisonQueueLength':
                itm['PoisonQueueLength'],
        }
