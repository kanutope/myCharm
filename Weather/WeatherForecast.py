"""
  Try out
  fetching weather information - forecasts - from several sources.
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


import json         # noqa
import os           # noqa
import re           # noqa

import requests     # noqa
import time as tm   # noqa
from datetime import datetime as dt     # noqa


"""
    Class definitions
"""


class class_Locations:
    """ __init__()
        ----------
    """
    def __init__(self):
        with open("locations.json", "r") as fp:
            self.locations = json.loads(fp.read())
            fp.close()

    def getLocation(self, code):
        return self.locations[code]


class class_APIconfig:
    """ __init__()
        ----------
    """
    def __init__(self):
        self.keys = {}
        with open("APIconfig.json", "r") as fp:
            self.config = json.loads(fp.read())
            fp.close()

    def __getAPIkey(self, prov):
        if not (prov in list(self.keys)):
            with open(self.config[prov]["keyfile"], "r") as fp:
                self.keys[prov] = fp.readline().replace("\n", "")
                fp.close()

        return self.keys[prov]

    def getURL(self, prov, rep, lat, lon, lid):
        key = self.__getAPIkey(prov)
        return (self.config[prov]["reports"][rep]["url"]).format(key=key, lat=lat, lon=lon, id=lid)

    def getPayload(self, prov, rep):
        return self.config[prov]["reports"][rep]["payload"]

    def listProviders(self):
        return list(self.config)

    def listReports(self, prov):
        return list(self.config[prov]["reports"])


class class_Config:
    """ __init__()
        ----------
    """
    def __init__(self):
        with open("config.json", "r") as fp:
            self.config = json.loads(fp.read())
            fp.close()

    def getOutputDir(self):
        return self.config["output"]

    def getQueryDir(self):
        return self.config["query"]

    def getStructDir(self):
        return self.config["struct"]


"""
    Static objects
"""


__Config = class_Config()
__Locations = class_Locations()
__APIconfig = class_APIconfig()


"""
    Public functions accessing the static objects
"""


def listProviders():
    return __APIconfig.listProviders()


def listReports(prov):
    return __APIconfig.listReports(prov)


def getOutputDir():
    return __Config.getOutputDir()


def getQueryDir():
    return __Config.getQueryDir()


def getStructDir():
    return __Config.getStructDir()


def epoch2str(epoch):
    return dt.fromtimestamp(epoch).isoformat(sep=' ')


def epoch2time(epoch):
    return tm.strftime("%H:%M", tm.localtime(epoch))


"""
    Data record (class) definitions
"""


class Record_super:
    def __init__(self):
        self.EffectiveEpoch = -1
        self.Forecasts = []

    def __str__(self):
        ret = f"EffectiveDate = {epoch2str(self.EffectiveEpoch)} - "
        for fc in self.Forecasts:
            ret = f"{ret}\n  {str(fc)}"
        return ret


class Forecast_super:
    def __init__(self):
        self.ForecastEpoch = -1
        self.temperatures = []
        self.Sun = None
        self.Moon = None

    def __str__(self):
        temperatures = self.temperatures
        unit = temperatures["Unit"]
        temp = temperatures["Temp"]
        feel = temperatures["Feel"]
        shade = temperatures["Shade"]

        ret = f"forecast {epoch2str(self.ForecastEpoch)} - " \
              f"Sun: {str(self.Sun)} - Moon: {str(self.Moon)}" \
              f"\n    Temper. Min:{temp['Min']:5.1f}{unit} Max:{temp['Max']:5.1f}{unit}" \
              f"      gevoels Min:{feel['Min']:5.1f}{unit} Max:{feel['Max']:5.1f}{unit}" \
              f"      schaduw Min:{shade['Min']:5.1f}{unit} Max:{shade['Max']:5.1f}{unit}"
        return ret


class Transition_super:
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


"""
    Some static (constant) variables
