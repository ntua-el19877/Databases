import secrets

import bcrypt


path='C:/Users/Aggelos/Documents/GitHub/Databases/Data/'



def removedata(output_file):
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

output_file4 = path+"Data/Passwords.txt"
output_file5 = path+"Data/Passwords.sql"

removedata(output_file4)
removedata(output_file5)

for Userid in range(501):
    Password=secrets.token_urlsafe(13)
    # Generate a salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(Password.encode('utf-8'), salt)
    addPassword(output_file5,Userid,hashed_password.decode('utf-8'))
    savePassword(output_file4,Password,Userid)


