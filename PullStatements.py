import csv
import os
import re
from time import sleep
from urllib.request import urlopen

from bs4 import BeautifulSoup


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
