from .base import Base
import datetime
import time


class CheckSystemTime(Base):
    qry = 'SELECT * FROM Win32_UTCTime'
    type_name = 'system'

    def on_item(self, itm):
        remote_ts = datetime.datetime(
            itm['Year'], itm['Month'], itm['Day'], itm['Hour'],
            itm['Minute'], itm['Second'],
        ).timestamp()
        ts = time.time()
        diff = abs(remote_ts - ts)

        return {
            'name': 'system',
            'timeDifference': diff
        }
