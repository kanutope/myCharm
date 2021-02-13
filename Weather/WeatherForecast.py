"""
  Try out
  fetching weather information - forecasts - from several sources.
"""

import json

import requests
import time as tm


class class_Locations:
    """ __init__()
        ----------
    """
    def __init__(self):
        with open("locations.json", "r") as fp:
            self.locations = json.loads(fp.read())

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

    def __getAPIkey(self, prov):
        if not (prov in list(self.keys)):
            with open(self.config[prov]["keyfile"], "r") as fp:
                self.keys[prov] = fp.readline().replace("\n", "")

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


__APIconfig = class_APIconfig()
__Locations = class_Locations()


def listProviders():
    return __APIconfig.listProviders()


def listReports(prov):
    return __APIconfig.listReports(prov)


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


def fetchFile(fnam="openweather.DEPANNE") -> dict:
    fp = open(fnam, "r")
    response = json.loads(fp.read())
    return response


def loop(data=None):
    if data is None:
        data = fetchFile()

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
