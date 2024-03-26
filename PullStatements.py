import csv
import os
import re
from time import sleep
from urllib.request import urlopen

from bs4 import BeautifulSoup

outdir = os.path.join("statements", "statements.raw")


def FOMCstatementURL(date):
    year = date[0:4]
    dateInt = int(date)
    if dateInt == 20081216:
        urlout = (
            "http://www.federalreserve.gov/newsevents/"
            + "press/monetary"
            + date
            + "b.htm"
        )
    elif dateInt >= 19990501 and dateInt < 20020331:
        urlout = (
            "http://www.federalreserve.gov/boarddocs/"
            + "press/general/"
            + year
            + "/"
            + date
            + "/"
        )
    elif dateInt >= 20020501 and dateInt < 20030000:
        urlout = (
            "http://www.federalreserve.gov/boarddocs/press"
            + "monetary/"
            + year
            + "/"
            + date
            + "/"
        )
    elif dateInt >= 2003000 and dateInt < 20060000:
        urlout = (
            "http://www.federalreserve.gov/boarddocs/press/"
            + "monetary/"
            + year
            + "/"
            + date
            + "/default.htm"
        )
    elif dateInt >= 20050000:
        urlout = (
            "http://www.federalreserve.gov/newsevents/press/"
            + "monetary"
            + date
            + "a.htm"
        )

    return urlout


def getStatement(mtgDate):
    print("Pulling: " + mtgDate)
    html = urlopen(FOMCstatementURL(mtgDate)).read()
    soup = BeautifulSoup(html)
    allText = soup.get_text(" ")
    startLoc = re.search("[Ff]or\s[Ii]mmediate\s[Rr]elease", allText).start()

    statementText = allText[startLoc:]
    endLoc = re.search("[0-9]{4}\s[Mm]onetary\s[Pp]olicy", statementText).start()
    statementText = statementText[:endLoc]
    statementText = statementText.encode("ascii", "ignore").decode("ascii")
    return statementText


def main():
    releaseDates = [
        line.rstrip() for line in open(os.path.join("data", "dates.sort.txt"), "r")
    ]
    for releaseDate in releaseDates:
        data = getStatement(releaseDate)
        # Give the Fed Servers a break
        sleep(2)
        if releaseDate.find("20070618") > -1:
            releaseDate = "20070628"
        filename = "statement.fomc." + releaseDate + ".txt"
        f = open(os.path.join(outdir, filename), "w")
        f.write(data)
        f.close


if __name__ == "__main__":
    main()
