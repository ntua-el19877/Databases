import mysql.connector


db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdatabases" 
)

mycursor=db.cursor()

# mycursor.execute("CREATE DATABASE testdatabases")

# Retrieve all table names in the database
mycursor.execute("SHOW TABLES")
tables = [table[0] for table in mycursor]

# Truncate and drop each table in the database
for table in tables:
    mycursor.execute(f"TRUNCATE TABLE {table}")
    mycursor.execute(f"DROP TABLE {table}")

SchoolInfo=''
SchoolInfo+='SchoolID int PRIMARY KEY AUTO_INCREMENT,'
SchoolInfo+='SchoolName VARCHAR(50), '
SchoolInfo+='Address VARCHAR(50), '
SchoolInfo+='City VARCHAR(50),'
SchoolInfo+='PhoneNumber '   
mycursor.execute("CREATE TABLE IF NOT EXISTS School (%s)",SchoolInfo)



def insert_summary_with_list(book_id, school_id, values):
    connection = mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    cursor = connection.cursor()

    # Insert into Summary table
    sql_summary = "INSERT INTO Summary (BookID, SchoolID) VALUES (%s, %s)"
    values_summary = (book_id, school_id)
    cursor.execute(sql_summary, values_summary)

    # Get the generated SummaryID
    summary_id = cursor.lastrowid

    # Insert list elements into ListElement table
    sql_list_element = "INSERT INTO ListElement (SummaryID, Value) VALUES (%s, %s)"
    values_list_element = [(summary_id, value) for value in values]
    cursor.executemany(sql_list_element, values_list_element)

    connection.commit()
    cursor.close()
    connection.close()

    print("Summary with list inserted successfully.")

# Example usage
# insert_summary_with_list(1, 1, [1, 2])


mycursor.close()
db.close()