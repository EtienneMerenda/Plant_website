# encoding: utf-8

"""function used for get html and sort data"""

import requests
from bs4 import BeautifulSoup
from pprint import pprint


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

    #print(plant.name, checkName)

    del checkName

    # I take the html's part thats interests me

    raw_data = {"col2-md": soup.find("div", id="tabs-description").find("div", attrs={"class": "col2-md description"}),
                "col-right": soup.find("div", id="tabs-soins").find("div", attrs={"class": "col-right"})}

    for tag in raw_data.values():
        for li_tag in tag.find_all("li"):

            try:
                if li_tag.find("ul") is not None:
                    l = []
                    li_list = li_tag.find_all("li")
                    print(li_tag["class"][0])
                    for li_tag_ in li_list:
                        li = li_tag_.get_text(strip=True)
                        l.append(li)
                    setattr(plant, li_tag["class"][0], l)

                elif li_tag.find("h2") is not None:
                    try:
                        setattr(plant, li_tag["class"][0], li_tag.find("h2").get_text(strip=True).lower().replace("'", "''"))
                    except KeyError:
                        setattr(plant, li_tag["clas"][0], li_tag.find("h2").get_text(strip=True).lower().replace("'", "''"))
                else:
                    try:
                        setattr(plant, li_tag["class"][0], li_tag.find("span", class_="value").get_text(strip=True).lower().replace("'", "''"))
                    except KeyError:
                            setattr(plant, li_tag["clas"], li_tag.find("span", class_="value").get_text(strip=True).lower().replace("'", "''"))

            except (KeyError, AttributeError) as e:
                print(e)
        # Get complementary information
        try:
            setattr(plant, tag.find("p").parent.find("span", class_="title").get_text(strip=True), tag.find("p").get_text(strip=True).lower().replace("'", "''"))
        except AttributeError:
            pass

    pprint(plant.get_all())

    # I make list if the data traitement need and .strip() all useless whitespace.

    for key, value in plant.get_all().items():
        if "," in value and key != "Soins":
            setattr(plant, key, value.split(", "))
            setattr(plant, key, [i.strip() for i in getattr(plant, key)])

    # Adding key in table name dictionary for traitement.
    for key in plant.get_all().keys():

        # processing of data about month periods.
        if "periode" in key:
            if isinstance(getattr(plant, key), list):
                l = []
                for d in getattr(plant, key):
                    tmp = d.strip("de ").replace(" à ", "-").strip(".").lower().split("-")
                    l += tmp
                    date = conv.date_convert(l)
                    setattr(plant, key, date)

            else:
                #print(getattr(plant, key))
                date = getattr(plant, key).strip("de ").replace(" à ", "-").strip(".").lower().split("-")
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
                print(getattr(plant, key))
                data = getattr(plant, key).strip("de ").replace("à ", "").replace("et ", "").strip(".").replace(";", "").lower()
                setattr(plant, key, data)

    # Save table_name_reference
    conv.burn_RS()

    pprint(plant.get_all())
    #print(len(plant.get_all()))
    conv.RS_read()
