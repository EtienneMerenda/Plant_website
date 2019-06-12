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

linkDict = {}

with open("../Link_scrapper/all_link.txt", "r", encoding="utf-8") as file:
    for link in file.readlines():
        if len(link) > 6 and len(link) < 20:
            category = link.strip("\n")
            linkDict[category] = []
        if len(link) > 20:
            linkDict[category].append(link.strip("\n"))

for key in linkDict.keys():

    for link in linkDict[key]:
        print(link)
        # Object will contains scrap data.
        plant = Plant()
        plant.category = key

        # Object will convert table name and date
        conv = Converter()
        conv.rosetta_stone()

        scrap(link, plant, conv)
        inject(plant, conv)

        with open("do.txt", "a", encoding="utf-8") as file:
            file.write(link+"\n")
