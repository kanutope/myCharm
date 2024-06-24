"""
    Class definitions for managing the ACCUweather.com API's response

    UNLICENSE:
    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.
"""

# SPDX-License-Identifier: Unlicense


import Weather.WeatherForecast as wf

"""
    Class definitions ACCUweather Daily report
"""


class ACCUtransition(wf.Transition):
    def __init__(self, trans):
        super().__init__()
        self.age = -1
        self.phase = ""
        self.riseEpoch = trans['EpochRise']
        self.setEpoch = trans['EpochSet']

        if 'Phase' in list(trans):
            self.phase = trans['Phase']
        if 'Age' in list(trans):
            self.age = trans['Age']


class ACCUwind(wf.wind):
    def __init__(self, wind):
        self.speed = wind['Speed']['Value']
        self.speedUnit = wind['Speed']['Unit']
        self.degrees = wind['Direction']['Degrees']
        self.direction = wind['Direction']['Localized']


class ACCUprecipitation(wf.Precipitation):
    def __init__(self, daynight):
        super().__init__()
        self.probability = daynight['PrecipitationProbability']
        self.type = daynight['PrecipitationType']
        self.intensity = daynight['PrecipitationIntensity']
        self.phrase = daynight['ShortPhrase']
        self.probThunderstorm = daynight['ThunderstormProbability']
        self.probRain = daynight['RainProbability']
        self.probSnow = daynight['SnowProbability']
        self.probIce = daynight['IceProbability']
        self.hours = daynight['HoursOfPrecipitation']
        self.hrsRain = daynight['HoursOfRain']
        self.hrsSnow = daynight['HoursOfSnow']
        self.hrsIce = daynight['HoursOfIce']


class ACCUdaynightfcast(wf.Daynightfcast):
    def __init__(self, daynight):
        super().__init__()
        self.phrase = daynight['IconPhrase']
        if daynight['HasPrecipitation']:
            self.precipitation = ACCUprecipitation(daynight)
        else:
            self.precipitation = None

        self.wind = ACCUwind(daynight['Wind'])
        self.gust = ACCUwind(daynight['WindGust'])
        self.cloudCover = daynight['CloudCover']


class ACCUdailyForecast(wf.Forecast):
    """ __init__()
        ----------
    """
    def __init__(self, fc):
        super().__init__()
        self.forecastEpoch = fc['EpochDate']
        self.sun = ACCUtransition(fc['Sun'])
        self.moon = ACCUtransition(fc['Moon'])
        self.temperatures = {
            'Unit': fc['Temperature']['Minimum']['Unit'],
            'Temp': {
                'Min': fc['Temperature']['Minimum']['Value'],
                'Max': fc['Temperature']['Maximum']['Value']
            },
            'Feel': {
                'Min': fc['RealFeelTemperature']['Minimum']['Value'],
                'Max': fc['RealFeelTemperature']['Maximum']['Value']
            },
            'Shade': {
                'Min': fc['RealFeelTemperatureShade']['Minimum']['Value'],
                'Max': fc['RealFeelTemperatureShade']['Maximum']['Value']
            }
        }
        self.sunHours = fc['HoursOfSun']
        self.day = ACCUdaynightfcast(fc['Day'])
        self.night = ACCUdaynightfcast(fc['Night'])


class ACCUdaily(wf.Report):
    """ __init__()
        ----------
    """
    def __init__(self, report):
        super().__init__()
        self.effectiveEpoch = report['Headline']['EffectiveEpochDate']
        self.forecasts = []
        for fc in report['DailyForecasts']:
            self.forecasts.append(ACCUdailyForecast(fc))

    @staticmethod
    def setClass():
        wf.setClass('ACCU', 'daily', ACCUdaily)


"""
    Class definitions ACCUweather Daily report
"""


class ACCUhourlyForecast(wf.Forecast):
    """ __init__()
        ----------
    """
    def __init__(self, fc):
        super().__init__()
        self.forecastEpoch = fc['EpochDateTime']
        self.phrase = fc['IconPhrase']
        self.isDayLight = fc['IsDaylight']
        self.temperatures = {
            'Unit': fc['Temperature']['Unit'],
            'Temp': {
                'Val': fc['Temperature']['Value']
            },
            'Feel': {
                'Val': fc['RealFeelTemperature']['Value']
            }
        }
        self.sunHours = fc['HoursOfSun']
        self.day = ACCUdaynightfcast(fc['Day'])
        self.night = ACCUdaynightfcast(fc['Night'])


def initACCU():
    ACCUdaily.setClass()
    return
