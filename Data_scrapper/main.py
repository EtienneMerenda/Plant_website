# conding:utf-8

# import data manager class
from tools.Converter import Converter
# import object used for stock data
from tools.Plant import Plant
# import pprint for beautiful print
from pprint import pprint
# function used for scrap data
from scrap import scrap
# function used for convert table name, create table and inject data in DB
from inject import inject

import pickle

linkDict = {}

try:
    with open("do.py", "rb") as file:
        linkDict = pickle.load(file)
except FileNotFoundError:
    with open("../Link_scrapper/all_link.txt", "r", encoding="utf-8") as file:
        for link in file.readlines():
            if len(link) > 6 and len(link) < 20:
                category = link.strip("\n")
                linkDict[category] = []
            if len(link) > 20:
                linkDict[category].append(link.strip("\n"))

for key in linkDict.keys():
    i = len(linkDict[key]) - 1
    while i > 0:
        link = linkDict[key][i]
        print(link)
        # Object will contains scrap data.
        plant = Plant()
        plant.category = key

        # Object will convert table name and date
        conv = Converter()
        conv.rosetta_stone()

        scrap(link, plant, conv)
        if "mélange" in plant.name or "melange" in plant.name or \
           "Mélange" in plant.name or "Melange" in plant.name:
            print(len(linkDict), len(linkDict[key]))
            del linkDict[key][i]
        else:
            inject(plant, conv)
            print(len(linkDict), len(linkDict[key]))
            del linkDict[key][i]

        i -= 1

        with open("do.py", "wb") as file:
            file.write(pickle.dumps(linkDict))
