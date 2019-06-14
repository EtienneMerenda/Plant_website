# encoding: utf-8

# MySQLAdministrator for admin injection in my database.
from MySQL.MySQL_Administrator import MySQLAdministrator
# import connexion identification in external file registered in .gitignore.
from MySQL.connexion import user, password

def inject(plant, conv):
    # Connection to MySQL with my MySQLAdministrator classe
    path = "./MySQL"
    sql = MySQLAdministrator()
    sql.makeHelper("./MySQL/")
    sql.link(user, password)
    try:
        sql.useDB("plants")
    except sql.errors.ProgrammingError:
        sql.createDB("plants")

    # Create table "nom" if not exist (in first scrap)
    if not sql.inTable("nom"):
        sql.createTable("nom")
        sql.createCol("nom", "nom", "VARCHAR(100)", "UNIQUE NOT NULL")

    if not sql.inRow("nom", plant.name):
        sql.insert("nom", plant.name)

    for raw_TN, data in plant.get_all().items():

        # print(raw_TN, data)
        # We skip useless data: cultivar
        if raw_TN not in conv.ignored():

            #print("\n", raw_TN, conv.convert(raw_TN), data, "\n")

            if raw_TN == "name":
                pass

            # We work in Name to other table multi-relations.
            elif "Nom_has" in conv.convert(raw_TN):

                # Get the relation table name too.
                rel_tn = conv.convert(raw_TN).lower()
                # Get table_name in RS dict
                tn = rel_tn.replace("nom_has_", "")

                if len(data) > 99:
                    # print(sql.checkRows(tn))
                    data = input(data)

                # if the table not exist, we create it.
                if not sql.inTable(tn):
                    sql.createTable(tn)
                    sql.createCol(tn, "valeur", "VARCHAR(100)")
                    sql.createRelTable("nom", tn)

                # Adding value in table if not done yet.
                # #print(data)
                # If value is list type
                if isinstance(data, list):
                    t = []
                    # check if each value not already in table
                    for v in data:
                        if not sql.inRow(tn, v):
                            t.append(v)
                    # Each data not in table append in list and reaffect to data var
                    data = t
                    if len(data) > 0:
                        sql.insert(tn, data)
                        for value in data:
                            sql.nnfKey("nom", plant.name, tn, value)
                elif not sql.inRow(tn, data):
                    sql.insert(tn, data)
                    #print("nom", plant.name, tn, data)
                    sql.nnfKey("nom", plant.name, tn, data)

                else:
                    sql.nnfKey("nom", plant.name, tn, data)

            elif "Date" in conv.convert(raw_TN):

                date_dict = {1: "Janvier",
                            2: "Février",
                            3: "Mars",
                            4: "Avril",
                            5: "Mai",
                            6: "Juin",
                            7: "Juillet",
                            8: "Août",
                            9: "Septembre",
                            10: "Octobre",
                            11: "Novembre",
                            12: "Décembre"}

                # Get the relation table name too.
                rel_tn = conv.convert(raw_TN).lower()
                # Get table_name in RS dict
                tn = "date"

                #print(rel_tn, tn)

                # if the table not exist, we create it.
                if not sql.inTable(tn):
                    sql.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `Plants`.`Date` ( "
                                          "`id` INT UNSIGNED NOT NULL, "
                                          "`mois` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_bin' NOT NULL, "
                                          "PRIMARY KEY (`id`), "
                                          "UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE, "
                                          "UNIQUE INDEX `date_UNIQUE` (`mois` ASC) VISIBLE)")

                # if new date appears, we inject it.
                #print(conv.RS["_date"])

                    for nb, month in date_dict.items():
                        sql.insert("date", ((nb, month),), ("id", "mois"))

                # Create relational table.
                if not sql.inTable(rel_tn):
                    sql.myCursor.execute(f"CREATE TABLE IF NOT EXISTS `{rel_tn}` ("
                                            f"`nom_id` INT UNSIGNED NOT NULL, "
                                            f"`date_start_id` INT UNSIGNED NOT NULL, "
                                            f"`date_end_id` INT UNSIGNED NOT NULL, "
                                            f"PRIMARY KEY (`nom_id`, `date_start_id`, `date_end_id`), "
                                            f"INDEX `fk_Plantation_has_Date_Date1_idx` (`date_start_id` ASC) VISIBLE, "
                                            f"INDEX `fk_Plantation_has_Date_Date2_idx` (`date_end_id` ASC) VISIBLE, "
                                            f"CONSTRAINT `fk_{rel_tn}_Nom1` "
                                              f"FOREIGN KEY (`Nom_id`) "
                                              f"REFERENCES `Plants`.`Nom` (`id`) "
                                              f"ON DELETE NO ACTION "
                                              f"ON UPDATE NO ACTION, "
                                            f"CONSTRAINT `fk_{rel_tn}_Date1` "
                                              f"FOREIGN KEY (`date_start_id`) "
                                              f"REFERENCES `Plants`.`date` (`id`) "
                                              f"ON DELETE NO ACTION "
                                              f"ON UPDATE NO ACTION, "
                                            f"CONSTRAINT `fk_{rel_tn}_Date2` "
                                              f"FOREIGN KEY (`date_end_id`) "
                                              f"REFERENCES `Plants`.`date` (`id`) "
                                              f"ON DELETE NO ACTION "
                                              f"ON UPDATE NO ACTION) "
                                            f"ENGINE = InnoDB;")

                # Format date for insert in relational table row.
                iP = sql.inRow("nom", plant.name, "k")

                if len(data) % 2 == 0:

                    final_list_tuple = []
                    list_tuple = [iP]
                    for date_index in data:
                        list_tuple.append(date_index)
                        if len(list_tuple) == 3:
                            final_list_tuple.append(tuple(list_tuple))
                            list_tuple = [iP]

                    data = tuple(final_list_tuple)

                elif not len(data) % 2 == 0:

                    i = len(data)

                    final_list_tuple = []
                    list_tuple = [iP]
                    for date_index in data:
                        i -= 1
                        list_tuple.append(date_index)
                        if len(list_tuple) == 3:
                            final_list_tuple.append(tuple(list_tuple))
                            list_tuple = [iP]

                        elif i == 0:
                            list_tuple.append(date_index)
                            final_list_tuple.append(tuple(list_tuple))

                    data = tuple(final_list_tuple)

                try:
                    sql.insert(rel_tn, data, ("nom_id", "date_start_id", "date_end_id"))
                except sql.errors.IntegrityError as e:
                    print(e)
                # If value is list type

            elif "Couleur" in conv.convert(raw_TN):

                # Get the relation table name too.
                rel_tn = conv.convert(raw_TN).lower()
                # Get table_name in RS dict
                tn = rel_tn.replace("_has_couleur", "")

                #print(rel_tn, tn)

                # if the table not exist, we create it.
                if not sql.inTable("couleur"):
                    sql.createTable("couleur")
                    sql.createCol("couleur", "valeur", "VARCHAR(100)")

                if not sql.inTable(rel_tn):
                    sql.createRelTable("nom", "couleur", rel_tn)

                # Adding value in table if not done yet.
                #print(data)
                # If value is list type
                if isinstance(data, list):
                    t = []
                    # check if each value not already in table
                    for v in data:
                        if not sql.inRow("couleur", v):
                            t.append(v)
                    # Each data not in table append in list and reaffect to data var
                    data = t
                    if len(data) > 0:
                        sql.insert("couleur", data)
                        for value in data:
                            #print("nom", plant.name, "couleur", value, rel_tn)
                            sql.nnfKey("nom", plant.name, "couleur", value, rel_tn)
                elif not sql.inRow("couleur", data.strip("-").strip(".")):
                    sql.insert("couleur", data.strip("-").strip("."))
                    sql.nnfKey("nom", plant.name, "couleur", data.strip("-").strip("."), rel_tn)

            # processing of values in the primary table
            elif "Nom." in conv.convert(raw_TN):

                column_name = conv.convert(raw_TN).replace("Nom.", "").lower()
                try:
                    data = float(data.strip(" cm").strip(" au m²").strip(" jours"))
                    if not sql.inColumn("nom", column_name):
                        sql.createCol("nom", column_name, "INT", "UNSIGNED")
                        sql.update("nom", plant.name, column_name, data)
                    else:
                        sql.update("nom", plant.name, column_name, data)

                except ValueError:
                    if not sql.inColumn("nom", column_name):
                        sql.createCol("nom", column_name, "VARCHAR(100)")
                        if column_name in ["taille_conseille"
                                           "mellifere"]:
                            sql.update("nom", plant.name, column_name, "oui")
                        else:
                            sql.update("nom", plant.name, column_name, data)
                    else:
                        if column_name in ["taille_conseille"
                                           "mellifere"]:
                            sql.update("nom", plant.name, column_name, "oui")
                        else:
                            sql.update("nom", plant.name, column_name, data)

            else:
                # Get the relation table name too.
                tn = conv.convert(raw_TN).lower()

                if "info" in tn:
                    if not sql.inTable(tn):
                        sql.createTable(tn)
                        sql.createCol(tn, "valeur", "TEXT")

                    # data = data.replace('"', "''")

                if not sql.inTable(tn):
                    sql.createTable(tn)
                    sql.createCol(tn, "valeur", "VARCHAR(100)")

                # If value is list type
                if isinstance(data, list):
                    t = []
                    # check if each value not already in table
                    for v in data:
                        if not sql.inRow(tn, v):
                            t.append(v)
                    # Each data not in table append in list and reaffect to data var
                    data = t
                    if len(data) > 0:
                        sql.insert(tn, data)
                        for value in data:
                            sql.fKey("nom", plant.name, tn, value)
                elif not sql.inRow(tn, data):
                    sql.insert(tn, data.replace('"', '\"'))
                    sql.fKey("nom", plant.name, tn, data)
                else:
                    sql.fKey("nom", plant.name, tn, data)
