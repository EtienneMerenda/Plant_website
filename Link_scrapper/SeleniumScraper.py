# -*- coding: utf-8 -*-

"""Script used for get html page generated with AJAX method"""

# Use this script with geckodriver.exe and Firefox

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

urlList = ["https://www.promessedefleurs.com/bulbes-de-printemps.html",
           "https://www.promessedefleurs.com/bulbes-d-ete.html",
           "https://www.promessedefleurs.com/vivaces.html",
           "https://www.promessedefleurs.com/arbustes.html",
           "https://www.promessedefleurs.com/grimpantes.html",
           "https://www.promessedefleurs.com/rosiers.html",
           "https://www.promessedefleurs.com/annuelles.html",
           "https://www.promessedefleurs.com/potager.html",
           "https://www.promessedefleurs.com/fruitiers.html",
           ]


class Selenium():
    """Permet de descendre en bas de page et de récupérer la page html
     completement chargé"""

    def __init__(self, url):

        self.browser = webdriver.Firefox()
        self.browser.get(url)
        self.command = self.browser.find_element_by_tag_name("html")

    def scrapScript(self, path):
        """Get content of web page."""
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.browser.page_source)

    def pageDown(self):
        """Give 'endpage' command to navigator when it's not in a bottom of page."""
        end = False
        while end is False:
            try:
                # when is-none left not in html script, content still to load.
                self.browser.find_element_by_class_name("ias-noneleft")
                end = True
            except NoSuchElementException:
                self.command.send_keys(Keys.END)


for url in urlList:
    main = Selenium(url)
    main.pageDown()
    main.scrapScript(f"html_page/{url[33:]}")
