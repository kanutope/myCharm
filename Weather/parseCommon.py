"""
    Generic, common class definitions for managing the weather reports and forecast from the various providers

    UNLICENSE:
    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.
"""

# SPDX-License-Identifier: Unlicense

from locale import setlocale, LC_NUMERIC, str as lstr
setlocale(LC_NUMERIC, 'nl_BE.ISO8859-1')


""" Public functions accessing __APIconfig """


def setClass(prov, rep, repClass):
    __APIconfig.config[prov]['reports'][rep]['class'] = repClass


def getClass(prov, rep):
    return __APIconfig.config[prov]['reports'][rep]['class']


""" Data record (class) definitions """


class Coordinates:
    def __init__(self, lat=-99.99, lon=-99.99):
        self.lat = lat  # City geo location, latitude
        self.lon = lon  # City geo location, longitude

    def __str__(self):
        return f"{abs(self.lat)} {'N' if self.lat > 0 else 'S'}  {abs(self.lon)} {'E' if self.lon > 0 else 'W'}"


class Weather:
    """ Weather condition """

    def __init__(self, wid=-1, main="", descr="", icon=""):
        self.wid = wid      # Weather condition 'id'
        self.main = main    # Group of weather parameters ('Rain', 'Snow', 'Extreme' etc.)
        self.descr = descr  # Weather condition within the group
        self.icon = icon    # Weather icon id. How to get: http://openweathermap.org/img/wn/10d@2x.png

    def __str__(self):
        return f"{self.main} - {self.descr}"

    @staticmethod
    def csvHeader():
        return "Wgroup;Wdescr;"

    def csv(self):
        return f"{self.main};{self.descr};"


class Temperature:
    def __init__(self, morn=-99.99, day=-99.99, eve=-99.99, night=-99.99, minT=-99.99, maxT=-99.99):
        self.morn = morn    # Morning temperature.
        self.day = day      # Day temperature.
        self.eve = eve      # Evening temperature.
        self.night = night  # Night temperature.
        self.minT = minT    # Min daily temperature.
        self.maxT = maxT    # Max daily temperature.


class Current:
    """ current Current weather data API response."""

    def __init__(self, dt=-1, sunrise=-1, sunset=-1, temp=-99.99, feels_like=-99.99, pressure=-1, humidity=-1,
                 dew_point=-99.99, clouds=-1, uvi=-1, visibility=-1, wind_speed=-1, wind_gust=-1, wind_deg=-1,
                 rain=None, snow=None, weather=None
                 ):
        self.dt = dt                 # Current time, Unix, UTC
        self.sunrise = sunrise       # Sunrise time, Unix, UTC
        self.sunset = sunset         # Sunset time, Unix, UTC
        self.temp = temp             # Temperature. Units - default: kelvin, metric: Celsius
        """ Temperature. This temperature parameter accounts for the human perception of weather.
            Units – default: kelvin, metric: Celsius."""
        self.feels_like = feels_like
        self.pressure = pressure      # Atmospheric pressure on the sea level, hPa
        self.humidity = humidity      # Humidity, %
        """ Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to
            condense and dew can form. Units – default: kelvin, metric: Celsius"""
        self.dew_point = dew_point
        self.clouds = clouds          # Cloudiness, %
        self.uvi = uvi                # Current UV index
        self.visibility = visibility  # Average visibility, metres
        self.wind_speed = wind_speed  # Wind speed. Wind speed. Units – default: metre/sec, metric: metre/sec
        self.wind_gust = wind_gust    # (where available) Wind gust. Units – default: metre/sec, metric: metre/sec
        self.wind_deg = wind_deg      # Wind direction, degrees (meteorological)
        
        if rain is None:
            self.rain = {}
        else:
            self.rain = rain          # current.rain.1h (where available) Rain volume for last hour, mm

        if snow is None:
            self.snow = {}
        else:
            self.snow = snow           # current.snow.1h (where available) Snow volume for last hour, mm

        if weather is None:
            self.weather = []
        else:
            self.weather = weather     # list of 'Weather' object - Weather condition


class Minutely:
    """ minutely Minute forecast weather data API response. """
    def __init__(self, dt=-1, precipitation=-1):
        self.dt = dt                        # Time of the forecasted data, unix, UTC
        self.precipitation = precipitation  # Precipitation volume, mm


