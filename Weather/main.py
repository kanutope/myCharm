import WeatherForecast as wf
# Press the green button in the gutter to run the script.


def printReport(loc, prov, rep):
    print(loc, prov, rep)
    print(wf.fetchAPI(loc, prov, rep))


def test(loc, prov='', rep=''):
    if len(prov) == 0:
        for __prov in wf.listProviders():
            for __rep in wf.getReports(__prov):
                printReport(loc, __prov, __rep)
    else:
        if len(rep) == 0:
            for __rep in wf.listReports(prov):
                printReport(loc, prov, __rep)
        else:
            printReport(loc, prov, rep)


if __name__ == "__main__":
    test("EBFN", "WAPI")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
