"""
    Class definitions for managing the weather reports and forecast from OpenWeatherMap

    UNLICENSE:
    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.
"""

# SPDX-License-Identifier: Unlicense

import Weather.WeatherForecast as wf
from Weather.parseCommon import Coordinates, Current, Weather, Wind, WINDDIV, WINDDESC, WINDDIR, mps2knt, beaufort, \
    windDirection
import time as tm
from locale import str as lstr


class OWMP_OneCall:
    """ master structure containing the various onecall records."""

    def __init__(self, lat=-1, lon=-1, timezone="", timezone_offset=-99999,
                 current=None, minutely=None, daily=None
                 ):
        self.lat = lat                                        # Geographical coordinates of the location (latitude)
        self.lon = lon                                        # Geographical coordinates of the location (longitude)
        self.timezone = timezone                              # Timezone name for the requested location
        self.timezone_offset = timezone_offset                # Shift in seconds from UTC
        self.current = current                                # 'Current' object
        self.minutely = [] if minutely is None else minutely  # list of 'Minutely' object
        self.daily = [] if daily is None else daily           # list of 'Daily' object

    def __str__(self):
        return f"{Coordinates(self.lat, self.lon)}"

    @staticmethod
    def csvHeader():
        return "LAT;LON;"


"""
    Class definitions OWMP Forecast
"""


class OWMP_Forecast_city:
    """ master structure containing the various forecast records."""

    def __init__(self, cid=-1, name="", coord=None, country="", timezone_offset=-99999):
        self.cid = cid                          # City ID
        self.name = name                        # City name
        self.coord = coord                      # 'Coordinates' object
        self.country = country                  # Country code (GB, JP etc.)
        self.timezone_offset = timezone_offset  # Shift in seconds from UTC

    def __str__(self):
        return f"{self.name} [{self.country}] ({self.coord}) TZ={self.timezone_offset}"

    @staticmethod
    def csvHeader():
        return "CityName;LAT;LON;"

    def csv(self):
        return f"{self.name};{lstr(self.coord.lat)};{lstr(self.coord.lon)};"


class OWMP_Forecast_main:
    """ master structure containing the various forecast records."""

    def __init__(self, temp=-99.99, feels_like=-99.99, temp_min=-99.99, temp_max=-99.99,
                 pressure=-1, sea_level=-1, grnd_level=-1, humidity=-1
                 ):
        self.temp = temp              # Temperature. Unit Default: Kelvin, Metric: Celsius
        """ This temperature parameter accounts for the human perception of weather.
            Unit Default: Kelvin, Metric: Celsius"""
        self.feels_like = feels_like
        """ Minimum temperature at the moment of calculation. This is minimal forecasted temperature (within large
            megalopolises and urban areas), use this parameter optionally. Unit Default: Kelvin, Metric: Celsius"""
        self.temp_min = temp_min
        """ Maximum temperature at the moment of calculation. This is maximal forecasted temperature (within large
            megalopolises and urban areas), use this parameter optionally. Unit Default: Kelvin, Metric: Celsius"""
        self.temp_max = temp_max
        self.pressure = pressure      # Atmospheric pressure on the sea level by default, hPa
        self.sea_level = sea_level    # Atmospheric pressure on the sea level, hPa
        self.grnd_level = grnd_level  # Atmospheric pressure on the ground level, hPa
        self.humidity = humidity      # Humidity, %

    def __str__(self):
        return f"T: {self.temp} °C feels {self.feels_like} (min {self.temp_min}, max {self.temp_max}, " + \
               f"P: {self.pressure} hPa hum: {self.humidity} %"

    @staticmethod
    def csvHeader():
        return "Temp;Tfeel;Tmin;Tmax;Press;Hum.;"

    def csv(self):
        return f"{lstr(self.temp)};{lstr(self.feels_like)};{lstr(self.temp_min)};" + \
               f"{lstr(self.temp_max)};{lstr(self.pressure)};{lstr(self.humidity)};"


