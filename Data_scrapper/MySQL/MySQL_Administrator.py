# -*- coding: utf-8 -*-

import mysql.connector
import json
from pprint import pprint


class MySQLAdministrator:
    """Object used for manage database"""

    def __init__(self):
        self.mydb = None
        self.myCursor = None
        self.dataBaseList = []
        self.TableList = []

        with open("sqlHelper.json", "r", encoding="utf-8") as file:
            self.sqlHelper = json.loads(file.read())
            print(self.sqlHelper)


    def link(self, user, password, host="localhost", db=None):
        """Method used to connect to the database."""

        self.mydb = mysql.connector.connect(host=host,
                                            user=user,
                                            passwd=password,
                                            database=db)
        self.myCursor = self.mydb.cursor()

    def createDB(self, namedb):
        """Method used to create a new database."""

        print(self.checkDB())
        if namedb not in self.checkDB():
            self.myCursor.execute(f"CREATE DATABASE {namedb};")
        else:
            r = ""
            while r not in ["n", "y"]:
                r = input("Database already exist, do you want drop it ? y/n ")
            if r == "y":
                self.myCursor.execute(f"DROP DATABASE {namedb};")
                self.myCursor.execute(f"CREATE DATABASE {namedb};")

    def checkDB(self):
        """Method used to check existing database."""

        self.myCursor.execute("SHOW DATABASES")

        for dataBase in self.myCursor:
            print(dataBase[0])
            if self.dataBaseList.count(dataBase[0]) == 0:
                self.dataBaseList.append(dataBase[0])

        return self.dataBaseList

# ------------------------------------------------------------------------------

    def createTable(self, name, type, primaryKey=None, id="key"):
        """Method used to create a new tab."""

        if primaryKey is True:
            self.myCursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({id} INT"
            f" UNSIGNED AUTO_INCREMENT PRIMARY KEY, {name} ")

        else:
            self.myCursor.execute(f"CREATE TABLE {name} (name VARCHAR(255),"
                              "address VARCHAR(255))")

        #  Primary Key with auto incrementation if primaryKey is True.

    def checkTable(self):
        """Method used to check existing tables."""

        self.myCursor.execute("SHOW TABLES")

        for table in self.myCursor:
            print(table)
            if self.TableList.count(table) == 0:
                self.TableList.append(table)

        return self.TableList

    def insert(self, name, value, IDCol):
        """Method used to insert a or many records in the table."""

        if isinstance(value, list):
            nbInsertion = ("%s, "*(len(value) - 1)) + "%s"
            cmd = f"INSERT INTO {name} ({IDCol}) VALUES ({nbInsertion})"
            self.myCursor.executemany(cmd, value)

        else:
            cmd = f"INSERT INTO {name} ({IDCol}) VALUES (%s)"
            self.myCursor.execute(cmd, value)

        self.mydb.commit()
        print(self.myCursor.rowcount, "was inserted")

    def checkRows(self):

        self.mysCursor.execute("")


sql = MySQLAdministrator()
