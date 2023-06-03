import mysql.connector

class CheckDatabase:
    def __init__(self,host, user, password, database):
        # Connect to MySQL server
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        # Create a cursor to execute SQL statements
        cursor = db.cursor()
        
        # Execute query to fetch database names
        cursor.execute("SHOW DATABASES")
        
        # Fetch all the databases
        databases = cursor.fetchall()
        
        # Check if the desired database exists
        if (database.lower(),) in databases:
            cursor.execute(f"DROP SCHEMA IF EXISTS {database};")
            cursor.execute(f"CREATE SCHEMA {database};")
            print("Database '{}' deleted and remade".format(database))
        else:
            # Create the database
            cursor.execute("CREATE DATABASE {}".format(database))
            print("Database '{}' created successfully.".format(database))
        
        # Close the cursor and database connection
        cursor.close()
        db.close()