class OWMP_Forecast_member:
    def __init__(self, dt=-1, main=None, weather=None, clouds_all=-1, wind=None, visibility=-1,
                 pop=-1, rain_3h=-1, snow_3h=-1, pod="", dt_txt=""):
        self.dt = dt                  # Time of data forecasted, unix, UTC
        self.main = main              # 'Main' object
        self.weather = weather        # 'Weather' object
        self.clouds_all = clouds_all  # Cloudiness, %
        self.wind = wind              # 'Wind' object
        self.visibility = visibility  # Average visibility, metres
        self.pop = pop                # Probability of precipitation
        self.rain_3h = rain_3h        # Rain volume for last 3 hours, mm
        self.snow_3h = snow_3h        # Snow volume for last 3 hours
        self.pod = pod                # Part of the day (n - night, d - day)
        self.dt_txt = dt_txt          # Time of data forecasted, ISO, UTC

    def __str__(self):
        return f"{self.dt_txt}\n{self.weather[0]}\n{self.main}"

    @staticmethod
    def csvHeader():
        return "DT;DTtxt;" + OWMP_Forecast_main.csvHeader() + Weather.csvHeader() + Wind.cvsHeader()

    def csv(self):
        return f"{self.dt};{self.dt_txt};" + self.main.csv() + self.weather[0].csv() + self.wind.csv()


class OWMP_Forecast:
    """ master structure containing the various forecast records."""

    def __init__(self, cnt=-1, llst=None, city=None):
        self.cnt = cnt                             # number of timestamps returned in the API response
        self.llst = [] if llst is None else llst   # list of 'OWMP_Forecast_member' objects
        self.city = city                           # 'OWMP_Forecast_city' object

    def __str__(self):
        __lstr = ""
        for mmbr in self.llst:
            __lstr = __lstr + f"{mmbr}\n"

        return f"{__lstr} {self.city}"

    @staticmethod
    def csvHeader():
        return OWMP_Forecast_city.csvHeader() + OWMP_Forecast_member.csvHeader()

    def csv(self):
        __lstr = ""
        for mmbr in self.llst:
            __lstr = __lstr + self.city.csv() + mmbr.csv() + "\n"

        return __lstr


def j2o_OWMP_weather(llst):
    """ JSON to Object mapping - OWMP_forecast_weather """

    tgt = []
    for mbmr in llst:
        tgt.append(Weather(wid=mbmr['id'], main=mbmr['main'], descr=mbmr['description'], icon=mbmr['icon']))
    return tgt


def j2o_OWMP_forecast_wind(data):
    """ JSON to Object mapping - OWMP_forecast_wind """

    obj = Wind(speed=data['speed'], speedUnit='m/sec', degrees=data['deg'],
               direction=windDirection(data['deg']), gust=data['gust']
               )
    return obj


def j2o_OWMP_forecast_city(data):
    """ JSON to Object mapping - OWMP_forecast_city """

    obj = OWMP_Forecast_city(cid=data['id'], name=data['name'],
                             coord=Coordinates(data['coord']['lat'], data['coord']['lon']),
                             country=data['country'], timezone_offset=data['timezone'])
    return obj


def j2o_OWMP_forecast_main(data):
    """ JSON to Object mapping - OWMP_forecast_main """

    obj = OWMP_Forecast_main(temp=data['temp'], feels_like=data['feels_like'], temp_min=data['temp_min'],
                             temp_max=data['temp_max'], pressure=data['pressure'], sea_level=data['sea_level'],
                             grnd_level=data['grnd_level'], humidity=data['humidity']
                             )

    return obj


