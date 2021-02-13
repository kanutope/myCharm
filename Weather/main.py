import WeatherForecast as wf
import time as tm
import json


def printReport(loc, prov, rep):
    print(loc, prov, rep)
    print(wf.fetchAPI(loc, prov, rep))


def dumpReport(loc, prov, rep):
    ts = tm.strftime("%Y%m%d-%H%M", tm.localtime())

    out = wf.fetchAPI(loc, prov, rep)
    if len(out) > 0:
        nam = f"output/{prov}-{rep}_{loc}_{ts}.json"
        with open(nam, "w") as fp:
            print(ts, loc, prov, rep, json.dump(out, fp, indent=2))


def execute(func, loc, prov='', rep=''):
    if len(prov) == 0:
        for __prov in wf.listProviders():
            for __rep in wf.listReports(__prov):
                func(loc, __prov, __rep)
    else:
        if len(rep) == 0:
            for __rep in wf.listReports(prov):
                func(loc, prov, __rep)
        else:
            func(loc, prov, rep)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    #    execute(dumpReport, "EBFN", "WAPI")
    execute(dumpReport, "8660", "OWMP", "onecall")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
