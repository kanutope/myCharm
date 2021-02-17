"""
UNLICENSE:
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.
"""

# SPDX-License-Identifier: Unlicense

import WeatherForecast as wf
import time as tm
import json


def fetch_and_print(loc, prov, rep):
    print(loc, prov, rep)
    print(wf.fetchAPI(loc, prov, rep))


def dumpReport(loc, prov, rep):
    resp = wf.fetchAPI(loc, prov, rep)
    if len(resp) > 0:
        ts = tm.strftime("%Y%m%d-%H%M", tm.localtime())
        nam = f"{wf.getOutputDir()}/{loc}_{prov}-{rep}_{ts}.json"
        with open(nam, "w") as fp:
            print(ts, loc, prov, rep, json.dump(resp, fp, indent=2))
            fp.close()


def execute(func, loc, prov="", rep=""):
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
    #    execute(dumpReport, "8660", "ACCU")
    execute(dumpReport, "8660")
    #    wf.getStructure(loc="8860")
    wf.loop("8660", "OWMP", "forecast")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
