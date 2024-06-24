import json
from datetime import datetime as dt


def epoch2str(epoch):
    return dt.fromtimestamp(epoch).isoformat(sep=' ')


WIND_DIR = ["N", "NNO", "NO", "ONO",
            "O", "OZO", "ZO", "ZZO",
            "Z", "ZZW", "ZW", "WZW",
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
    _result['wind_kph'] = round(_srce['wind_speed'] * 3.6, 1)
    _result['wind_degree'] = _srce['wind_deg']
    _idx = int(((_srce['wind_deg'] + 11.25) % 360) / 22.5)
    _result['wind_dir'] = WIND_DIR[_idx]
    _result['pressure_mb'] = _srce['pressure']
    
    _result['is_day'] = -1
    _result['gust_kph'] = -1
    _result['precip_mm'] = -1
    
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
        _wrk['wind_kph'] = round(_srce['wind_speed'] * 3.6, 1)
        _wrk['wind_degree'] = _srce['wind_deg']
        _idx = int(((_srce['wind_deg'] + 11.25) % 360) / 22.5)
        _wrk['wind_dir'] = WIND_DIR[_idx]
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
            _fcast['wind_kph'] = round(_srce['wind_speed'] * 3.6, 1)
            _fcast['wind_degree'] = _srce['wind_deg']
            _idx = int(((_srce['wind_deg'] + 11.25) % 360) / 22.5)
            _fcast['wind_dir'] = WIND_DIR[_idx]
            _fcast['gust_kph'] = round(_srce['wind_gust'] * 3.6, 1)
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
    
    for hour in rec['hourly']:
        time = hour['time']
        temp_c = hour['temp_c']
        wind_kph = hour['wind_kph']
        wind_degree = hour['wind_degree']
        wind_dir = hour['wind_dir']
        gust_kph = hour['gust_kph']
        pressure_mb = hour['pressure_mb']
        condition = hour['condition']
        print(f"{time}\tOWM\t{temp_c}°C\t{wind_kph}\tkm/h\t{wind_degree}°\t{wind_dir}\t{pressure_mb}\tmb\t{condition}")
