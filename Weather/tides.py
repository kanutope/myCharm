import json
from datetime import datetime


class tides:
    def __init__(self, file=""):
        """ fetches tides from the json file 'file' """
        with open(file) as fp:
            data = json.load(fp)
            fp.close()
        
        _avg = 0
        _cnt = data['rows']
        _work = {}
        _srce = data['tides']
        for i in range(_cnt):
            tide = _srce[i]
            dt = datetime.fromisoformat(tide['Timestamp'])
            
            mon = dt.month
            day = dt.day
            tim = int(dt.timestamp())
            
            if mon not in _work:
                _work[mon] = {}
            if day not in _work[mon]:
                _work[mon][day] = {}
            
            _avg += tide['Value']
            _work[mon][day][tim] = tide['Value']
        
        _avg = round(_avg / _cnt, 2)
        
        self.tides = {}
        for mon in _work:
            for day in _work[mon]:
                srt = sorted(_work[mon][day])
                
                for tim in srt:
                    if mon not in self.tides:
                        self.tides[mon] = {}
                    if day not in self.tides[mon]:
                        self.tides[mon][day] = {}
                    _lvl = _work[mon][day][tim]
                    self.tides[mon][day][tim] = (_lvl, "L" if _lvl < _avg else "H")
    
    def get_tides(self, givendate=""):
        """ get list of tides for a given date passed in *isoformat* '2024-12-31'.
            If date is omitted, the current day is taken.
        """
        _date = datetime.today() if not givendate else datetime.fromisoformat(givendate)
        return self.tides[_date.month][_date.day]
    
    def get_low_times(self, givendate=""):
        """ get land yacht sailing time(s) for a given date in *isoformat* '2024-12-31'.
            Returns array of {'L': x, 'B': y, 'E': z}, where L is low tide time,
            B is begin and E is end of riding window.
            If date is omitted, the current day is taken.
        """
        _date = datetime.today() if not givendate else datetime.fromisoformat(givendate)
        
        ret = []
        _tides = self.tides[_date.month][_date.day]
        for _ts in _tides:
            _tid = _tides[_ts]
            if _tid[1] == "L":
                ret.append(_ts)
        
        return ret
