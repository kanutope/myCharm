import json


def get_header(record: dict):
    _result = {}
    _loc = record['location']
    for _idx in ('name', 'country', 'lat', 'lon', 'tz_id'):
        _result[_idx] = _loc[_idx]
    
    return _result


def get_current(record: dict):
    _result = {}
    _loc = record['current']
    for _idx in ('last_updated', 'temp_c', 'is_day', 'wind_kph', 'wind_degree', 'wind_dir', 'gust_kph', 'pressure_mb',
                 'precip_mm'):
        _result[_idx] = _loc[_idx]
    
    return _result


def get_forecast(record: dict):
    _result = []
    # loop over the day records (3)
    for _srce in record['forecast']['forecastday']:
        _dest = dict({})
        _dest['header'] = dict({})
        
        # fetch header data
        _wrk = _dest['header']
        _wrk['date'] = _srce['date']
        # fetch meteo data for that day
        for _idx in ('maxtemp_c', 'mintemp_c', 'avgtemp_c', 'maxwind_kph', 'totalprecip_mm',
                     'totalsnow_cm', 'daily_will_it_rain', 'daily_chance_of_rain', 'daily_will_it_snow',
                     'daily_chance_of_snow'):
            _wrk[_idx] = _srce['day'][_idx]
        # fetch astro data for that day
        for _idx in ('sunrise', 'sunset', 'moon_phase'):
            _wrk[_idx] = _srce['astro'][_idx]
        
        _dest['hourly'] = []
        _wrk = _dest['hourly']
        # loop hourly data for that day
        for _hourly in _srce['hour']:
            _fcast = dict({})
            for _idx in ('time', 'temp_c', 'is_day', 'wind_kph', 'wind_degree', 'wind_dir', 'gust_kph', 'pressure_mb',
                         'precip_mm', 'snow_cm', 'will_it_rain', 'chance_of_rain', 'will_it_snow', 'chance_of_snow'):
                _fcast[_idx] = _hourly[_idx]
            _fcast['condition'] = _hourly['condition']['text']
            _wrk.append(_fcast)

        _result.append(_dest)
        
    return _result


with open("query/weatherapi-forecast.json") as fp:
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
        print(f"{time}\tWAPI\t{temp_c}°C\t{wind_kph}\tkm/h\t{wind_degree}°\t{wind_dir}\t{pressure_mb}\tmb\t{condition}")
    