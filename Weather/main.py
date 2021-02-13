"""
  Try out
  fetching weather information - forecasts - from several sources.
"""

import json
import requests
import time as tm


LOCATIONS = {}
APICONFIG = {}
APIKEYS = {}


WINDDIR = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
WINDRNG = 360 / 16.0
WINDBFT = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 999]
WINDDESC = ["Windstil", "Zwakke wind", "Zwakke wind", "Matige wind", "Matige wind", "Vrij krachtige wind",
            "Krachtige wind", "Harde wind", "Stormachtige wind", "Storm", "Zware storm", "Zeer zware storm", "Orkaan"]
MPS2KNT = 3600 / 1852


def initLocations():
    global LOCATIONS

    if len(LOCATIONS) == 0:
        with open("locations.json", "r") as fp:
            LOCATIONS = json.loads(fp.read())


def initAPIconfig():
    global APICONFIG

    if len(APICONFIG) == 0:
        with open("APIconfig.json", "r") as fp:
            APICONFIG = json.loads(fp.read())


def getAPIkey(prov="None"):
    """

    :param prov:
    :return:
    """
    if not(prov in APIKEYS):
        with open(APICONFIG[prov]["keyfile"], "r") as fp:
            APIKEYS[prov] = fp.readline().replace("\n", "")

    return APIKEYS[prov]


def beaufort(spd):
    i = 0
    while spd > WINDBFT[i]:
        i = i + 1

    return i


def getReport(code: str, prov: str, api: str) -> str:
    loc = LOCATIONS[code]
    id = loc["id"]
    lat = loc["lat"]
    lon = loc["lon"]

    key = getAPIkey(prov)
    url = APICONFIG[prov]["reports"][api]["url"].format(key=key, lat=lat, lon=lon, id=id)

    r = requests.get(url, params=APICONFIG[prov]["reports"][api]["payload"])

    if r.status_code == 200:
        return r.text  # .content
    else:
        print("Error %d" % r.status_code)
        return ""


def fetchAPI(code, prov, api) -> dict:
    response = json.loads(getReport(code, prov, api))
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


def printReport(loc, rep, qry):
    print(rep, qry)
    print(fetchAPI(loc, rep, qry))


def test(loc, prov='', qry=''):
    initLocations()
    initAPIconfig()

    if len(prov) == 0:
        for __prov in list(APICONFIG):
            for __qry in list(APICONFIG[__prov]["reports"]):
                printReport(loc, __prov, __qry)
    else:
        if len(qry) == 0:
            for __qry in list(APICONFIG[prov]["reports"]):
                printReport(loc, prov, __qry)
        else:
            printReport(loc, prov, qry)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    test("8660", "ACCU")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
