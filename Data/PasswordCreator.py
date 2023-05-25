import secrets
import bcrypt

path='Data/'

#Class that creates the appropriate password for its users
class PasswordCreator:
    def __init__(self,Users=500):
        output_file1 = path+"Data/Passwords.txt"
        output_file2 = path+"Data/Passwords.sql"

        self.removedata(output_file1)
        self.removedata(output_file2)

        for Userid in range(Users+1):
            Password=secrets.token_urlsafe(13)
            # Generate a salt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(Password.encode('utf-8'), salt)
            self.addPassword(output_file2,Userid,hashed_password.decode('utf-8'))
            self.savePassword(output_file1,Password,Userid)
            
    def removedata(self,output_file):
        with open(output_file, "w") as file:
            pass  # No need to write anything; the file will be emptied
        print("File contents erased:", output_file)


    def addPassword(output_file,Userid,hashed_password):
        with open(output_file, "a", encoding="utf-8") as file:
            file.write("Insert into Password\n")
            file.write("(`UserID`,`Hash`)\n")
            file.write("Values\n")
            file.write(f"('{Userid}','{hashed_password}')\n")
            file.write(";\n\n")

    def savePassword(output_file,Password,Userid):
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"UserID: {Userid} Password: {Password}\n")




