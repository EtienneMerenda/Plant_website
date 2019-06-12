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

sys.path.append(sys.path[0]+"\\MySQL")
# MySQLAdministrator for admin injection in my database.
from MySQL_Administrator import MySQLAdministrator
# import connexion identification in external file registered in .gitignore.
from connexion import user, password


class DataAdmin():

    def __init__(self):
        from pprint import pprint

    def rosetta_stone(self):
        """Get table conversion in extenal file"""
        try:
            with open("RS.dic", "rb") as file:
                self.RS = pickle.load(file)
                self.date = self.RS["_date"]
        except EOFError:
            self.RS = {'arrosage': 'Nom_has_Arrosage',
                       'autres_noms_communs': 'Nom_has_Autre_nom',
                       'climat_de_preference': 'Nom_has_climat',
                       'couleur_feuillage': 'Feuillage_has_Couleur',
                       'couleur_fleur': 'Fleur_has_Couleur',
                       'densite_plantation': 'Nom.densite_plantation',
                       'difficulte_culture': 'Difficulte',
                       'drainage_humidite': 'Nom_has_Drainage',
                       'espece': 'Espece',
                       'exposition': 'Nom_has_Exposition',
                       'famille': 'Famille',
                       'forme_fleur': 'Inflorescence',
                       'genre_botanique': 'Genre',
                       'hauteur': 'Nom.hauteur',
                       'hivernage': 'Hivernage',
                       'ignored': ['cultivar'],
                       'largeur': 'Nom.envergure',
                       'origine': 'Origine',
                       'parfum': 'Nom_has_Parfum',
                       'periode_floraison': 'Floraison_has_Date',
                       'periode_plantation': 'Plantation_optimale_has_Date',
                       'periode_raisonnable_plantation': 'Plantation_has_Date',
                       'periode_taillage': 'Taille_has_Date',
                       'persistance_feuillage': 'Persistance_feuillage',
                       'ph_sol': 'Nom_has_Ph_sol',
                       'resistance_maladie': 'Resistance_maladie',
                       'rusticite': 'Nom_has_Rusticite',
                       'specificite_substrat': 'Nom_has_Substrat',
                       'taillage': 'Nom.taille_conseille',
                       'taille_fleur': 'Nom.taille_fleur',
                       'type_jardin': 'Nom_has_Jardin',
                       'type_utilisation': 'Nom_has_Type_utilisation',
                       'vitesse_de_pousse': 'Croissance'}
            self.date = {}

    def burn_RS(self):
        """Save dictionary in external file called 'RS.dic'"""
        self.RS["_date"] = self.date
        with open("RS.dic", "wb") as file:
            pickle.dump(self.RS, file)

    def date_convert(self, date):
        """Convert month in numeric format."""
        for month in date:
            if month not in self.date.keys():
                m = input(f"What month number for {month}: ")
                self.date[month] = int(m)

        date_list = [self.date[i] for i in date]
        return date_list

    def table_convert(self, name):
        """Check if table name is in Rosetta Stone"""
        if name in self.RS["ignored"]:
            pass
        elif name not in self.RS.keys():
            s = ""
            while s != "y":
                ref = input(f"What table for '{key}': ")
                s = input(f"You are sure '{ref}' makes reference to '{key}' ? y/n ")
            self.RS[key] = ref

    def convert(self, key):
        """Return value of given key into rosetta stone."""
        return self.RS[key]

    def ignored(self):
        """Return ignored list into RS."""
        return self.RS["ignored"]

    def RS_read(self):
        """Return RS dictionary."""
        return pprint(self.RS)

admin_data = DataAdmin()
admin_data.rosetta_stone()
r = requests.get("https://www.promessedefleurs.com/annuelles/fleurs-annuelles-en-minimottes/annuelles-par-varietes/bidens/bidens-yellow-charm-bidens-jaune-dore.html")
soup = BeautifulSoup(r.text, "html5lib")

# I get name in tag div with product-name class and in title tag and compare them.
name = soup.find("div", attrs={"class": "product-name"}).find("h1").get_text(strip=True)
checkName = soup.find("title").get_text(strip=True)

name = name.split(" ")
checkName = checkName.split(" ")

name = " ".join([i for i in name if i in checkName])

print(name, checkName)

del checkName

# I take the html's part thats interests me

raw_data = {"col2-md": soup.find("div", id="tabs-description").find("div", attrs={"class": "col2-md description"}),
            "col-right": soup.find("div", id="tabs-soins").find("div", attrs={"class": "col-right"})}

rafined_data = {}

