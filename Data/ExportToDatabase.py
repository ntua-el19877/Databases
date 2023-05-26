from calendar import c
from MySQLdb import OperationalError
import mysql.connector

class ExportToDatabase:
    def __init__(self,Data=True, DatabaseName="testDB1", file_path="Data/Data/mysql-db23-50-insert-data.sql"):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=DatabaseName
        )
        mycursor = db.cursor()

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                    sql_file=''
                    for i, line in enumerate(file):
                        sql_statement = line.strip()
                        if Data and sql_statement:  # Skip empty lines
                            if i % 500 == 0:
                                print(f'At {i} additions')
                            mycursor.execute(sql_statement)
                        elif (not Data) and (not sql_statement.startswith("--")):
                            #  print(sql_statement)
                             sql_file+=sql_statement
                    try:
                        if not Data:
                            sqlCommands = sql_file.split(';')
                            for i,sqlSt in enumerate(sqlCommands):
                                # print(sqlCommands[0])
                                if i % 5 == 0:
                                    print(f'At {i} additions')
                                try:
                                    mycursor.execute(sqlSt+';')
                                except:
                                    print(f"---------Error at {i}---------")
                    except:
                        print("Error occurred during SQL Schema insertion")

            db.commit()
            mycursor.close()
            db.close()
            print(f'Made {i} additions to the database')
        except mysql.connector.Error as err:
            print("Error occurred during SQL execution:")
