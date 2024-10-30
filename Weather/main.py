import time
from datetime import datetime, date
from tides import tides

HRS3 = 3 * 60 * 60  # 3 hours = 3 * 60' * 60"

calendar = tides("data/Nieuwpoort-waterlevels-2024.json")

_date = "2024-04-15"
curr = calendar.get_tides(_date)
print(curr)

ride = calendar.get_low_times(_date)

for _tim in ride:
    _beg = _tim - HRS3
    _end = _tim + HRS3
    print(f"{_date} LW om {datetime.fromtimestamp(_tim).strftime('%H:%M')}"
          f" - rijden van {datetime.fromtimestamp(_beg).strftime('%H:%M')}"
          f" tot {datetime.fromtimestamp(_end).strftime('%H:%M')}")

"""
# 2024-06-30T08:38:00.000+02:00
for i in (0, 700, 1400):
    print(tides[i]['Timestamp'])
    print(time.strptime(data['tides'][i]['Timestamp'][0:19], "%Y-%m-%dT%H:%M:%S"))
"""  # approximation
# idx = round((now - beg) / (beg - end))
# print (idx)