for tag in raw_data.values():
    for li_tag in tag.find_all("li"):
        if li_tag.find("h2") is not None:
            try:
                rafined_data[li_tag["class"][0]] = li_tag.find("h2").get_text(strip=True).lower()
            except KeyError:
                rafined_data[li_tag["clas"][0]] = li_tag.find("h2").get_text(strip=True).lower()
        else:
            try:
                rafined_data[li_tag["class"][0]] = li_tag.find("span", class_="value").get_text(strip=True).lower()
            except KeyError:
                rafined_data[li_tag["clas"]] = li_tag.find("span", class_="value").get_text(strip=True).lower()

    # Get complementary information
    try:
        rafined_data[tag.find("p").parent.find("span", class_="title").get_text(strip=True)] = tag.find("p").get_text(strip=True).lower()
    except AttributeError:
        pass

# I make list if the data traitement need and .strip() all useless whitespace.

for key, value in rafined_data.items():
    if "," in value:
        rafined_data[key] = value.split(", ")
        rafined_data[key] = [i.strip() for i in rafined_data[key]]

# Adding key in table name dictionary for traitement.
for key in rafined_data.keys():
    admin_data.table_convert(key)

    # processing of data about month periods.
    if "periode" in key:
        date = rafined_data[key].strip("de ").replace(" à ", "-").strip(".").lower().split("-")
        date = admin_data.date_convert(date)
        rafined_data[key] = date

# Save table_name_reference
admin_data.burn_RS()

pprint(rafined_data)
print(len(rafined_data))
admin_data.RS_read()
# MySQL Traitement -------------------------------------------------------------

# Connection to MySQL with my MySQLAdministrator classe
path = "./MySQL"
sql = MySQLAdministrator()
sql.makeHelper("./MySQL/")
sql.link(user, password)

# Create DB for test
sql.createDB("Plants")

# Create table "nom" if not exist (in first scrap)
if not sql.inTable("nom"):
    sql.createTable("nom")
    sql.createCol("nom", "nom", "VARCHAR(100)", "UNIQUE NOT NULL")

if not sql.inRow("nom", name):
    sql.insert("nom", name)

