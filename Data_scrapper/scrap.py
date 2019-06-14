# encoding: utf-8

"""function used for get html and sort data"""

import requests
from bs4 import BeautifulSoup
from pprint import pprint


def split_bracket(str):
    """function used to split out brackets"""

    bracket = False
    str = str.split(" ")

    format_str = []

    for piece in str:
        if "(" in piece:
            bracket = True
        if ")" in piece:
            bracket = False
        if bracket is False:
            piece = piece.replace("et", "*").replace(",", "*")
        format_str.append(piece)

    format_str = " ".join(format_str)
    format_str = format_str.split("*")
    format_str = [i.strip().replace(".", "") for i in format_str]

    return format_str


def scrap(link, plant, conv):

    # Dl webpage
    r = requests.get(link)

    # Parsing page
    soup = BeautifulSoup(r.text, "html5lib")

    # I get name in tag div with product-name class and in title tag and compare them.
    name = soup.find("div", attrs={"class": "product-name"}).find("h1").get_text(strip=True)
    checkName = soup.find("title").get_text(strip=True)

    name = name.split(" ")
    checkName = checkName.split(" ")

    plant.name = " ".join([i for i in name if i in checkName])

    print(plant.name, checkName)

    del checkName

    # I take the html's part thats interests me

    raw_data = {"col2-md": soup.find("div", id="tabs-description").find("div", attrs={"class": "col2-md description"}),
                "col-right": soup.find("div", id="tabs-soins").find("div", attrs={"class": "col-right"})}

    for tag in raw_data.values():
        if tag is not None:
            for li_tag in tag.find_all("li"):

                try:
                    if li_tag.find("ul") is not None:
                        l = []
                        li_list = li_tag.find_all("li")
                        # print(li_tag["class"][0])
                        for li_tag_ in li_list:
                            li = li_tag_.get_text(strip=True)
                            l.append(li)
                        setattr(plant, li_tag["class"][0], l)

                    elif li_tag.find("h2") is not None:
                        try:
                            setattr(plant, li_tag["class"][0], li_tag.find("h2").get_text(strip=True).lower().replace("'", "''").replace('"', "''"))
                        except KeyError:
                            setattr(plant, li_tag["clas"][0], li_tag.find("h2").get_text(strip=True).lower().replace("'", "''").replace('"', "''"))
                    else:
                        try:
                            setattr(plant, li_tag["class"][0], li_tag.find("span", class_="value").get_text(strip=True).lower().replace("'", "''").replace('"', "''"))
                        except KeyError:
                                setattr(plant, li_tag["clas"], li_tag.find("span", class_="value").get_text(strip=True).lower().replace("'", "''").replace('"', "''"))

                except (KeyError, AttributeError) as e:
                    print(e)
            # Get complementary information
            try:
                setattr(plant, tag.find("p").parent.find("span", class_="title").get_text(strip=True), tag.find("p").get_text(strip=True).lower().replace("'", "''").replace('"', "''"))
            except AttributeError:
                pass

    # I make list if the data traitement need and .strip() all useless whitespace.
    for key, value in plant.get_all().items():
        # print(f"{key}, {value}")
        if key == "name":
            pass
        elif key == "specificite_substrat" or key == "drainage_humidite":
            # Faire en sorte que lorsque paraenthèse ouverte, pas de split par virgule
            # print(value)
            value = split_bracket(value)
            setattr(plant, key, value)

        elif "," in value and key not in ["Soins", "rusticite", "Floraison", "Feuillage", "drainage", "autofertile"]:

            setattr(plant, key, split_bracket(value))

        elif key == "rusticite":
            setattr(plant, key, value.replace("zone de rusticité usda", "").split(", "))
            setattr(plant, key, [i.strip() for i in getattr(plant, key)])
        else:
            if isinstance(value, list):
                setattr(plant, key, [i.strip("., ") for i in value])
            else:
                setattr(plant, key, value.strip("., "))

    # Adding key in table name dictionary for traitement.
    for key in plant.get_all().keys():

        # processing of data about month periods.
        if "periode" in key:
            if isinstance(getattr(plant, key), list):
                l = []
                for d in getattr(plant, key):
                    tmp = d.replace("de", "").replace("en", "").replace("à", "*").replace(".", "").replace(" ", "").lower().split("*")
                    l += tmp
                    date = conv.date_convert(l)
                    setattr(plant, key, date)

            else:
                #print(getattr(plant, key))
                date = getattr(plant, key).replace("de", "").replace("en", "").replace("à", "*").replace(".", "").replace(" ", "").lower().split("*")
                date = conv.date_convert(date)
                setattr(plant, key, date)

        elif "couleur" in key:
            if isinstance(getattr(plant, key), list):
                l = []
                for d in getattr(plant, key):
                    tmp = d.replace("à ", "").replace("et ", "").replace("-", "").replace(";", "").lower()
                    l.append(tmp)
                setattr(plant, key, l)

            else:
                data = getattr(plant, key).strip("de ").replace("à ", "").replace("et ", "").strip(".").replace(";", "").lower()
                setattr(plant, key, data)

        elif "autres_noms_communs" in key:
            if " - " in getattr(plant, key):
                setattr(plant, key, getattr(plant, key).split(" - "))


    # Save table_name_reference
    conv.burn_RS()

    #pprint(plant.get_all())
    #print(len(plant.get_all()))
