import mysql.connector
class ExportToDatabase:
    def __init__(DatabaseName="testDB1",file_path="Data/Data/mysql-db23-50-insert-data.sql"):
        db=mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database=DatabaseName
                )
        mycursor = db.cursor()

        with open(file_path, "r", encoding="utf-8") as file:
            for i,line in enumerate(file):
                sql_statement = line.strip()
                if sql_statement:  # Skip empty lines
                    if i%500==0:
                        print(f'At {i} additions')
                    mycursor.execute(sql_statement)
                    
        db.commit()
        mycursor.close()
        db.close()
        print(f'Made {i} additions to database')
