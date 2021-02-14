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
import os
import re


def printReport(loc, prov, rep):
    print(loc, prov, rep)
    print(wf.fetchAPI(loc, prov, rep))


def dumpReport(loc, prov, rep):
    resp = wf.fetchAPI(loc, prov, rep)
    if len(resp) > 0:
        ts = tm.strftime("%Y%m%d-%H%M", tm.localtime())
        nam = f"output/{loc}_{prov}-{rep}_{ts}.json"
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


def latest(loc="", prov="", rep=""):
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
    last = []
    for f in [f for f in sorted(os.listdir("output/")) if patt.search(f) is not None]:
        curr = re.sub(r"_[0-9]{8}\-[0-9]{4}.json", "", f)

        if mask == "":
            mask = curr
        else:
            if curr != mask:
                if len(mask) > 0:
                    last.append(prev)
                mask = curr

        prev = f

    if len(prev) > 0:
        last.append(prev)

    return last


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


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    #    execute(dumpReport, "EBFN", "WAPI")
    #    execute(dumpReport, "8660", "ACCU")
    for f in latest():
        inpFile = "output/" + f
        outFile = inpFile.replace("output/", "struct/").replace(".json", ".txt")
        resp = (wf.fetchFile(inpFile))

        with open(outFile, "w") as fp:
            typ = type(resp)
            print("response", typ, file=fp)

            functions[typ](fp, resp)
            fp.close()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
