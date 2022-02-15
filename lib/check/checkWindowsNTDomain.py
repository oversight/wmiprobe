from .base import Base


class CheckWindowsNTDomain(Base):

    qry = 'SELECT DomainName, DnsForestName, DomainControllerName FROM Win32_NTDomain WHERE DomainName IS NOT NULL'
    type_name = 'domain'

    def on_item(self, itm):
        return {
            'name': itm['DomainName'],
            'dnsForest': itm['DnsForestName'],
            'domainController': itm['DomainControllerName'].strip('\\\\')
        }
