
from CheckDatabase import CheckDatabase
from Data_to_SQL import DataToSQL
from ExportToDatabase import ExportToDatabase
from config import info_data

path=info_data["path"]
data_path=path+info_data["data_file"]
schema_path=path+info_data["schema_file"]
Dbname=info_data["database"]
host = info_data["host"]
user = info_data["user"]
password = info_data["password"]
data_single_files=info_data["data_single_files"]

if(__name__ == "__main__"):
    CheckDatabase(host, user, password, Dbname)
    DataToSQL(MakePasswords=False,FilesToOne=False,DatabaseName=Dbname)
    ExportToDatabase(False,Dbname,schema_path)
    
    # ExportToDatabase(True,Dbname,path+data_single_files[7])
    for file in data_single_files:
        ExportToDatabase(True,Dbname,path+file)