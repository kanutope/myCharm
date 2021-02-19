# initialize remaining common functions
period = {}
for fnc in [readBME280, storeData]:
    nam = fnc.__name__
    cnf = Configuration.objects.get(module="readSensor", parameter=nam)
    per = float(cnf.value)
    dly = float(cnf.value2)
    poll.setPeriod(nam, per, fnc, dly)
    period[nam] = per