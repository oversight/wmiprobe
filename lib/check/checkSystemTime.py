from .base import Base
import datetime
import time


class CheckSystemTime(Base):
    qry = 'SELECT Year, Month, Day, Hour, Minute, Second FROM Win32_UTCTime'
    type_name = 'system'

    @staticmethod
    def on_item(itm):
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
