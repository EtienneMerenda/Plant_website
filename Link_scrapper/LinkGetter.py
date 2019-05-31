# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import os
from pprint import pprint
import time

"""Scrpit used for get links in html page"""

file_list = os.listdir(os.getcwd()+"/html_page")
pprint(file_list)

link_dict = {}

for file in file_list:
    print(file)
    # getting each html page to found link in <a> tag
    with open("data/"+file, "r", encoding="latin-1") as html:
        soup = BeautifulSoup(html, "html5lib")
        # find list ul conatin links
        list_ul_with_link = soup.find("ul", attrs={"class": "products-grid"})
        # get a tags
        link_list = list_ul_with_link.find_all("a", attrs={"class": "product-image gua-add-product"})
        # adding each link un dictionary
        for a in link_list:
            try:
                link_dict[f"{file.replace('.html', '')}"].append(a["href"])
            except KeyError:
                link_dict[f"{file.replace('.html', '')}"] = [a["href"]]
        pprint(link_dict)
        print(len(link_list))

print(len(link_dict))

with open("all_link.txt", "w", encoding="utf-8") as file:
    for key, value in link_dict.items():
        value = [i+"\n" for i in value]
        print(key)
        print(value)
        file.write("\n")
        time.sleep(0.3)
        file.write(key)
        time.sleep(0.3)
        file.write("\n")
        time.sleep(0.3)
        file.writelines(value)
