import json
from datetime import datetime


def epoch2str(epoch):
    return datetime.fromtimestamp(epoch).isoformat(sep=' ')


NM = 1.852
SRCE = "OWM"
WIND_DIR = ["N", "NNE", "NE", "ENE",
            "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW",
            "W", "WNW", "NW", "NNW"]


def get_header(record: dict):
    _result = {}
    _loc = record
    _result['name'] = ""
    _result['country'] = ""
    for _idx in ('lat', 'lon', 'timezone'):
        _result[_idx] = _loc[_idx]
    
    return _result


def get_current(record: dict):
    _result = {}
    _srce = record['current']
    _result['last_updated'] = epoch2str(_srce['dt'])
    _result['temp_c'] = _srce['temp']
    _result['wind_ms'] = _srce['wind_speed']
    _result['wind_kph'] = round(_result['wind_ms'] * 3.6, 1)
    _result['wind_kt'] = round(_result['wind_kph'] / NM, 1)
    _result['wind_degree'] = _srce['wind_deg']
    _idx = int(((_srce['wind_deg'] + 11.25) % 360) / 22.5)
    _result['wind_dir'] = WIND_DIR[_idx]
    _result['pressure_mb'] = _srce['pressure']
    
    _result['is_day'] = -999
    _result['precip_mm'] = -999
    
    return _result


def get_forecast(record: dict):
    _result = []
    """
    
    """
    # loop over the day records (2)
    for _day in range(2):
        _srce = record['daily'][_day]
        
        _dest = dict({})
        _dest['header'] = dict({})
        
        # fetch header data
        _wrk = _dest['header']
        _wrk['date'] = epoch2str(_srce['dt']).replace(" .*", "")
        # fetch meteo data for that day
        _wrk['moon_phase'] = _srce['moon_phase']
        _wrk['wind_ms'] = _srce['wind_speed']
        _wrk['wind_kph'] = round(_wrk['wind_ms'] * 3.6, 1)
        _wrk['wind_kt'] = round(_wrk['wind_kph'] / NM, 1)
        _wrk['wind_degree'] = _srce['wind_deg']
        _idx = int(((_srce['wind_deg'] + 11.25) % 360) / 22.5)
        _wrk['wind_dir'] = WIND_DIR[_idx]
        _wrk['gust_ms'] = _srce['wind_gust']
        _wrk['gust_kph'] = round(_wrk['gust_ms'] * 3.6, 1)
        _wrk['gust_kt'] = round(_wrk['gust_kph'] / NM, 1)
        _wrk['pressure_mb'] = _srce['pressure']
        _wrk['condition'] = _srce['weather'][0]['description']
        
        # fetch astro data for that day
        for _idx in ('sunrise', 'sunset'):
            _wrk[_idx] = epoch2str(_srce[_idx])
        
        _dest['hourly'] = []
        _wrk = _dest['hourly']
        # loop hourly data for that day
        for _hour in range(24):
            _fcast = dict({})
            _srce = record['hourly'][_day * 24 + _hour]
            
            _fcast['temp_c'] = -99
            _fcast['time'] = epoch2str(_srce['dt'])
            _fcast['wind_ms'] = _srce['wind_speed']
            _fcast['wind_kph'] = round(_fcast['wind_ms'] * 3.6, 1)
            _fcast['wind_kt'] = round(_fcast['wind_kph'] / NM, 1)
            _fcast['wind_degree'] = _srce['wind_deg']
            _idx = int(((_srce['wind_deg'] + 11.25) % 360) / 22.5)
            _fcast['wind_dir'] = WIND_DIR[_idx]
            _fcast['gust_ms'] = _srce['wind_gust']
            _fcast['gust_kph'] = round(_fcast['gust_ms'] * 3.6, 1)
            _fcast['gust_kt'] = round(_fcast['gust_kph'] / NM, 1)
            _fcast['pressure_mb'] = _srce['pressure']
            _fcast['condition'] = _srce['weather'][0]['description']
            
            _wrk.append(_fcast)

        _result.append(_dest)
        
    return _result


with open("query/openweather-onecall.json") as fp:
    data = json.load(fp)
    fp.close()

header = get_header(data)
current = get_current(data)
forecast = get_forecast(data)

print(header)
print(current)
for rec in forecast:
    print(rec['header'])
    
    print(f"time\tsrce\t°C\tm/s\tkt\tkm/h\t°\tdir\tm/s\tkt\tkm/h\tmb\tcondities")
    for hour in rec['hourly']:
        time = hour['time']
        temp_c = hour['temp_c']
        wind_kph = hour['wind_kph']
        wind_kt = hour['wind_kt']
        wind_ms = hour['wind_ms']
        wind_degree = hour['wind_degree']
        wind_dir = hour['wind_dir']
        gust_kph = hour['gust_kph']
        gust_kt = hour['gust_kt']
        gust_ms = hour['gust_ms']
        pressure_mb = hour['pressure_mb']
        condition = hour['condition']
        print(f"{time}\t{SRCE}\t{temp_c}\t{wind_ms}\t{wind_kt}\t{wind_kph}\t{wind_degree}\t{wind_dir}\t{gust_ms}"
              f"\t{gust_kt}\t{gust_kph}\t{pressure_mb}\t{condition}")

    print("<table>")
    print("</tr><td>hour</td>")
    for hour in rec['hourly'][0:11]:
        tim = datetime.fromisoformat(hour['time']).timetuple()
        print(f"<td>{tim[3]:02}</td>")
        
    print("<//tr></tr><td>wind</td>")
    for hour in rec['hourly'][0:11]:
        wdir = hour['wind_dir']
        i = WIND_DIR.index(wdir)
        nam = f"{i:02} {wdir}.png"
        print(f"<td><img src=\"icons/compass B/{nam}\" style=\"width:30px;height:30px;\"></td>")
    
    print("<//tr></tr><td>wind m/s</td>")
    for hour in rec['hourly'][0:11]:
        print(f"<td>{hour['wind_ms']:.1f}</td>")
    
    print("<//tr></tr><td>vlaag m/s</td>")
    for hour in rec['hourly'][0:11]:
        print(f"<td>{hour['gust_ms']:.1f}</td>")
    print("<//tr></table>")
        
    
    
        
    