for raw_TN, data in rafined_data.items():

    # We skip useless data: cultivar
    if raw_TN not in admin_data.ignored():

        print("\n", raw_TN, admin_data.convert(raw_TN), data, "\n")

        # We work in Name to other table multi-relations.
        if "Nom_has" in admin_data.convert(raw_TN):

            # Get the relation table name too.
            rel_tn = admin_data.convert(raw_TN).lower()
            # Get table_name in RS dict
            tn = rel_tn.replace("nom_has_", "")

            # if the table not exist, we create it.
            if not sql.inTable(tn):
                sql.createTable(tn)
                sql.createCol(tn, "valeur", "VARCHAR(100)")
                sql.createRelTable("nom", tn)

            # Adding value in table if not done yet.
            # print(data)
            # If value is list type
            if isinstance(data, list):
                t = []
                # check if each value not already in table
                for v in data:
                    if not sql.inRow(tn, v):
                        t.append(v)
                # Each data not in table append in list and reaffect to data var
                data = t
                if len(data) > 0:
                    sql.insert(tn, data)
                    for value in data:
                        sql.nnfKey("nom", name, tn, value)
            elif not sql.inRow(tn, data):
                sql.insert(tn, data)
                print("nom", name, tn, data)
                sql.nnfKey("nom", name, tn, data)

        elif "Date" in admin_data.convert(raw_TN):
            # Get the relation table name too.
            rel_tn = admin_data.convert(raw_TN).lower()
            # Get table_name in RS dict
            tn = "date"

            print(rel_tn, tn)

            # if the table not exist, we create it.
            if not sql.inTable(tn):
                sql.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `Plants`.`Date` ( "
                                      "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT, "
                                      "`mois` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_bin' NOT NULL, "
                                      "PRIMARY KEY (`id`), "
                                      "UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE, "
                                      "UNIQUE INDEX `date_UNIQUE` (`mois` ASC) VISIBLE)")

            # if new date appears, we inject it.
            pprint(admin_data.RS["_date"])
            for k, v in admin_data.RS["_date"].items():
                print(k, v)
                if not sql.inRow("date", k):
                    sql.insert("date", k)
                    print(f"UPDATE date SET `id` = {v} WHERE `mois` = '{k}'")
                    sql.myCursor.execute(f"UPDATE date SET `id` = {v} WHERE `mois` = '{k}'")

            # Create relational table.
            if not sql.inTable(rel_tn):
                sql.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `{rel_tn}` ("
                                        f"`nom_id` INT UNSIGNED NOT NULL, "
                                        f"`date_start_id` INT UNSIGNED NOT NULL, "
                                        f"`date_end_id` INT UNSIGNED NOT NULL, "
                                        f"PRIMARY KEY (`nom_id`, `date_start_id`, `date_end_id`), "
                                        f"INDEX `fk_Plantation_has_Date_Date1_idx` (`date_start_id` ASC) VISIBLE, "
                                        f"INDEX `fk_Plantation_has_Date_Date2_idx` (`date_end_id` ASC) VISIBLE, "
                                        f"CONSTRAINT `fk_{rel_tn}_Nom1` "
                                          f"FOREIGN KEY (`Nom_id`) "
                                          f"REFERENCES `Plants`.`Nom` (`id`) "
                                          f"ON DELETE NO ACTION "
                                          f"ON UPDATE NO ACTION, "
                                        f"CONSTRAINT `fk_{rel_tn}_Date1` "
                                          f"FOREIGN KEY (`date_start_id`) "
                                          f"REFERENCES `Plants`.`date` (`id`) "
                                          f"ON DELETE NO ACTION "
                                          f"ON UPDATE NO ACTION, "
                                        f"CONSTRAINT `fk_{rel_tn}_Date2` "
                                          f"FOREIGN KEY (`date_end_id`) "
                                          f"REFERENCES `Plants`.`date` (`id`) "
                                          f"ON DELETE NO ACTION "
                                          f"ON UPDATE NO ACTION) "
                                        f"ENGINE = InnoDB;")

            print("after", data)
            iP = [sql.inRow("nom", name, "k")]
            print(iP)
            data = (tuple(iP + data),)
            print(data)

            if len(data[0]) == 2:
                data = ((data[0][0], data[0][1], data[0][1],),)

            print(data)
            sql.insert(rel_tn, data, ("nom_id", "date_start_id", "date_end_id"))
            # If value is list type

        elif "Couleur" in admin_data.convert(raw_TN):

            # Get the relation table name too.
            rel_tn = admin_data.convert(raw_TN).lower()
            # Get table_name in RS dict
            tn = rel_tn.replace("_has_couleur", "")

            # print(rel_tn, tn)

            # if the table not exist, we create it.
            if not sql.inTable(tn):
                sql.createTable(tn)
                sql.createCol(tn, "valeur", "VARCHAR(100)")

            if not sql.inTable(rel_tn):
                sql.createRelTable("nom", tn, rel_tn)

            # Adding value in table if not done yet.
            # print(data)
            # If value is list type
            if isinstance(data, list):
                t = []
                # check if each value not already in table
                for v in data:
                    if not sql.inRow(tn, v):
                        t.append(v)
                # Each data not in table append in list and reaffect to data var
                data = t
                if len(data) > 0:
                    sql.insert(tn, data)
                    for value in data:
                        print("nom", name, tn, value, rel_tn)
                        sql.nnfKey("nom", name, tn, value, rel_tn)
            elif not sql.inRow(tn, data):
                sql.insert(tn, data)
                sql.nnfKey("nom", name, tn, data, rel_tn)


        # processing of values in the primary table
        elif "Nom." in admin_data.convert(raw_TN):

            column_name = admin_data.convert(raw_TN).replace("Nom.", "").lower()
            # print(column_name, data)

            try:
                data = int(data.strip(" cm").strip(" au m²"))
                if not sql.inColumn("nom", column_name):
                    sql.createCol("nom", column_name, "INT", "UNSIGNED")
                    sql.update("nom", name, column_name, data)

            except ValueError:
                if not sql.inColumn("nom", column_name):
                    sql.createCol("nom", column_name, "VARCHAR(100)")
                    if column_name in ["taille_conseille"
                                       "mellifere"]:
                        sql.update("nom", name, column_name, "oui")
                    else:
                        sql.update("nom", name, column_name, data)
        else:
            # Get the relation table name too.
            tn = admin_data.convert(raw_TN).lower()

            if not sql.inTable(tn):
                sql.createTable(tn)
                sql.createCol(tn, "valeur", "VARCHAR(100)")

            # If value is list type
            if isinstance(data, list):
                t = []
                # check if each value not already in table
                for v in data:
                    if not sql.inRow(tn, v):
                        t.append(v)
                # Each data not in table append in list and reaffect to data var
                data = t
                if len(data) > 0:
                    sql.insert(tn, data)
                    for value in data:
                        sql.fKey("nom", name, tn, value)
            elif not sql.inRow(tn, data):
                sql.insert(tn, data)
                sql.fKey("nom", name, tn, data)
