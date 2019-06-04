# encoding=utf-8

from pprint import pprint
import pickle

quest = ""
move = ""

with open("rosetta_stone.dic", "rb") as file:
    RS = pickle.load(file)

pprint(RS)

with open("modifier.txt", "w", encoding="utf-8") as file:
    for key, value in RS.items():
        file.write(f"{key}:{value}\n\n")
