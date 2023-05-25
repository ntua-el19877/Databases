ovedata(output_file4)
removedata(output_file5)

for Userid in range(501):
    Password=secrets.token_urlsafe(13)
    # Generate a salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(Password.encode('utf-8'), salt)
    addPassword(output_file5,Userid,hashed_password.decode('utf-8'))
    savePasswor