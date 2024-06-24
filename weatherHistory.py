import dispatch as dsp
import time as tm
import sys

i = 1
if len(sys.argv) > 1:
    try:
        i = int(sys.argv[1])
        if (i > 5):
            raise ValueError("Cannot walk back more than 5 days!")
    except:
        raise ValueError("(first) argument shoud be an Integer between 1 and 5!")

day = 60 * 60 * 24
dt = int(int(tm.time() - i * day) / day) * day
dsp.execute(dsp.dumpReport, "8660", "OWMP", "history", ldt=dt)
