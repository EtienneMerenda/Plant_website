# -*- coding: utf-8 -*-

"""Script chargé de trier mes listes faites mains pour
 la création de ma dataBase"""

import os
from pprint import pprint

# Déclaration de ma liste ayant pour but de contenir tous les noms de mes
# tables.

table_name = []

name_file = os.listdir(os.getcwd()+"/txt")
pprint(name_file)

for file_name in name_file:
    with open(os.getcwd()+"/txt/"+file_name, "r", encoding="utf-8") as file:
        list_table = file.readlines()
        list_table = list_table[2:]
        for item in list_table:
            i = 0
            for char in item:
                if char == ":":
                    break
                else:
                    i += 1
            item = item[0:i].strip("\n").strip(",").replace("é", "e")
            if item+"\n" not in table_name and item != "":
                table_name.append(item+"\n")

table_name = sorted(table_name)

with open(os.getcwd()+"/table_name.txt", "w", encoding="utf-8") as file:
    file.writelines(table_name)

pprint(sorted(table_name))
