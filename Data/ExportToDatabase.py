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
                    try:
                        for i, line in enumerate(file):
                            sql_statement = line.strip()
                            if Data and sql_statement:  # Skip empty lines
                                if i % 5000 == 0 and i>0:
                                    print(f'At {i} additions from {file_path}')
                                mycursor.execute(sql_statement)
                            elif (not Data) and (not sql_statement.startswith("--")):
                                #  print(sql_statement)
                                sql_file+=sql_statement
                    except:
                        print(f"---------Error occurred when going through file: at {i} from {file_path}---------")
                    try:
                        if not Data:
                            sqlCommands = sql_file.split(';')
                            for i,sqlSt in enumerate(sqlCommands):
                                # print(sqlCommands[0])
                                if i % 5 == 0:
                                    print(f'At {i} additions from {file_path}')
                                try:
                                    mycursor.execute(sqlSt+';')
                                except:
                                    print(f"---------Error at {i}---------")
                                
                    except:
                        print(f"---------Error occurred during SQL Schema insertion from {file_path}---------")

            db.commit()
            mycursor.close()
            db.close()
            print(f'    Made {i} additions to the database')
        except mysql.connector.Error as err:
            print(f"---------Error occurred during SQL execution: at {i} from {file_path}---------")
