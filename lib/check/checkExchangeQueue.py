from .base import Base


class CheckExchangeQueue(Base):

    qry = 'SELECT AggregateDeliveryQueueLengthAllQueues, \
        ActiveMailboxDeliveryQueueLength, \
        ActiveRemoteDeliveryQueueLength, \
        SubmissionQueueLength, \
        ActiveNonSmtpDeliveryQueueLength, \
        RetryMailboxDeliveryQueueLength, \
        RetryNonSmtpDeliveryQueueLength, \
        RetryRemoteDeliveryQueueLength, \
        UnreachableQueueLength, \
        LargestDeliveryQueueLength, \
        PoisonQueueLength \
        FROM Win32_PerfFormattedData_MSExchangeTransportQueues_MSExchangeTransportQueues'

    type_name = 'exchangeQueue'
    required_services = ['wmi', 'exchange']

    def on_item(self, itm):
        return {
            'name': itm['Name'],
            'aggregateDeliveryQueueLengthAllQueues': itm['AggregateDeliveryQueueLengthAllQueues'],
            'activeMailboxDeliveryQueueLength': itm['ActiveMailboxDeliveryQueueLength'],
            'activeRemoteDeliveryQueueLength': itm['ActiveRemoteDeliveryQueueLength'],
            'submissionQueueLength': itm['SubmissionQueueLength'],
            'activeNonSmtpDeliveryQueueLength': itm['ActiveNonSmtpDeliveryQueueLength'],
            'retryMailboxDeliveryQueueLength': itm['RetryMailboxDeliveryQueueLength'],
            'retryNonSmtpDeliveryQueueLength': itm['RetryNonSmtpDeliveryQueueLength'],
            'retryRemoteDeliveryQueueLength': itm['RetryRemoteDeliveryQueueLength'],
            'unreachableQueueLength': itm['UnreachableQueueLength'],
            'largestDeliveryQueueLength': itm['LargestDeliveryQueueLength'],
            'poisonQueueLength': itm['PoisonQueueLength'],
        }
