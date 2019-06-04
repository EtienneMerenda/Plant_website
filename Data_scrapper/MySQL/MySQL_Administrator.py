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

    def makeHelper(self, path):
        """Need to give the MySQL folder path to create sqlHelper."""
        with open(f"{path}sqlHelper.json", "r", encoding="utf-8") as file:
            self.sqlHelper = json.loads(file.read())

    def link(self, user, password, host="localhost", db=None):
        """Method used to connect to the database."""

        self.dbName = db
        self.mydb = mysql.connector.connect(host=host,
                                            user=user,
                                            passwd=password,
                                            database=db)
        self.myCursor = self.mydb.cursor(buffered=True)

    def createDB(self, namedb):
        """Method used to create a new database."""

        print("------", namedb)
        namedb = namedb.lower()
        if namedb not in self.checkDB():
            self.myCursor.execute(f"CREATE DATABASE {namedb} CHARACTER SET utf8;")
            self.myCursor.execute(f"USE {namedb};")
        else:
            r = ""
            while r not in ["n", "y"]:
                r = input("Database already exist, do you want drop it ? y/n ")
            if r == "y":
                self.myCursor.execute(f"DROP DATABASE {namedb};")
                self.myCursor.execute(f"CREATE DATABASE {namedb} CHARACTER SET utf8;")
                self.myCursor.execute(f"USE {namedb};")
            else:
                self.myCursor.execute(f"USE {namedb};")

    def checkDB(self):
        """Method used to check existing database."""

        self.myCursor.execute("SHOW DATABASES;")
        print("Burn after reading")
        for dataBase in self.myCursor:
            if self.dataBaseList.count(dataBase[0]) == 0:
                self.dataBaseList.append(dataBase[0])

        return self.dataBaseList

# ------------------------------------------------------------------------------

    def createTable(self, name):
        """Method used to create a new tab with id column."""
        print(name, "table created")
        self.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `{name}`"
                              f" (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                              f" PRIMARY KEY (`id`))")

    def createRelTable(self, primT, childT, tableName=""):
        """Create an relationnel table.
        primT: primary table
        childT: child table
        tableName: relation table name's (optional)"""

        self.myCursor.execute("SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;")
        self.myCursor.execute("SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;")
        self.myCursor.execute("SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';")

        if tableName == "":

            self.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `{primT}_has_{childT}` ("
                                    f"`{primT}_id` INT UNSIGNED NOT NULL, "
                                    f"`{childT}_id` INT UNSIGNED NOT NULL, "
                                    f"PRIMARY KEY (`{primT}_id`, `{childT}_id`), "
                                    f"INDEX `fk_{primT}_has_{childT}_{childT}_idx` (`{childT}_id` ASC) VISIBLE, "
                                    f"INDEX `fk_{primT}_has_{childT}_{primT}_idx` (`{primT}_id` ASC) VISIBLE, "
                                    f"CONSTRAINT `fk_{primT}_has_{childT}_{primT}` "
                                      f"FOREIGN KEY (`{primT}_id`) "
                                      f"REFERENCES `{self.dbName}`.`{primT}` (`id`) "
                                      f"ON DELETE NO ACTION "
                                      f"ON UPDATE NO ACTION, "
                                    f"CONSTRAINT `fk_{primT}_has_{childT}_{childT}` "
                                      f"FOREIGN KEY (`{childT}_id`) "
                                      f"REFERENCES `{self.dbName}`.`{childT}` (`id`) "
                                      f"ON DELETE NO ACTION "
                                      f"ON UPDATE NO ACTION) "
                                  "ENGINE = InnoDB;")

        else:
            self.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `{tableName}` ("
                                    f"`{primT}_id` INT UNSIGNED NOT NULL, "
                                    f"`{childT}_id` INT UNSIGNED NOT NULL, "
                                    f"PRIMARY KEY (`{primT}_id`, `{childT}_id`), "
                                    f"INDEX `fk_{primT}_has_{childT}_{childT}_idx` (`{childT}_id` ASC) VISIBLE, "
                                    f"INDEX `fk_{primT}_has_{childT}_{primT}_idx` (`{primT}_id` ASC) VISIBLE, "
                                    f"CONSTRAINT `fk_{primT}_has_{childT}_{childT}` "
                                      f"FOREIGN KEY (`{primT}_id`) "
                                      f"REFERENCES `{self.dbName}`.`{primT}` (`id`) "
                                      f"ON DELETE NO ACTION "
                                      f"ON UPDATE NO ACTION, "
                                    f"CONSTRAINT `fk_{primT}_has_{childT}_{childT}` "
                                      f"FOREIGN KEY (`{childT}_id`) "
                                      f"REFERENCES `{self.dbName}`.`{childT}` (`id`) "
                                      f"ON DELETE NO ACTION "
                                      f"ON UPDATE NO ACTION) "
                                  "ENGINE = InnoDB;")

        self.myCursor.execute("SET SQL_MODE=@OLD_SQL_MODE;")
        self.myCursor.execute("SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;")
        self.myCursor.execute("SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;")

    def checkTable(self):
        """Method used to check existing tables."""

        self.myCursor.execute("SHOW TABLES")

        for table in self.myCursor:
            if self.TableList.count(table[0]) == 0:
                self.TableList.append(table[0])

        return self.TableList

# ------------------------------------------------------------------------------

    def createCol(self, tableName, columnName, type_col, parameter=""):
        """Method for create column in existing table"""

        self.myCursor.execute(f"ALTER TABLE {tableName} "
                              f"ADD COLUMN {columnName} {type_col} {parameter};")

    def checkColumn(self, table):
        """Method used for get column name of table"""

        self.myCursor.execute(f"SELECT * FROM {table};")
        columnName = [i[0] for i in self.myCursor.description]

        return columnName

# ------------------------------------------------------------------------------

    def insert(self, tableName, value, columnName=None):
        """Method used to insert a or many records in the table."""

        print(tableName)
        print(value)

        if columnName is None:
            columnName = self.checkColumn(tableName)[1]
        print(columnName)
        if isinstance(value, list) is False:
            self.myCursor.execute(f'INSERT INTO {tableName} (`{columnName}`) VALUES ("{value}")')

        else:
            for values in value:
                self.myCursor.execute(f'INSERT INTO {tableName.lower()} (`{columnName}`) VALUES ("{values}")')

    def checkRows(self, table):

        self.myCursor.execute(f"SELECT * FROM {table};")
        return self.myCursor.fetchall()

# ------------------------------------------------------------------------------

    def checkInTable(self, name):
        """Return True if table already exist"""

        name = name.lower()
        if name in self.checkTable():
            return True
        else:
            return False

    def checkInColumns(self, name, tableName):
        """Return True if column already exist"""

        name = name.lower()
        if name in self.checkColumn(tableName):
            return True
        else:
            return False

    def checkInRow(self, value, tableName):
        """Return True if value is in row"""

        print(value)
        print(self.checkRows(tableName))

        if value in [i[1] for i in self.checkRows(tableName)]:
            return True
        else:
            return False
