# conding:utf-8

"""Try alternative method to get information in the page"""

# adding MySQL folder in path for import MySQL_Administrator.
import sys
# import Pickle for load and pickle table_name_reference dictionary
import pickle
# import pprint for beautiful print
from pprint import pprint
# beautifulSoup for parse html text
from bs4 import BeautifulSoup
# requests for get page in the net.
import requests
# re for nothing

sys.path.append(sys.path[0]+"\\MySQL")
# MySQLAdministrator for admin injection in my database.
from MySQL_Administrator import MySQLAdministrator


r = requests.get("https://www.promessedefleurs.com/acorus-gramineus-ogon-jonc-japonais-panache.html")
soup = BeautifulSoup(r.text, "html5lib")

table_name_reference = {"genre": "genre_botanique",
          "espece": "espece",
          "famille": "famille",
          "origine": "origine",
          "autres_noms": "autres_noms_communs",
          "couleur": "couleur_fleur",
          "periode_floraison": "periode_floraison",
          "inflorescence": "forme_fleur",
          "taille_fleur": "taille_fleur",
          "parfum": "parfum",
          "feuillage": "persistance_feuillage",
          "couleur_feuillage": "couleur_feuillage",
          "hauteur": "hauteur",
          "envergure": "largeur",
          "croissance": "vitesse_de_pousse",
          "date_plantation": "periode_raisonnable_plantation",
          "date_plantation_optimale": "periode_plantation",
          "type_jardin": "type_jardin",
          "type_utilisation": "type_utilisation",
          "rusticite": "rusticite",
          "densite_plantation": "densite_plantation",
          "substrat": "specificite_substrat",
          "exposition": "exposition",
          "ph_sol": "ph_sol",
          "drainage": "drainage_humidite",
          "arrosage": "arrosage",
          "resistance_maladie": "resistance_maladie",
          "hivernage": "hivernage",
          "periode_taille": "periode_taillage",
          }



with open("table_name.dic", "wb") as file:
    pickle.dump(table_name_reference, file)

# name

name = soup.find("div", attrs={"class": "product-name"}).find("h1").get_text(strip=True)

# I take the html's part thats interests me

raw_data = {"col2-md": soup.find("div", id="tabs-description").find("div", attrs={"class": "col2-md description"}),
            "col-right": soup.find("div", id="tabs-soins").find("div", attrs={"class": "col-right"})}

rafined_data = {}

for tag in raw_data.values():
    for li_tag in tag.find_all("li"):
        print(li_tag)
        if li_tag.find("h2") is not None:
            try:
                print(li_tag["class"][0], li_tag.find("h2").get_text(strip=True))
                rafined_data[li_tag["class"][0]] = li_tag.find("h2").get_text(strip=True)
            except KeyError:
                print(li_tag["clas"][0], li_tag.find("h2").get_text(strip=True))
                rafined_data[li_tag["clas"][0]] = li_tag.find("h2").get_text(strip=True)
        else:
            try:
                print(li_tag, li_tag.find("span", class_="value"))
                rafined_data[li_tag["class"][0]] = li_tag.find("span", class_="value").get_text(strip=True)
            except KeyError:
                rafined_data[li_tag["clas"]] = li_tag.find("span", class_="value").get_text(strip=True)

# I make list if the data traitement need and .strip() all useless whitespace.

for key, value in rafined_data.items():
    if "," in value:
        rafined_data[key] = value.split(", ")
        rafined_data[key] = [i.strip() for i in rafined_data[key]]

pprint(rafined_data)
print(len(rafined_data))
