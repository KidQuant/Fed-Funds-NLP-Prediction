import csv
import os
import re
from os import listdir
from os.path import isfile, join

from nltk.stem.lancaster import LancasterStemmer

from textmining_withnumbers import TermDocumentMatrix as TDM

# Directory where the stop word and n-gram to concatenate are
datadir = "data"
# Where the raw statement are
statementdir = os.path.join("statements", "statements.raw")
# Where the clean statements will go (with and without preprocessing)
cleanDir = os.path.join("statements", "statements.clean")
cleanDirNP = os.path.join("statements", "statements.clean.np")
# Where the cleaned documents should go
outputDr = "output"


def getReplacementList(list_name):
    allWords = [line.rstrip("\n") for line in open(list_name, "r")]
    oldWords = [allWords[i] for i in range(len(allWords)) if i % 2 == 0]
    newWords = [allWords[i] for i in range(len(allWords)) if i % 2 == 1]
    return [oldWords, newWords]


def cleanStatement(
    statement, locationold, replacements, locationnew, stoplist, charsToKeep
):

    # Read in the statement and covert it to lower case
    original = open(os.path.join(locationold, statement), "r").read().lower()

    clean = original
    # Remove punctuation and newlines first, to keep space between words
    for todelete in [".", "\r\n", "\n", ",", "-", ";", ":"]:
        clean = clean.replace(todelete, "")

    # Keep only the characters that you want to keep
    clean = re.sub(charsToKeep, "", clean)
    clean = clean.replace("  ", " ")
    clean = clean.replace(" u s", " unitedstates ")

    # Remove anything before (and including) 'for immediate release'
    deleteBefore = re.search("[Ff]or\s[Ii]mmdiate\s[Rr]elease", clean).start() + len(
        "for immediate release"
    )

    clean = clean[deleteBefore:]

    # Looking for the end of the text
    intaking = re.search("in\staking\sthe\sdiscount\srate\saction", clean)
    votingfor = re.search("voting\sfor\sthe\sdiscount\srate\saction", clean)
    if intaking == None and not votingfor == None:
        deleteAfter = votingfor.start()
    elif votingfor == None and not intaking == None:
        deleteAfter = intaking.start()
    elif votingfor == None and intaking == None:
        deleteAfter = len(clean)
    else:
        deleteAfter = min(votingfor.start(), intaking.start())
    clean = clean[:deleteAfter]

    # Replace replacement words (concatenations)
    for word in range(len(replacements[0])):
        clean = clean.replace(replacements[0][word], replacements[1][word])

    # Remove stop words
    for word in stoplist:
        clean = clean.replace(" " + word.lower() + " ", " ")

    # Write cleaned file
    new = open(os.path.join(locationnew, statement), "w")
    new.write(clean)
    new.close


def main():
    stoplist = [
        line.rstrip("\n")
        for line in open(os.path.join(datadir, "stoplist_mcdonald_comb.txt"), "r")
    ]
    stoplistNP = [
        line.rstrip("\n") for line in open(os.path.join(datadir, "emptystop.txt"), "r")
    ]
    replacements = getReplacementList(os.path.join(datadir, "wordlist.txt"))
    replacementsNP = getReplacementList(os.path.join(datadir, "wordlist.np.txt"))

    statementList = [f for f in listdir(statementdir) if isfile(join(statementdir, f))]

    for statement in statementList:
        # First, the case with heavier preprocessing (keep only letters)
        cleanStatement(
            statement, statementdir, replacements, cleanDir, stoplist, "[^A-Za-z ]+", 1
        )

        # Second, the no-preprocessing case (keep letters and numbers)
        cleanStatement(
            statement,
            statementdir,
            replacementsNP,
            cleanDirNP,
            stoplistNP,
            "[^A-Za-z0-9 ]+",
            0,
        )
