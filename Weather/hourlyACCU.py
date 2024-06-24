import json

true = True
false = False

with open("query/accuweather-12hours.json", "r") as fp:
    data = json.load(fp)
    fp.close()

for rec in data:
    time = (rec['DateTime'].replace("T", " ")).replace(":00+02:00", "")
    temp_c = rec['Temperature']['Value']
    wind_kph = rec['Wind']['Speed']['Value']
    wind_degree = rec['Wind']['Direction']['Degrees']
    wind_dir = rec['Wind']['Direction']['Localized']
    gust_kph = rec['WindGust']['Speed']['Value']
    pressure_mb = -1
    condition = rec['IconPhrase']
    print(f"{time}\tACCU\t{temp_c}°C\t{wind_kph}\tkm/h\t{wind_degree}°\t{wind_dir}\t{pressure_mb}\tmb\t{condition}")
    