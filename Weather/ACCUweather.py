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
        self.Age = -1
        self.Phase = ""
        self.RiseEpoch = trans["EpochRise"]
        self.SetEpoch = trans["EpochSet"]
        
        if "Phase" in list(trans):
            self.Phase = trans["Phase"]
        if "Age" in list(trans):
            self.Age = trans["Age"]


class ACCUdailyForecast_class(wf.Forecast_super):
    """ __init__()
        ----------
    """
    def __init__(self, fc):
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


class ACCUdaily_class(wf.Record_super):
    """ __init__()
        ----------
    """
    def __init__(self, report):
        self.EffectiveEpoch = report["Headline"]["EffectiveEpochDate"]
        self.Forecasts = []
        for fc in report["DailyForecasts"]:
            self.Forecasts.append(ACCUdailyForecast_class(fc))

