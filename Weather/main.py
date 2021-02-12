"""
  Try out
  fetching weather information - forecasts - from several sources.
"""

import json
import requests
import time as tm

# OWM = OpenWeatherMap
KEYS = {'OWM': None
        }
KEYFILES = {'OWM': 'openweathermap.key'
            }

ZIP = {'De Panne': 8660,
       'Oostende': 8400
       }
COORD = {8660: {'lat': 51.0935, 'lon': 2.5776},
         8400: {'lat': 51.2322, 'lon': 2.9144}
         }

WINDDIR = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
WINDRNG = 360 / 16.0
WINDBFT = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 999]
WINDDESC = ['Windstil', 'Zwakke wind', 'Zwakke wind', 'Matige wind', 'Matige wind', 'Vrij krachtige wind',
            'Krachtige wind', 'Harde wind', 'Stormachtige wind', 'Storm', 'Zware storm', 'Zeer zware storm', 'Orkaan']
MPS2KNT = 3600 / 1852


def get_openweathermap_key(prov='None'):
    """

    :param prov:
    :return:
    """
    global KEYS

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


def fetch(zipcode) -> dict:
    loc = COORD[zipcode]
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fetch(8660)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