class Hourly:
    """ hourly Hourly forecast weather data API response"""

    def __init__(self, dt=-1, temp=-99.99, feels_like=-99.99, pressure=-1, humidity=-1, dew_point=-99.99,
                 uvi=-1, clouds=-1, visibility=-1, wind_speed=-1, wind_gust=-1, wind_deg=-1, pop=-1,
                 rain=None, snow=None, weather=None
                 ):
        self.dt = dt          # Time of the forecasted data, Unix, UTC
        self.temp = temp    # Temperature. Units – default: kelvin, metric: Celsius
        """ Temperature. This accounts for the human perception of weather. Units – default: kelvin, metric: Celsius."""
        self.feels_like = feels_like
        self.pressure = pressure    # Atmospheric pressure on the sea level, hPa
        self.humidity = humidity    # Humidity, %
        """ Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to
            condense and dew can form. Units – default: kelvin, metric: Celsius."""
        self.dew_point = dew_point
        self.uvi = uvi                # UV index
        self.clouds = clouds          # Cloudiness, %
        self.visibility = visibility  # Average visibility, metres
        self.wind_speed = wind_speed  # Wind speed. Units – default: metre/sec, metric: metre/sec
        self.wind_gust = wind_gust    # (where available) Wind gust. Units – default: metre/sec, metric: metre/sec
        self.wind_deg = wind_deg      # Wind direction, degrees (meteorological)
        self.pop = pop                # Probability of precipitation
        if rain is None:
            self.rain = {}
        else:
            self.rain = rain          # hourly.rain.1h (where available) Rain volume for last hour, mm

        if snow is None:
            self.snow = {}
        else:
            self.snow = snow          # hourly.snow.1h (where available) Snow volume for last hour, mm

        if weather is None:
            self.weather = []
        else:
            self.weather = weather    # list of 'Weather' object - Weather condition


class Daily:
    """ daily Daily forecast weather data API response """

    def __init__(self, dt=-1, sunrise=-1, sunset=-1, moonrise=-1, moonset=-1, moon_phase=-1,
                 temp=Temperature, feels_like=Temperature, pressure=-1, humidity=-1, dew_point=-99.99,
                 wind_speed=-1, wind_gust=-1, wind_deg=-1, clouds=-1, uvi=-1, pop=-1, rain=-1, snow=-1,
                 weather=None
                 ):
        self.dt = dt                  # Time of the forecasted data, Unix, UTC
        self.sunrise = sunrise        # Sunrise time, Unix, UTC
        self.sunset = sunset          # Sunset time, Unix, UTC
        self.moonrise = moonrise      # The time of when the moon rises for this day, Unix, UTC
        self.moonset = moonset        # The time of when the moon sets for this day, Unix, UTC
        """" Moon phase. 0 and 1 are 'new moon', 0.25 is 'first quarter moon', 0.5 is 'full moon' and 0.75 is
            'last quarter moon'. The periods in between are called 'waxing crescent', 'waxing gibous', 'waning gibous'
            and 'waning crescent', respectively."""
        self.moon_phase = moon_phase
        self.temp = temp              # Units – default: kelvin, metric: Celsius
        self.feels_like = feels_like  # This accounts for the human perception of weather.
        self.pressure = pressure      # Atmospheric pressure on the sea level, hPa
        self.humidity = humidity      # Humidity, %
        """ Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to
            condense and dew can form. Units – default: kelvin, metric: Celsius."""
        self.dew_point = dew_point
        self.wind_speed = wind_speed  # Wind speed. Units – default: metre/sec, metric: metre/sec.
        self.wind_gust = wind_gust    # (where available) Wind gust.
        self.wind_deg = wind_deg      # Wind direction, degrees (meteorological)
        self.clouds = clouds          # Cloudiness, %
        self.uvi = uvi                # The maximum value of UV index for the day
        self.pop = pop                # Probability of precipitation
        self.rain = rain              # (where available) Precipitation volume, mm
        self.snow = snow              # (where available) Snow volume, mm
        if weather is None:
            self.weather = []
        else:
            self.weather = weather    # list of 'Weather' object - Weather condition


class Alert:
    """ alerts National weather alerts data from major national weather warning systems"""

    def __init__(self, sender_name="", event="", start=-1, end=-1, descr="", tags=""
                 ):
        self.sender_name = sender_name  # Name of the alert source. Please read here the full list of alert sources
        self.event = event              # Alert event name
        self.start = start              # Date and time of the start of the alert, Unix, UTC
        self.end = end                  # Date and time of the end of the alert, Unix, UTC
        self.descr = descr              # Description of the alert
        self.tags = tags                # Type of severe weather


'''
    super classes created previously on the basis of AccuWeather data.
    Superceeded or replaced by OpenWeatherMap data.
'''


class ReportACCU:
    def __init__(self):
        self.effectiveEpoch = -1
        self.forecasts = []

    def __str__(self):
        ret = f"EffectiveDate = {epoch2str(self.effectiveEpoch)} - "
        for fc in self.forecasts:
            ret = f"{ret}\n  {str(fc)}"
        return ret


