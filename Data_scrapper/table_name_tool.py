# encoding=utf-8

from pprint import pprint
import pickle
import json

quest = ""
move = ""

with open("rosetta_stone.dic", "rb") as file:
    RS = pickle.load(file)

pprint(RS)

while move != "e":
    while quest not in RS.keys():
        quest = input("what table would you modifie ? ")
    while move not in ["rm", "ct", "b", "e"]:
        move = input("Remove ? (rm)    Change table ? (ct)     Back ? (b)    End ? (e)")
        if move == "rm":
            RS[quest] = input("What table name ? \n>")
        elif move == "ct":
            del RS[quest]
        elif move in ["b", "e"]:
            pass
with open("rosetta_stone.dic", "wb") as file:
    pickle.dumps(file, RS)
