# encoding: utf-8

"""Class contains table converter and ignored data."""

import pickle
import os
from pprint import pprint


class Converter():

    def __init__(self):
        pass

    def rosetta_stone(self):
        """Get table conversion in extenal file"""
        try:
            with open("./RS/RS.dic", "rb") as file:
                self.RS = pickle.load(file)
                self.date = self.RS["_date"]
        except EOFError as e:
            print(e)
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
        with open("./RS/RS.dic", "wb") as file:
            pickle.dump(self.RS, file)

    def date_convert(self, date):
        """Convert month in numeric format."""
        for month in date:
            if month not in self.date.keys():
                m = input(f"What month number for {month}: ")
                self.date[month] = int(m)

        date_list = [self.date[i] for i in date]
        return date_list

    def table_convert(self, key):
        """Check if table name is in Rosetta Stone"""
        if key in self.RS["ignored"]:
            pass
        elif key not in self.RS.keys():
            s = ""
            while s != "y":
                ref = input(f"What table for '{key}': ")
                s = input(f"You are sure '{ref}' makes reference to '{key}' ? y/n ")
            self.RS[key] = ref

    def convert(self, key):
        """Return value of given key into rosetta stone if in. Else, adding it in."""
        try:
            return self.RS[key]
        except KeyError:
            self.table_convert(key)
            self.burn_RS()
            return self.RS[key]

    def ignored(self):
        """Return ignored list into RS."""
        return self.RS["ignored"]

    def RS_read(self):
        """Return RS dictionary."""
        return pprint(self.RS)
