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
import Weather.ACCUweather as ACCU
import dispatch as dsp
import time as tm
import sys


print (f"len(argv)={len(sys.argv)}")
print (f"argv[1]={sys.argv[1]}")

raise ValueError("Just a value error ;-)")


def analyseACCU():
    ACCU.initACCU()
    #    fnam = f"{wf.getOutputDir()}/{wf.getLatest('8400', 'ACCU', 'daily')[0]}"
    fnam = f"{wf.getOutputDir()}/8400_ACCU-daily_20210223-0758.json"
    obj = wf.getClass("ACCU", "daily")(wf.fetchFile(fnam))
    print(obj)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # python 3.10 ...
    sel = 3

    if sel == 0:
        dsp.execute(dsp.dumpReport, "8660", "ACCU")
    elif sel == 1:
        dsp.execute(dsp.dumpReport, "8660")
    elif sel == 2:
        dsp.execute(dsp.dumpReport, "8660", "WBIT")
    elif sel == 3:
        dsp.execute(dsp.dumpReport, "8660", "WBIT", "usage")
    elif sel == 4:
        day = 60 * 60 * 24
        dt = int(int(tm.time() - day) / day) * day
        dsp.execute(dsp.dumpReport, "8660", "OWMP", "history", ldt=dt)
    elif sel == 5:
        wf.getStructure(loc="8860")
    elif sel == 6:
        wf.loop("8660", "OWMP", "forecast") # chould be removed as it is included in OneCall
    else:
        print (F"set valid, accepted code for sel={sel}")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
