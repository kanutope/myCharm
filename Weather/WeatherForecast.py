"""
    WeatherForecast

    fetching weather information - forecasts - from several sources.

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
from datetime import datetime as dt

myPath = os.path.dirname(os.path.abspath(__file__))


def fullPath(path):
    return myPath + '/' + path


"""
    Class definitions
"""


class class_Locations:
    def __init__(self):
        with open(fullPath('locations.json'), 'r') as fp:
            self.locations = json.loads(fp.read())
            fp.close()

    def reInit(self):
        self.__init__()

    def getLocation(self, code):
        return self.locations[code]


class class_APIconfig:
    def __init__(self):
        self.keys = {}
        with open(fullPath('APIconfig.json'), 'r') as fp:
            self.config = json.loads(fp.read())
            fp.close()

            cnf = self.config
            for prov in cnf:
                reps = cnf[prov]['reports']
                for rep in reps:
                    reps[rep]['class'] = None

    def reInit(self):
        self.__init__()

    def __getAPIkey(self, prov):
        if not (prov in list(self.keys)):
            with open(fullPath(self.config[prov]['keyfile']), 'r') as fp:
                self.keys[prov] = fp.readline().replace('\n', "")
                fp.close()

        return self.keys[prov]

    def getURL(self, prov, rep, lat, lon, lid, ldt=""):
        key = self.__getAPIkey(prov)
        return (self.config[prov]['reports'][rep]['url']).format(key=key, lat=lat, lon=lon, id=lid, dt=ldt)

    def getPayload(self, prov, rep):
        return self.config[prov]['reports'][rep]['payload']

    def listProviders(self):
        return list(self.config)

    def listReports(self, prov):
        return list(self.config[prov]['reports'])


class class_Config:
    """ __init__()
        ----------
    """
    def __init__(self):
        with open(fullPath('config.json'), 'r') as fp:
            self.config = json.loads(fp.read())
            fp.close()

    def getOutputDir(self):
        return fullPath(self.config['output'])

    def getQueryDir(self):
        return fullPath(self.config['query'])

    def getStructDir(self):
        return fullPath(self.config['struct'])


"""
    Static objects
"""

__Config = class_Config()
__Locations = class_Locations()
__APIconfig = class_APIconfig()


"""
    Public functions accessing __APIconfig
"""


def listProviders():
    return __APIconfig.listProviders()


def listReports(prov):
    return __APIconfig.listReports(prov)


"""
    Public functions accessing __Config
"""


def getOutputDir():
    return __Config.getOutputDir()


def getQueryDir():
    return __Config.getQueryDir()


def getStructDir():
    return __Config.getStructDir()


"""
    Public functions used by the Report data classes
"""


def epoch2str(epoch):
    return dt.fromtimestamp(epoch).isoformat(sep=' ')


def epoch2time(epoch):
    return tm.strftime('%H:%M', tm.localtime(epoch))


"""
    Public functions
"""


def getReport(code: str, prov: str, rep: str, ldt="") -> str:
    loc = __Locations.getLocation(code)
    lid = loc['lid']
    lat = loc['lat']
    lon = loc['lon']

    print(__APIconfig.getURL(prov, rep, lat, lon, lid, ldt))
    r = requests.get(__APIconfig.getURL(prov, rep, lat, lon, lid, ldt),
                     params=__APIconfig.getPayload(prov, rep))

    if r.status_code == 200:
        return r.text  # .content
    else:
        print(f"Error {r.status_code}")
        print(r.text)
        return ""


def fetchAPI(code, prov, rep, ldt="") -> dict:
    response = json.loads(getReport(code, prov, rep, ldt))
    return response


def fetchFile(fnam) -> dict:
    with open(fnam, 'r') as fp:
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
        inpFile = getOutputDir() + '/' + f
        outFile = inpFile.replace(f"{getOutputDir()}/", f"{getStructDir()}/").replace('.json', " STRUC.txt")
        resp = (fetchFile(inpFile))

        with open(outFile, 'w') as fp:
            typ = type(resp)
            print('response', typ, file=fp)

            functions[typ](fp, resp)
            fp.close()
