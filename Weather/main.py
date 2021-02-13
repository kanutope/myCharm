import WeatherForecast as wf
# Press the green button in the gutter to run the script.


def printReport(loc, rep, qry):
    print(loc, rep, qry)
    print(wf.fetchAPI(loc, rep, qry))


def test(loc, prov='', qry=''):
    wf.initAPIconfig()

    if len(prov) == 0:
        for __prov in list(wf.APICONFIG):
            for __qry in list(wf.APICONFIG[__prov]["reports"]):
                printReport(loc, __prov, __qry)
    else:
        if len(qry) == 0:
            for __qry in list(wf.APICONFIG[prov]["reports"]):
                printReport(loc, prov, __qry)
        else:
            printReport(loc, prov, qry)


if __name__ == "__main__":
    test("EBFN")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
