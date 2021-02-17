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


import json
import os
import re

import requests
import time as tm


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


__Config = class_Config()
__Locations = class_Locations()
__APIconfig = class_APIconfig()


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


WINDDIR = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
WINDRNG = 360 / 16.0
WINDBFT = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 999]
WINDDESC = ["Windstil", "Zwakke wind", "Zwakke wind", "Matige wind", "Matige wind", "Vrij krachtige wind",
            "Krachtige wind", "Harde wind", "Stormachtige wind", "Storm", "Zware storm", "Zeer zware storm", "Orkaan"]
MPS2KNT = 3600 / 1852


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
        print("Error %d" % r.status_code)
        return ""


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
    last = []
    for f in [f for f in sorted(os.listdir(getOutputDir())) if patt.search(f) is not None]:
        curr = re.sub(r"_[0-9]{8}-[0-9]{4}.json", "", f)

        if mask == "":
            mask = curr
        else:
            if curr != mask:
                if len(mask) > 0:
                    last.append(prev)
                mask = curr

        prev = f

    if len(prev) > 0:
        last.append(prev)

    return last


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

            indx = int(((wind["deg"] + WINDRNG / 2.0) % 360) / WINDRNG)
            knts = wind["speed"] * MPS2KNT
            bft = beaufort(knts)

            time = tm.strftime("%a %d %b %H:%M", tm.localtime(rec['dt']))
            out = f"{time} - T:{main['temp']:5.1f} gevoels {main['feels_like']:5.1f}" \
                  f" [{main['temp_min']:5.1f} ~{main['temp_max']:5.1f}]" \
                  f" - P: {main['pressure']:4d}hPa" \
                  f" - W: {knts:2.0f}kn {bft:2d}bft {WINDDIR[indx]:^3s} {WINDDESC[bft]:s}"

            print(out)
