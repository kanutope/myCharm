"""
    Class definitions for managing the ACCUweather.com API's response

"""
"""
UNLICENSE:
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.
"""

# SPDX-License-Identifier: Unlicense

"""
import json                             # noqa
import os                               # noqa
import re                               # noqa

import requests                         # noqa
import time as tm                       # noqa
from datetime import datetime as dt     # noqa
"""

import Weather.WeatherForecast as wf

"""
    Class definitions
"""


class ACCUtransition_class(wf.Transition_super):
    def __init__(self, trans):
        super().__init__()
        self.Age = -1
        self.Phase = ""
        self.RiseEpoch = trans["EpochRise"]
        self.SetEpoch = trans["EpochSet"]
        
        if "Phase" in list(trans):
            self.Phase = trans["Phase"]
        if "Age" in list(trans):
            self.Age = trans["Age"]


class ACCUprecipitation_class(wf.Precipitation_super):
    def __init__(self, daynight):
        super().__init__()
        self.Probability = daynight["PrecipitationProbability"]
        self.Type = daynight["PrecipitationType"]
        self.Intensity = daynight["PrecipitationIntensity"]
        self.Phrase = daynight["ShortPhrase"]
        self.ProbThunderstorm = daynight["ThunderstormProbability"]
        self.ProbRain = daynight["RainProbability"]
        self.ProbSnow = daynight["SnowProbability"]
        self.ProbIce = daynight["IceProbability"]
        self.Hours = daynight["HoursOfPrecipitation"]
        self.HrsRain = daynight["HoursOfRain"]
        self.HrsSnow = daynight["HoursOfSnow"]
        self.HrsIce = daynight["HoursOfIce"]


class ACCUdaynightfcast_class(wf.Daynightfcast_super):
    def __init__(self, daynight):
        super().__init__()
        self.Phrase = daynight["IconPhrase"]
        if daynight["HasPrecipitation"]:
            self.Precipitation = ACCUprecipitation_class(daynight)
        else:
            self.Precipitation = None

        self.Wind = None
        self.Gust = None
        self.CloudCover = -1


class ACCUdailyForecast_class(wf.Forecast_super):
    """ __init__()
        ----------
    """
    def __init__(self, fc):
        super().__init__()
        self.ForecastEpoch = fc["EpochDate"]
        self.Sun = ACCUtransition_class(fc["Sun"])
        self.Moon = ACCUtransition_class(fc["Moon"])
        self.temperatures = {
            "Unit": fc["Temperature"]["Minimum"]["Unit"],
            "Temp": {
                "Min": fc["Temperature"]["Minimum"]["Value"],
                "Max": fc["Temperature"]["Maximum"]["Value"]
            },
            "Feel": {
                "Min": fc["RealFeelTemperature"]["Minimum"]["Value"],
                "Max": fc["RealFeelTemperature"]["Maximum"]["Value"]
            },
            "Shade": {
                "Min": fc["RealFeelTemperatureShade"]["Minimum"]["Value"],
                "Max": fc["RealFeelTemperatureShade"]["Maximum"]["Value"]
            }
        }
        self.SunHours = fc["HoursOfSun"]
        self.Day = ACCUdaynightfcast_class(fc["Day"])
        self.Night = ACCUdaynightfcast_class(fc["Night"])


class ACCUdaily_class(wf.Report_super):
    """ __init__()
        ----------
    """
    def __init__(self, report):
        super().__init__()
        self.EffectiveEpoch = report["Headline"]["EffectiveEpochDate"]
        self.Forecasts = []
        for fc in report["DailyForecasts"]:
            self.Forecasts.append(ACCUdailyForecast_class(fc))

    @staticmethod
    def setClass():
        wf.setClass("ACCU", "daily", ACCUdaily_class)


def initACCU():
    ACCUdaily_class.setClass()
    return
