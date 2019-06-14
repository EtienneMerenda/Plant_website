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
        self.errors = mysql.connector.errors

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

        #print("------", namedb)
        namedb = namedb.lower()
        self.dbName = namedb
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
        for dataBase in self.myCursor:
            if self.dataBaseList.count(dataBase[0]) == 0:
                self.dataBaseList.append(dataBase[0])

        return self.dataBaseList

    def useDB(self, namedb):
        self.myCursor.execute(f"USE {namedb};")
        self.dbName = namedb

# ------------------------------------------------------------------------------

    def createTable(self, name):
        """Method used to create a new tab with id column."""
        #print(name, "table created")
        self.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `{name}`"
                              f" (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                              f" PRIMARY KEY (`id`))")

    def createRelTable(self, primaryTable, childTable, tableName=""):
        """Create an relationnel table.
        primaryTable: primary table
        childTable: child table
        tableName: relation table name's (optional)"""

        self.myCursor.execute("SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;")
        self.myCursor.execute("SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;")
        self.myCursor.execute("SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';")

        if tableName == "":

            self.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `{primaryTable}_has_{childTable}` ("
                                    f"`{primaryTable}_id` INT UNSIGNED NOT NULL, "
                                    f"`{childTable}_id` INT UNSIGNED NOT NULL, "
                                    f"PRIMARY KEY (`{primaryTable}_id`, `{childTable}_id`), "
                                    f"INDEX `fk_{primaryTable}_has_{childTable}_{childTable}_idx` (`{childTable}_id` ASC) VISIBLE, "
                                    f"INDEX `fk_{primaryTable}_has_{childTable}_{primaryTable}_idx` (`{primaryTable}_id` ASC) VISIBLE, "
                                    f"CONSTRAINT `fk_{primaryTable}_has_{childTable}_{primaryTable}` "
                                      f"FOREIGN KEY (`{primaryTable}_id`) "
                                      f"REFERENCES `{self.dbName}`.`{primaryTable}` (`id`) "
                                      f"ON DELETE NO ACTION "
                                      f"ON UPDATE NO ACTION, "
                                    f"CONSTRAINT `fk_{primaryTable}_has_{childTable}_{childTable}` "
                                      f"FOREIGN KEY (`{childTable}_id`) "
                                      f"REFERENCES `{self.dbName}`.`{childTable}` (`id`) "
                                      f"ON DELETE NO ACTION "
                                      f"ON UPDATE NO ACTION) "
                                  "ENGINE = InnoDB;")

        else:
            self.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `{tableName}` ("
                                    f"`{primaryTable}_id` INT UNSIGNED NOT NULL, "
                                    f"`{childTable}_id` INT UNSIGNED NOT NULL, "
                                    f"PRIMARY KEY (`{primaryTable}_id`, `{childTable}_id`), "
                                    f"INDEX `fk_{tableName}_{childTable}_idx` (`{childTable}_id` ASC) VISIBLE, "
                                    f"INDEX `fk_{tableName}_{primaryTable}_idx` (`{primaryTable}_id` ASC) VISIBLE, "
                                    f"CONSTRAINT `fk_{tableName}_{primaryTable}` "
                                      f"FOREIGN KEY (`{primaryTable}_id`) "
                                      f"REFERENCES `{self.dbName}`.`{primaryTable}` (`id`) "
                                      f"ON DELETE NO ACTION "
                                      f"ON UPDATE NO ACTION, "
                                    f"CONSTRAINT `fk_{tableName}_{childTable}` "
                                      f"FOREIGN KEY (`{childTable}_id`) "
                                      f"REFERENCES `{self.dbName}`.`{childTable}` (`id`) "
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

        if columnName is None:
            columnName = self.checkColumn(tableName)[1]
        if isinstance(value, list) is False and isinstance(value, tuple) is False:
            # print(f'INSERT INTO {tableName} (`{columnName}`) VALUES ("{value}")')
            self.myCursor.execute(f'INSERT INTO {tableName} (`{columnName}`) VALUES ("{value}")')
            self.mydb.commit()
            print(self.myCursor.rowcount, f"record(s) inserted in '{tableName}': {value}")

        else:
            if isinstance(value, list):
                if isinstance(value[0], list):
                    n = len(value[0])
                else:
                    n = 0
                    value = [(i,) for i in value]
            elif isinstance(value, str):
                value = [(i,) for i in value]
                n = len(value) - 1
            if isinstance(columnName, tuple) or isinstance(columnName, list):
                columnName = f"{'`, `'.join(columnName)}"
                n = len(value[0]) - 1


            cmd = f"INSERT INTO {tableName.lower()} (`{columnName}`) VALUES ({'%s'+(', %s'*n)})"
            # print(cmd, value, type(value[0]))
            self.myCursor.executemany(cmd, value)
            self.mydb.commit()
            print(self.myCursor.rowcount, f"record(s) inserted in '{tableName}': {value}")

    def update(self, tableName, valueRef, columnName, value):

        valueRef = int(self.inRow(tableName, valueRef, "k"))

        # print(f"UPDATE {tableName} SET {columnName} = ('{value}') WHERE id = {valueRef}")
        self.myCursor.execute(f"UPDATE {tableName} SET {columnName} = ('{value}') WHERE id = {valueRef}")
        self.mydb.commit()
        print(self.myCursor.rowcount, f"record(s) modified in '{tableName}' with '{value}'")

    def fKey(self, primaryTable, valuePT, childTable, valueCT):

        iP = int(self.inRow(primaryTable, valuePT, "k"))
        iC = int(self.inRow(childTable, valueCT, "k"))

        if not self.inColumn(primaryTable, f"{childTable}_id"):
            self.createCol(primaryTable, f"{childTable}_id", "INT(10)", "UNSIGNED")
        # print(f"UPDATE {primaryTable} SET {childTable}_id = {iC} WHERE {self.checkColumn(primaryTable)[0]} = {iP}")
        self.myCursor.execute(f"UPDATE {primaryTable} SET {childTable}_id = {iC} WHERE {self.checkColumn(primaryTable)[0]} = {iP}")
        self.mydb.commit()
        print(self.myCursor.rowcount, f"key(s) was insered in '{primaryTable}' table.")

    def nnfKey(self, primaryTable, valuePT, childTable, valueCT, altTableName=None):

        if not self.inTable(primaryTable) or not self.inTable(childTable):
            if not self.inTable(primaryTable):
                raise ValueError(f"Table '{primaryTable}' not exist.")
            else:
                raise ValueError(f"Table '{childTable}' not exist.")

        iP = self.inRow(primaryTable, valuePT, "k")
        iC = self.inRow(childTable, valueCT, "k")

        #print(iP, iC)
        try:
            if altTableName != None:
                self.insert(f"{altTableName}", ((iP, iC),), (f"{primaryTable}_id", f"{childTable}_id"))
            else:
                # print(f"{primaryTable}_has_{childTable}", (iP, iC), (f"{primaryTable}_id", f"{childTable}_id"))
                self.insert(f"{primaryTable}_has_{childTable}", ((iP, iC),), (f"{primaryTable}_id", f"{childTable}_id"))
        except mysql.connector.errors.IntegrityError as e:
            print("Keys in many to many table not added: ", e)

    def checkRows(self, table, value=""):

        if value == "":
            self.myCursor.execute(f"SELECT * FROM {table};")
            row = self.myCursor.fetchall()
            return row

        else:
            #print(1, f"SELECT * FROM {table} WHERE {self.checkColumn(table)[1]}='{value}'")
            self.myCursor.execute(f"SELECT * FROM {table} WHERE {self.checkColumn(table)[1]}=%s", ((value,)))
            row = self.myCursor.fetchall()
            return row

# ------------------------------------------------------------------------------

    def inTable(self, name):
        """Return True if table already exist"""

        name = name.lower()
        if name in self.checkTable():
            return True
        else:
            return False

    def inColumn(self, tableName, name):
        """Return True if column already exist"""

        name = name.lower()
        if name in self.checkColumn(tableName):
            return True
        else:
            return False

    def inRow(self, tableName, value, p=False):
        """Return True if value is in row.
        If p = "k", return key of id row"""

        if len(self.checkRows(tableName, value)) > 0:
            if p is False:
                return True
            elif p == "k":
                return self.checkRows(tableName, value)[0][0]
        else:
            return False
