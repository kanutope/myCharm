import json
from datetime import datetime

with open("data/Nieuwpoort-waterlevels-2024.json") as fp:
    data = json.load(fp)
    fp.close()

_work = {}
tides = data['tides']
for i in range(data['rows']):
    tide = tides[i]
    dt = datetime.fromisoformat(tide['Timestamp'])
    
    mon = dt.month
    day = dt.day
    tim = int(dt.timestamp())
    
    if mon not in _work:
        _work[mon] = {}
    if day not in _work[mon]:
        _work[mon][day] = {}
    
    _work[mon][day][tim] = tide['Value']
    
levels = {}
for mon in _work:
    for day in _work[mon]:
        srt = sorted(_work[mon][day])
        
        for tim in srt:
            if mon not in levels:
                levels[mon] = {}
            if day not in levels[mon]:
                levels[mon][day] = {}
            levels[mon][day][tim] = _work[mon][day][tim]
        
print(levels)

now = datetime.now()

"""
# 2024-06-30T08:38:00.000+02:00
for i in (0, 700, 1400):
    print(tides[i]['Timestamp'])
    print(time.strptime(data['tides'][i]['Timestamp'][0:19], "%Y-%m-%dT%H:%M:%S"))
"""
# approximation
# idx = round((now - beg) / (beg - end))
# print (idx)