def j2o_OWMP_forecast_list(llst):
    """ JSON to Object mapping - OWMP_forecast_list """

    tgt = []
    for mbmr in llst:
        tgt.append(OWMP_Forecast_member(dt=mbmr['dt'], clouds_all=mbmr['clouds']['all'], visibility=mbmr['visibility'],
                                        pop=mbmr['pop'], rain_3h=mbmr['rain']['3h'] if 'rain' in mbmr else -1,
                                        snow_3h=mbmr['snow']['3h'] if 'snow' in mbmr else -1, pod=mbmr['sys']['pod'],
                                        dt_txt=mbmr['dt_txt'], main=j2o_OWMP_forecast_main(mbmr['main']),
                                        weather=j2o_OWMP_weather(mbmr['weather']),
                                        wind=j2o_OWMP_forecast_wind(mbmr['wind'])
                                        )
                   )

    return tgt


def j2o_OWMP_forecast(data):
    """ JSON to Object mapping - OWMP_forecast """

    obj = OWMP_Forecast(cnt=data['cnt'], llst=j2o_OWMP_forecast_list(data['list']),
                        city=j2o_OWMP_forecast_city(data['city'])
                        )

    return obj


"""
    JSON to Object mapping - OWMP_onecall
"""


def j2o_OWMP_onecall_current(data):
    """ JSON to Object mapping - OWMP_onecall """

    obj = Current(dt=data['dt'], sunrise=data['sunrise'], sunset=data['sunset'], temp=data['temp'],
                  feels_like=data['feels_like'], pressure=data['pressure'], humidity=data['humidity'],
                  dew_point=data['dew_point'], clouds=data['clouds'], uvi=data['uvi'], visibility=data['visibility'],
                  wind_speed=data['wind_speed'], wind_gust=data['wind_gust'] if 'wind_gust' in data else -1,
                  wind_deg=data['wind_deg'],
                  rain=data['rain'] if 'rain' in data else None, snow=data['snow'] if 'snow' in data else None,
                  weather=j2o_OWMP_weather(data['weather']))

    return obj


def j2o_OWMP_onecall(data):
    """ JSON to Object mapping - OWMP_onecall """

    obj = OWMP_OneCall(lat=data['lat'], lon=data['lon'], timezone=data['timezone'],
                       timezone_offset=data['timezone_offseet'],
                       current=j2o_OWMP_onecall_current(data['current'])
                       )
    """
        ,
        minutely=None,
        daily=None)
    """

    return obj


"""
    Output
"""


def csv_OWMP_forecast(loc=""):
    """ transform forecast outputfile to csv """

    print(OWMP_Forecast.csvHeader())
    for fil in wf.getLatest(loc, 'OWMP', 'forecast'):
        fc = j2o_OWMP_forecast(wf.fetchFile(wf.getOutputDir() + '/' + fil))
        print(fc.csv())


def csv_OWMP_onecall(loc=""):
    """ transform forecast outputfile to csv """

    print(OWMP_OneCall.csvHeader())
    for fil in wf.getLatest(loc, 'OWMP', 'onecall'):
        fc = j2o_OWMP_onecall(wf.fetchFile(wf.getOutputDir() + '/' + fil))
        print(fc.csv())


def print_OWMP_forecast(loc=""):
    for fil in wf.getLatest(loc, 'OWMP', 'forecast'):
        data = wf.fetchFile(wf.getOutputDir() + '/' + fil)

        for rec in data['list']:
            main = rec['main']
            wthr = rec['weather']
            wind = rec['wind']

            indx = int(((wind['deg'] + WINDDIV / 2.0) % 360) / WINDDIV)
            knts = mps2knt(wind['speed'])
            bft = beaufort(knts)

            time = tm.strftime("%a %d %b %H:%M", tm.localtime(rec['dt']))
            out = f"{time}|{wthr[0]['description']}|T:{main['temp']:5.1f} feel {main['feels_like']:5.1f}" \
                  f" [{main['temp_min']:5.1f} ~{main['temp_max']:5.1f}]" \
                  f"|P: {main['pressure']:4d}hPa" \
                  f"|W: {knts:2.0f}kn {bft:2d}bft {WINDDIR[indx]:^3s} {WINDDESC[bft]:s}"

            print(out)
