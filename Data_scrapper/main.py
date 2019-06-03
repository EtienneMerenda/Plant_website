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

class DataAdmin():

    def __init__(self):
        pass

    def rosetta_stone(self):
        """Get table conversion in extenal file"""
        with open("table_name.dic", "rb") as file:
            self.table_name_reference = pickle.load(file)
            self.date = self.table_name_reference["__date__"]

    def burn_RS(self):
        """Save dictionary in external file called 'table_name.dic'"""
        self.table_name_reference["__date__"] = self.date
        with open("table_name.dic", "wb") as file:
            pickle.dump(self.table_name_reference, file)

    def date_convert(self, date):
        """Convert month in numeric format."""
        for month in date:
            if month not in self.date.keys():
                m = input(f"What month number for {month}: ")
                self.date[month] = int(m)

        date_list = [self.date[i] for i in date]
        return date_list


admin = DataAdmin()
admin.rosetta_stone()
r = requests.get("https://www.promessedefleurs.com/potager/plants-potagers/plants-greffes/pasteque-pata-negra-f1-en-plants.html")
soup = BeautifulSoup(r.text, "html5lib")

with open("table_name.dic", "rb") as file:
    table_name_reference = pickle.load(file)

table_name_reference_loaded = table_name_reference.copy()

# name

name = soup.find("div", attrs={"class": "product-name"}).find("h1").get_text(strip=True)

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
    if key in table_name_reference["ignored"]:
        pass
    elif key not in table_name_reference.keys():
        s = ""
        while s != "y":
            ref = input(f"What table for '{key}': ")
            s = input(f"You are sure '{ref}' makes reference to '{key}' ? y/n ")
        table_name_reference[key] = ref

    # processing of data about month periods.
    if "periode" in key:
        date = rafined_data[key].strip("de ").replace(" à ", "-").strip(".").lower().split("-")
        date = admin.date_convert(date)
        rafined_data[key] = date

# Save table_name_reference
admin.burn_RS()


pprint(rafined_data)
print(len(rafined_data))