class Precipitation:
    def __init__(self):
        self.probability = -1
        self.type = ""
        self.intensity = ""
        self.phrase = ""
        self.probThunder = -1
        self.probRain = -1
        self.probSnow = -1
        self.probIce = -1
        self.hours = -1
        self.hrsRain = -1
        self.hrsSnow = -1
        self.hrsIce = -1

    def __str__(self):
        ret = f"Neerslag - prob.:{self.probability:d} intens.:{self.intensity} type:{self.type}" \
              f" descr:\'{self.phrase}\'" \
              f" rain:{self.probRain} thunder:{self.probThunder} snow:{self.probSnow} ice:{self.probIce}"
        return ret


class Wind:
    def __init__(self, speed=-1, speedUnit="", degrees=-1, direction="", gust=-1):
        self.speed = speed          # Wind speed. Unit Default: meter/sec, Metric: meter/sec
        self.speedUnit = speedUnit  # actual unit
        self.degrees = degrees      # Wind direction, degrees (meteorological)
        self.direction = direction  # textual wind direction
        self.gust = gust            # (where available) Wind gust. Units – default: metre/sec, metric: metre/sec

    def __str__(self):
        ret = f"Speed={self.speed} {self.speedUnit} {self.direction}"
        return ret

    @staticmethod
    def cvsHeader():
        return "Wind m/s;Wind knts;Bft;WindAngle;WindDir;"

    def csv(self):
        knts = mps2knt(self.speed)
        return f"{lstr(self.speed)};{lstr(knts)};{beaufort(knts)};{self.degrees};{self.direction};"


class Daynightfcast:
    def __init__(self):
        self.phrase = ""
        self.precipitation = None
        self.wind = None
        self.gust = None
        self.cloudCover = -1

    def __str__(self):
        ret = f"\'{self.phrase:<18s}\' - {'Geen neerslag' if self.precipitation is None else str(self.precipitation)}" \
              f"\n           Wind: {str(self.wind)}    Rukwind: {str(self.gust)}"
        return ret


class Forecast:
    def __init__(self):
        self.forecastEpoch = -1
        self.phrase = ""
        self.isDayLight = False
        self.temperatures = {}
        self.sun = None
        self.moon = None
        self.sunHours = -1
        self.day = None
        self.night = None

    def __str__(self):
        temperatures = self.temperatures
        unit = temperatures['Unit']
        temp = temperatures['Temp']
        feel = temperatures['Feel']
        shade = temperatures['Shade']

        ret = f"forecast {epoch2str(self.ForecastEpoch)} - " \
              f"Zon: {str(self.Sun)} - Maan: {str(self.Moon)}\n" \
              f"    Zon: {self.SunHours:.1f}hrs Temp. min:{temp['Min']:5.1f}{unit} max:{temp['Max']:5.1f}{unit}" \
              f"    gevoels min:{feel['Min']:5.1f}{unit} max:{feel['Max']:5.1f}{unit}" \
              f"    schaduw min:{shade['Min']:5.1f}{unit} max:{shade['Max']:5.1f}{unit}\n" \
              f"    Dag:   {str(self.Day)}\n" \
              f"    Nacht: {str(self.Night)}"
        return ret


class Transition:
    def __init__(self):
        self.RiseEpoch = -1
        self.SetEpoch = -1
        self.Phase = ""
        self.Age = -1

    def __str__(self):
        Rise = int(self.RiseEpoch / (3600 * 24))
        Set = int(self.SetEpoch / (3600 * 24))

        ret = f"[rise {epoch2time(self.RiseEpoch)}  set    {epoch2time(self.SetEpoch)}]" \
            if Rise == Set else \
            f"[rise {epoch2time(self.SetEpoch)}  set +1 {epoch2time(self.RiseEpoch)}]"

        if self.Age > -1:
            ret = f"{ret} - Phase:{self.Phase:14s}  Age:{self.Age}"
        return ret


""" Some static (constant) variables """


WINDDIV = 360 / 16.0
WINDBFT = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 999]
WINDDIR = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
WINDDESC = ['Windstil', "Zwakke wind", "Zwakke wind", "Matige wind", "Matige wind", "Vrij krachtige wind"
            "Krachtige wind", "Harde wind", "Stormachtige wind", 'Storm', "Zware storm", "Zeer zware storm", 'Orkaan']


""" Public functions """


def mps2knt(spd):
    return (spd * 3600 / 1852)


def beaufort(spd):
    i = 0
    while spd > WINDBFT[i]:
        i = i + 1

    return i


def windDirection(deg):
    return WINDDIR[int(((deg + WINDDIV / 2.0) % 360) / WINDDIV)]
