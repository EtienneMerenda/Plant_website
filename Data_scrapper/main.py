from MySQL_Administrator import MySQLAdministrator
from BeautifulSoup import Soup
import requests
import re
import pprint

r = requests.get("https://www.promessedefleurs.com/acorus-gramineus-ogon-jonc-japonais-panache.html")
soup = Soup(data=r.text)

dictWithoutSearch = {}
FinalDict = {}
ErrorDict = {}

# name

dictWithoutSearch["nom"] = soup.find("div", attrs={"class": "product-name"})

# Botanique

dictWithoutSearch["genre"] = soup.find("li", attrs={"class": "genre_botanique"})
dictWithoutSearch["espece"] = soup.find("li", attrs={"class": "espece"})
dictWithoutSearch["famille"] = soup.find("li", attrs={"class": "famille"})
dictWithoutSearch["origine"] = soup.find("li", attrs={"class": "origine"})
dictWithoutSearch["autres noms"] = soup.find("li", attrs={"class": "autres_noms_communs"})

# floraison

dictWithoutSearch["couleur"] = soup.find("li", attrs={"class": "couleur_fleur"})
dictWithoutSearch["periode de floraison"] = soup.find("li", attrs={"class": "periode_floraison"})
dictWithoutSearch["forme fleur"] = soup.find("li", attrs={"class": "forme_fleur"})
dictWithoutSearch["taille fleur"] = soup.find("li", attrs={"class": "taille_fleur"})
dictWithoutSearch["parfum"] = soup.find("li", attrs={"class": "parfum"})

# Feuillage
dictWithoutSearch["feuillage"] = soup.find("li", attrs={"class": "persistance_feuillage"})
if dictWithoutSearch["feuillage"] is None:
    dictWithoutSearch["feuillage"] = soup.find("li", attrs={"clas": "persistance_feuillage"})
dictWithoutSearch["couleur feuillage"] = soup.find("li", attrs={"class": "couleur_feuillage"})

# Port

dictWithoutSearch["Hauteur à maturité"] = soup.find("li", attrs={"class": "hauteur"})
dictWithoutSearch["Envergure à maturité"] = soup.find("li", attrs={"class": "largeur"})
dictWithoutSearch["Croissance"] = soup.find("li", attrs={"class": "vitesse_de_pousse"})

# Date de plantation

dictWithoutSearch["date de plantation"] = soup.find("li", attrs={"class": "periode_raisonnable_plantation"})

# Quel endroit

dictWithoutSearch["type de jardin"] = soup.find("li", attrs={"class": "type_jardin"})
dictWithoutSearch["type d'utilisation"] = soup.find("li", attrs={"class": "type_utilisation"})
dictWithoutSearch["rusticité"] = soup.find("li", attrs={"class": "rusticite"})
# Balise <li> non fermé.------------------Traitement Spécial--------------------
dictWithoutSearch["densité de plantation"] = soup.find("li", attrs={"class": "densite_plantation"})
dictWithoutSearch["spécificite du substrat"] = soup.find("li", attrs={"class": "specificite_substrat"})
dictWithoutSearch["exposition"] = soup.find("li", attrs={"class": "exposition"})
dictWithoutSearch["ph du sol"] = soup.find("li", attrs={"class": "ph_sol"})
dictWithoutSearch["drainage humidite"] = soup.find("li", attrs={"class": "drainage_humidite"})

# soins

dictWithoutSearch["arrosage"] = soup.find("li", attrs={"class": "arrosage"})
dictWithoutSearch["résistance aux maladie"] = soup.find("li", attrs={"class": "resistance_maladie"})
dictWithoutSearch["hivernage"] = soup.find("li", attrs={"class": "hivernage"})
dictWithoutSearch["periode de taille"] = soup.find("li", attrs={"class": "periode_taillage"})

for key in dictWithoutSearch.keys():
    FinalDict[key] = None

try:
    FinalDict["nom"] = dictWithoutSearch["nom"].find("h1").get_text(" ", strip=True)
    ErrorDict[FinalDict["nom"]] = {}
except AttributeError:
    print("Error Name")

for key, item in dictWithoutSearch.items():

    if FinalDict[key] is None:
        try:
            FinalDict[key] = item.h2.text
        except AttributeError:
            pass

    if FinalDict[key] is None:
        try:
            FinalDict[key] = item.find("span", attrs={"class": "value"}).text
        except AttributeError:
            pass

    if FinalDict[key] is None:
        try:
            FinalDict[key] = item.find("span", attrs={"class": "value"}).text
        except AttributeError:
            pass

    if FinalDict[key] is None:
        try:
            FinalDict[key] = item.get_text(" ", strip=True).strip(" ").strip("Exposition")
            FinalDict[key] = re.sub(" ", "", FinalDict[key])
            FinalDict[key] = re.sub("\n", " ", FinalDict[key])

        except AttributeError:
            pass

    if FinalDict[key] is None:
        print("error", FinalDict[key])
        try:
            ErrorDict[FinalDict["nom"]][key] = item
        except AttributeError:
            pass

pprint(FinalDict)
pprint(ErrorDict)


# ------------------------------------------------------------------------------

# MySQL Traitement.
