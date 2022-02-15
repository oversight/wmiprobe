from .base import Base


class CheckInterface(Base):

    qry = 'SELECT BytesReceivedPersec, BytesSentPersec, CurrentBandwidth, Name, packetsReceivedPersec, packetsSentPersec, PacketsOutboundDiscarded, PacketsOutboundErrors, PacketsReceivedDiscarded, PacketsReceivedErrors, OutputQueueLength FROM Win32_PerfFormattedData_Tcpip_NetworkInterface'
    type_name = 'interface'

    def on_item(self, itm):
        return {
            'name': itm['Name'],
            'BytesReceivedPersec': itm['BytesReceivedPersec'],
            'BytesSentPersec': itm['BytesSentPersec'],
            'CurrentBandwidth': itm['CurrentBandwidth'],
            'PacketsReceivedPersec': itm['PacketsReceivedPersec'],
            'PacketsSentPersec': itm['PacketsSentPersec'],
            'PacketsOutboundDiscarded': itm['PacketsOutboundDiscarded'],
            'PacketsOutboundErrors': itm['PacketsOutboundErrors'],
            'PacketsReceivedDiscarded': itm['PacketsReceivedDiscarded'],
            'PacketsReceivedErrors': itm['PacketsReceivedErrors'],
            'OutputQueueLength': itm['OutputQueueLength'],
        }
