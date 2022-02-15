from .base import Base

# https://www.citrix.com/blogs/2014/05/30/wmi-objects-used-by-citrix-director-for-troubleshooting-sessions-2/


class CheckCitrixLogonTimings(Base):

    qry = 'SELECT * FROM LogonTimings'
    type_name = 'session'
    namespace = 'root/citrix/profiles/metrics'

    # TODOK
