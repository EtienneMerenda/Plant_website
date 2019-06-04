# encoding=utf-8

from pprint import pprint
import pickle

quest = ""
move = ""

with open("modifier.txt", "r", encoding="utf-8") as file:
    tmpRS = file.readlines()

    RS = {}

    pprint(tmpRS)

    for line in tmpRS:
        for i, char in enumerate(line):
            if char == ":":
                break
        if line[:i] != "_date":
            RS[line[:i]] = line[i+1:].strip("\n")
        else:
            strDict = line[i+1:].strip("\n").split(" ")
            strDict = [i.strip(" .':{},") for i in strDict]
            _date = dict((a[0], int(a[1])) for a in dict(strDict[i:i+2] for i in range(0, len(strDict), 2)).items())
            RS["_date"] = _date

pprint(RS)

with open("RS.dic", "wb") as file:
    file.write(pickle.dumps(RS))
