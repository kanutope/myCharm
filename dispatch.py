"""
UNLICENSE:
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.
"""

# SPDX-License-Identifier: Unlicense

import Weather.WeatherForecast as wf
import time as tm
import json


def dumpReport(loc, prov, rep, ldt=""):
    resp = wf.fetchAPI(loc, prov, rep, ldt)
    if len(resp) > 0:
        ts = tm.strftime("%Y%m%d-%H%M", tm.localtime())
        nam = f"{wf.getOutputDir()}/{loc}_{prov}-{rep}_{ts}.json"
        with open(nam, "w") as fp:
            print(ts, loc, prov, rep, json.dump(resp, fp, indent=2))
            fp.close()


def execute(func, loc, prov="", rep="", ldt=""):
    if len(prov) == 0:
        for __prov in wf.listProviders():
            for __rep in wf.listReports(__prov):
                func(loc, __prov, __rep, ldt)
    elif len(rep) == 0:
        for __rep in wf.listReports(prov):
            func(loc, prov, __rep, ldt)
    else:
        func(loc, prov, rep, ldt)

