
from CheckDatabase import CheckDatabase
from Data_to_SQL import DataToSQL
from ExportToDatabase import ExportToDatabase


if(__name__ == "__main__"):
    path="Data/Data/"
    data_path=path+"mysql-db23-50-insert-data.sql"
    schema_path=path+"mysql-db23-50-schema.sql"
    Dbname="testdb1"
    host = "localhost"
    user = "root"
    password = ""

    CheckDatabase(host, user, password, Dbname)
    # DataToSQL(MakePasswords=False,FilesToOne=True,DatabaseName=Dbname)
    ExportToDatabase(False,Dbname,schema_path)
    ExportToDatabase(True,Dbname,data_path)