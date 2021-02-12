"""
  Try out
  fetching weather information - forecasts - from several sources.
"""

import json
import requests
import time as tm


LOCATIONS = {}
KEYFILES = {}
KEYS = {'OWM': None     # OWM = OpenWeatherMap
        }


WINDDIR = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
WINDRNG = 360 / 16.0
WINDBFT = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 999]
WINDDESC = ['Windstil', 'Zwakke wind', 'Zwakke wind', 'Matige wind', 'Matige wind', 'Vrij krachtige wind',
            'Krachtige wind', 'Harde wind', 'Stormachtige wind', 'Storm', 'Zware storm', 'Zeer zware storm', 'Orkaan']
MPS2KNT = 3600 / 1852


def init_locations():
    locations = {}

    with open('locations.json', 'r') as fp:
        locations = json.loads(fp.read())

    return locations


def init_keyfiles():
    keyfiles = {}

    with open('keyfiles.json', 'r') as fp:
        keyfiles = json.loads(fp.read())

    return keyfiles


def get_openweathermap_key(prov='None'):
    """

    :param prov:
    :return:
    """
    if prov in KEYS:
        if KEYS[prov] is None:
            with open(KEYFILES[prov], 'r') as fp:
                KEYS[prov] = fp.readline().replace('\n', '')

        return KEYS[prov]
    else:
        return 'NONE'


def beaufort(spd):
    i = 0
    while spd > WINDBFT[i]:
        i = i + 1

    return i


def download_report(lat: float, lon: float) -> str:
    payload = {'units': 'metric', 'lang': 'nl'}

    key = get_openweathermap_key('OWM')
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat:.4f}&lon={lon:.4f}&appid={key}"

    r = requests.get(url, params=payload)

    if r.status_code == 200:
        ret = r.text  # .content
    else:
        print('Error %d' % r.status_code)
        ret = None

    return ret


def fetch(code) -> dict:
    loc = LOCATIONS[code]
    response = json.loads(download_report(loc['lat'], loc['lon']))
    return response


def file(fnam='openweather.DEPANNE') -> dict:
    fp = open(fnam, 'r')
    response = json.loads(fp.read())
    return response


def loop(data=None):
    if data is None:
        data = file()

    for rec in data['list']:
        main = rec['main']
        wthr = rec['weather']
        wind = rec['wind']

        indx = int(((wind['deg'] + WINDRNG / 2.0) % 360) / WINDRNG)
        knts = wind['speed'] * MPS2KNT
        bft = beaufort(knts)

        out = f"{tm.strftime('%a %d %b %H:%M', tm.localtime(rec['dt']))}" \
              f" - T:{main['temp']:5.1f} gevoels {main['feels_like']:5.1f}" \
              f" [{main['temp_min']:5.1f} ~{main['temp_max']:5.1f}]" \
              f" - P: {main['pressure']:4d}hPa" \
              f" - W: {knts:2.0f}kn {bft:2d}bft {WINDDIR[indx]:^3s} '{WINDDESC[bft]:s}'"

        print(out)


def test():
    global LOCATIONS
    global KEYFILES

    LOCATIONS = init_locations()
    KEYFILES = init_keyfiles()

    return fetch("8660")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(test())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
