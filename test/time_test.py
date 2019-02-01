import pytz
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import time

## get timezone with timezone name
estern = pytz.timezone('America/New_York')
china = pytz.timezone('Asia/Hong_Kong')

## get timezone with offset
tz_n5 = timezone(timedelta(hours=-5))

## read millisecond as specific timezone
milli = 1544161706119
n = datetime.fromtimestamp(milli/1000, tz=china)
print(n)

## convert from one timezone to another
d = n.astimezone(estern)
print(d)
d = n.astimezone(tz_n5)
print(d)

## UTC now
print(datetime.utcnow())

## get now in second
print(time.time())

## format time
fmt = '%Y-%m-%d, %a %H:%M:%S.%f %Z'
# tm_str = datetime.now().strftime(fmt)
tm_str = n.strftime(fmt)
print(tm_str)

## Result
# 2018-12-07 13:48:26.119000+08:00
# 2018-12-07 00:48:26.119000-05:00
# 2018-12-07 00:48:26.119000-05:00
# 2018-12-07 06:10:37.715883
# 1544163037.7158835
# 2018-12-07, Fri 13:48:26.119000 HKT