"""


MPS2KNT = 3600 / 1852
WINDDIV = 360 / 16.0
WINDBFT = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 999]
WINDDIR = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
WINDDESC = ["Windstil", "Zwakke wind", "Zwakke wind", "Matige wind", "Matige wind", "Vrij krachtige wind",
            "Krachtige wind", "Harde wind", "Stormachtige wind", "Storm", "Zware storm", "Zeer zware storm", "Orkaan"]


"""
    Public functions
"""


def beaufort(spd):
    i = 0
    while spd > WINDBFT[i]:
        i = i + 1

    return i


def getReport(code: str, prov: str, rep: str) -> str:
    loc = __Locations.getLocation(code)
    lid = loc["id"]
    lat = loc["lat"]
    lon = loc["lon"]

    r = requests.get(__APIconfig.getURL(prov, rep, lat, lon, lid),
                     params=__APIconfig.getPayload(prov, rep))

    if r.status_code == 200:
        return r.text  # .content
    else:
        print(f"Error {r.status_code}")
        print(r.text)
        return "{}"


def fetchAPI(code, prov, rep) -> dict:
    response = json.loads(getReport(code, prov, rep))
    return response


def fetchFile(fnam) -> dict:
    with open(fnam, "r") as fp:
        response = json.loads(fp.read())
        fp.close()

        return response


def structDict(fp, obj, ind=""):
    ind = ind + "  "
    for key in iter(obj):
        typ = type(obj[key])
        print(ind, key, typ, file=fp)

        if typ in iter(functions):
            functions[typ](fp, obj[key], ind)


def structList(fp, obj, ind=""):
    ind = ind + "  "
    for fld in obj:
        typ = type(fld)
        print(ind, typ, file=fp)

        if typ in iter(functions):
            functions[typ](fp, fld, ind)


functions = {dict: structDict,
             list: structList
             }


def getLatest(loc="", prov="", rep=""):
    if len(loc) > 0:
        patt = f"{loc}"
    else:
        patt = "[0-9,A-Z,a-z]{4}"

    if len(prov) > 0:
        patt = f"{patt}_{prov}"
    else:
        patt = f"{patt}_[A-Z,a-z]+"

    if len(rep) > 0:
        patt = f"{patt}\\-{rep}"
    else:
        patt = f"{patt}\\-[A-Z,a-z]*"

    patt = re.compile(patt)

    prev = ""
    mask = ""
    latest = []
    for f in [f for f in sorted(os.listdir(getOutputDir())) if patt.search(f) is not None]:
        curr = re.sub(r"_[0-9]{8}-[0-9]{4}.json", "", f)

        if mask == "":
            mask = curr
        elif curr != mask:
            if len(mask) > 0:
                latest.append(prev)
            mask = curr

        prev = f

    if len(prev) > 0:
        latest.append(prev)

    return latest


def getStructure(loc="", prov="", rep=""):
    for f in getLatest(loc, prov, rep):
        inpFile = getOutputDir() + "/" + f
        outFile = inpFile.replace(f"{getOutputDir()}/", f"{getStructDir()}/").replace(".json", ".txt")
        resp = (fetchFile(inpFile))

        with open(outFile, "w") as fp:
            typ = type(resp)
            print("response", typ, file=fp)

            functions[typ](fp, resp)
            fp.close()


def loop(loc="", prov="", rep=""):
    for fil in getLatest(loc, prov, rep):
        data = fetchFile(getOutputDir() + "/" + fil)

        for rec in data["list"]:
            main = rec["main"]
            wthr = rec["weather"]
            wind = rec["wind"]

            indx = int(((wind["deg"] + WINDDIV / 2.0) % 360) / WINDDIV)
            knts = wind["speed"] * MPS2KNT
            bft = beaufort(knts)

            time = tm.strftime("%a %d %b %H:%M", tm.localtime(rec['dt']))
            out = f"{time} - T:{main['temp']:5.1f} gevoels {main['feels_like']:5.1f}" \
                  f" [{main['temp_min']:5.1f} ~{main['temp_max']:5.1f}]" \
                  f" - P: {main['pressure']:4d}hPa" \
                  f" - W: {knts:2.0f}kn {bft:2d}bft {WINDDIR[indx]:^3s} {WINDDESC[bft]:s}"

            print(out)
