# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class Soup():

    def __init__(self, data=None, path=None):
        """Give data or path when you initialze object."""
        if path is not None:
            with open(path, "r", encoding="utf-8") as file:
                self.soup = BeautifulSoup(file, "html5lib")
        elif data is not None:
            self.soup = BeautifulSoup(data, "html5lib")
        self.dataList = []

    def __repr__(self):
        print(self.soup.text)

    def getSoup(self):
        """Return the soup object"""
        return self.soup

    def find(self, bal, attrs=None, soup=None):
        """Method used to find into the Soup
        'bal' the beacon to find.
        'attrs' the attribut to find => attrs={"id": "value"}.
        'soup' put your soup if you want.
        """
        if soup is None:
            if attrs is None:
                searchResult = self.soup.find(bal)
            else:
                searchResult = self.soup.find(bal, attrs)
        else:
            if attrs is None:
                searchResult = soup.find(bal)
            else:
                searchResult = soup.find(bal, attrs)
        return searchResult

    def find_all(self, bal, attrs=None, soup=None):
        """Method use to find all occurence of beacon.
        'bal' the beacon to find
        'soup' put your soup if you want."""

        if soup is None:
            if attrs is None:
                searchResult = self.soup.find_all(bal)
            else:
                searchResult = self.soup.find_all(bal, attrs)
        else:
            if attrs is None:
                searchResult = soup.find_all(bal)
            else:
                searchResult = soup.find_all(bal, attrs)

        return searchResult

    def scrap(self, path):
        """Method use to scrap some information and put them in file
        'path' give the path of the file where to save."""

        with open(path, "w", encoding="utf-8") as file:
            file.write("\n".join(self.dataList))
