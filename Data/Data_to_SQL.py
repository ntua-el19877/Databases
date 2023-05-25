import datetime
import os
import random
from numpy import split
import requests
import json
import names
import re
import codecs
import secrets
import time
import bcrypt
import pymysql

# path='/home/angelos/Documents/GitHub/Databases/'
path='C:/Users/Aggelos/Documents/GitHub/Databases/Data/'

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%d/%m/%Y %I:%M %p', prop)

def removedata(output_file):
    with open(output_file, "w") as file:
        pass  # No need to write anything; the file will be emptied
    print("File contents erased:", output_file)

def book_to_text():
    input_file = path+"output.json"
    output_file1 = path+"Data/Book.sql"
    output_file2 = path+"Data/Author.sql"
    output_file3 = path+"Data/Keyword.sql"
    output_file4 = path+"Data/Summary.sql"
    output_file5 = path+"Data/Category.sql"
    output_file6 = path+"Data/Image.sql"
    removedata(output_file2)
    removedata(output_file3)
    removedata(output_file4)
    removedata(output_file5)
    removedata(output_file6)

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file1, "w", encoding="utf-8") as file:
        #5 schools
        Auth=[]
        Cat=[]
        Sum=[]
        Key=[]
        Ima=[]
        book_id=1
        for SchoolID in range(1,6):
            
            #get all possible books

            for i, book in enumerate(data):
                #add 0-3 books to the school
                for j in range(random.randint(0,3)):
                    title = replace_special_characters(book.get("title", "*"))
                    publisher = replace_special_characters(book.get("publisher", "*"))
                    isbn = str(book.get("isbn", "*"))
                    num_of_pages = book.get("pageCount", "*")
                    inventory = book.get("Inventory", "True")
                    image = book.get("thumbnail", "*")
                    language = replace_special_characters(book.get("language", "*"))
                    file.write("Insert into Book\n")
                    file.write("(`BookID`,`SchoolID`,`Title`,`Publisher`,`ISBN`,`NumOfPages`,`Inventory`,`Language`)\n")
                    file.write("Values\n")
                    file.write(f"('{book_id}','{SchoolID}','{title}','{publisher}','{isbn}','{num_of_pages}',{inventory},'{language}')\n")
                    file.write(";\n\n")
                    Auth=addAuthor(isbn,book,output_file2,Auth)
                    Key=addKeyword(output_file3,book,isbn,Key)
                    Sum=addSummary(output_file4,book,isbn,Sum)
                    Cat=addCategory(output_file5,book,isbn,Cat)
                    Ima=addImage(output_file6,image,isbn,Ima)
                    # addAuthor(SchoolID,book_id,book,output_file2)
                    # addKeyword(output_file3,book,book_id,SchoolID)
                    # addSummary(output_file4,book,book_id,SchoolID)
                    # addCategory(output_file5,book,book_id,SchoolID)
                    book_id+=1

    print("Data exported")



def addImage(output_file,image,isbn,L):
    if not isbn in L:
        with open(output_file, "a", encoding="utf-8") as file:
            file.write("Insert into Image\n")
            file.write("(`ISBN`,`ImageLink`)\n")
            file.write("Values\n")
            file.write(f"('{isbn}','{image}')\n")
            file.write(";\n\n")
        L.append(isbn)
    return L


def addAuthor(isbn,book,output_file,L):
    if not isbn in L:
        with open(output_file, "a", encoding="utf-8") as file:
            authors=book.get("authors")
            for j,auth in enumerate(authors):
                file.write("Insert into Author\n")
                file.write("(`ISBN`,`AuthorName`)\n")
                file.write("Values\n")
                file.write(f"({isbn},'{replace_special_characters(auth)}')\n")
                file.write(";\n\n")
        L.append(isbn)
    return L

def addKeyword(output_file,book,isbn,L):
    if not isbn in L:
        with open(output_file, "a", encoding="utf-8") as file:
            categories=book.get("keywords")
            for j,categ in enumerate(categories):
                file.write("Insert into Keyword\n")
                file.write("(`ISBN`,`KeywordName`)\n")
                file.write("Values\n")
                file.write(f"('{isbn}','{replace_special_characters(categ)}')\n")
                file.write(";\n\n")
        L.append(isbn)
    return L

def addSummary(output_file,book,isbn,L):
    if not isbn in L:
        with open(output_file, "a", encoding="utf-8") as file:
            summary=book.get("summary")
            file.write("Insert into Summary\n")
            file.write("(`ISBN`,`Summary`)\n")
            file.write("Values\n")
            file.write(f"('{isbn}','{replace_special_characters(summary)}')\n")
            file.write(";\n\n")
        L.append(isbn)
    return L

def addCategory(output_file,book,isbn,L):
    if not isbn in L:
        with open(output_file, "a", encoding="utf-8") as file:
                categories=book.get("categories")
                for j,categ in enumerate(categories):
                        file.write("Insert into Category\n")
                        file.write("(`ISBN`,`CategoryName`)\n")
                        file.write("Values\n")
                        file.write(f"('{isbn}','{replace_special_characters(categ)}')\n")
                        file.write(";\n\n")
        L.append(isbn)
    return L
#########################################

def user_to_text():
    
    output_file = path+"Data/User.sql"
    output_file2 = path+"Data/Reservation.sql"
    output_file3 = path+"Data/Review.sql"
    output_file4 = path+"Data/School.sql"
    removedata(output_file4)
    removedata(output_file2)
    removedata(output_file3)
    with open(output_file, "w", encoding="utf-8") as file:
        #5 schools
        Userid=1
        for i in range(5):
            #100 people in school
            resID=1
            L=[]
            reviewid=1
            for j in range(100):
                Roles=['Professor',"Student",
                    'Student','Student','Student',
                    'Student','Student','Student',
                    'Student','Professor']
                Role=random.choice(Roles)
                FirstName=names.get_first_name()
                Username=FirstName+str(random.randint(100, 999))
                LastName=names.get_last_name()
                BorrowerCard=random.randint(10**12, (10**13)-1)
                if j==98:
                    Role='Operator'
                    school_to_text(output_file4,FirstName+' '+LastName,i+1)
                elif j==99:
                    Role='Administrator'
                file.write("Insert into User\n")
                file.write("(`UserID`,`SchoolID`,`Username`,`Role`,`FirstName`,`LastName`,`BorrowerCard`)\n")
                file.write("Values\n")
                file.write(f"('{Userid}','{i+1}','{Username}','{Role}','{FirstName}','{LastName}','{BorrowerCard}')\n")
                file.write(";\n\n")
                if random.randint(0, 5)==0:
                    reviewid=addReview(output_file3,Userid,i+1,reviewid)
                if random.randint(0, 5)==0:
                    L,resID=addReservation(output_file2,Userid,i+1,resID,L)
                Userid+=1
    print("Data exported to", output_file)
    print(f'We have Users from 1 to {Userid-1}')


def school_to_text(output_file,lib_operator,SchoolID):

    with open(output_file, "a", encoding="utf-8") as file:
        Fir=['Cape Coral','Riverdale','Pinewood','Lakewood','Livanates']
        Sec=['Institute','School of Fine Arts','High','Technical School']
        SchoolName=random.choice(Fir)+' '+random.choice(Sec)
        Fir=['2969 Charmaine Lane','2537 Commerce Boulevard','2066 North Bend River Road']
        Sec=['Patricia','Paris','Somerset']
        Thi=['79373','68669','78234']
        Address=random.choice(Fir)+','+random.choice(Thi)
        City=random.choice(Sec)
        PhoneNumber=random.randint(6_970_000_000, 6_979_999_999)
        Email=SchoolName+'@'+'mail.com'
        SchoolDirectorFullName=names.get_full_name()
        file.write("Insert into School\n")
        file.write("(`SchoolID`,`SchoolName`,`Address`,`City`,`PhoneNumber`,`Email`,`SchoolLibraryOperatorFullName`,`SchoolDirectorFullName`)\n")
        file.write("Values\n")
        file.write(f"('{SchoolID}','{SchoolName}','{Address}','{City}','{PhoneNumber}','{Email}','{lib_operator}','{SchoolDirectorFullName}')\n")
        file.write(";\n\n")



def addReservation(output_file,userid,schoolid,ReservationID,L):
    with open(output_file, "a", encoding="utf-8") as file:

        for i in range(random.randint(1,5)):
            ReservationDate,_,_=random_date("24/5/2023 1:30 PM", "15/6/2023 4:50 AM", random.random()).split(' ')
            u = datetime.datetime.strptime(ReservationDate,"%d/%m/%Y")
            d = datetime.timedelta(days=7)
            nowDate=datetime.datetime.strptime("4/6/2023","%d/%m/%Y")
            ExpirationDate = u + d
            if ExpirationDate<nowDate:
                Active="Inactive"
            else:
                Active="Active"
            
            while True:
                bookid=random.randint(1,500)
                if not bookid in L:
                    L.append(bookid)
                    break
            us,_=str(u).split(' ')
            ExpirationDates,_=str(ExpirationDate).split(' ')

            file.write("Insert into Reservation\n")
            file.write("(`ReservationID`,`SchoolID`,`UserID`,`BookID`,`ReservationDate`,`ExpirationDate`,`Active`)\n")
            file.write("Values\n")
            file.write(f"('{ReservationID}','{schoolid}','{userid}','{bookid}','{us}','{ExpirationDates}','{Active}')\n")
            file.write(";\n\n")
            ReservationID+=1
    return L,ReservationID

def addReview(output_file,userid,schoolid,ReviewID):
    with open(output_file, "a", encoding="utf-8") as file:

        for i in range(random.randint(1,5)):
            bookid=random.randint(1,500)
            Rating=random.randint(1,5)
            ran=random.randint(0,4)
            L5=["I really enjoyed reading this book.","It was a fantastic book, I highly recommend it.",
                "This book captivated me from start to finish.","I found it engaging and thought-provoking.",
                "Its definitely one of my favorite books.","I couldnt put it down; it was so good.",
                "The characters and story were incredibly well-developed."]
            L1=["Unfortunately, this book wasnt to my liking.","I didnt enjoy reading it; it didnt resonate with me.",
                "The plot felt weak and the characters were uninteresting.","It didnt meet my expectations; I was disappointed.",                
                "I struggled to connect with the story or the writing style.","It just wasnt my cup of tea.",
                "I found it boring and couldnt get into it."]
            if Rating>2:
                Comment=random.choice(L5)
            else:
                Comment=random.choice(L1)
            ApprovalStatus="Approved"
            if ran==0:
                ApprovalStatus="Rejected"
            file.write("Insert into Review\n")
            file.write("(`ReviewID`,`SchoolID`,`UserID`,`BookID`,`Rating`,`Comment`,`ApprovalStatus`)\n")
            file.write("Values\n")
            file.write(f"('{ReviewID}','{schoolid}','{userid}','{bookid}','{Rating}','{Comment}','{ApprovalStatus}')\n")
            file.write(";\n\n")
            ReviewID+=1
    return ReviewID

#########################################
def replace_special_characters(string):
    pattern = r'\\u([0-9a-fA-F]{4})'

    def replace(match):
        hex_code = match.group(1)
        character = codecs.decode(hex_code, 'unicode_escape')
        return character

    replaced_string = re.sub(pattern, replace, string)
    replaced_string = replaced_string.replace("'", "")
    replaced_string = replaced_string.replace('"', "")
    
    return replaced_string

def filesToOne(delete=True):
    output_files = [
        path + "Data/Book.sql",
        path + "Data/Author.sql",
        path + "Data/Keyword.sql",
        path + "Data/Summary.sql",
        path + "Data/Category.sql",
        path + "Data/Reservation.sql",
        path + "Data/Review.sql",
        path + "Data/User.sql",
        path+"Data/School.sql"
    ]

    output_file_combined = path + "Data/mysql-db23-50-insert-data.sql"
    ll=0
    with open(output_file_combined, "w", encoding="utf-8") as output_file:
        for file_path in output_files:
            with open(file_path, "r", encoding="utf-8") as input_file:
                data = input_file.read()
                output_file.write(data)
            output_file.write("\n\n")
    # Delete the output files
    if delete:
        for file_path in output_files:
            os.remove(file_path)
book_to_text()

user_to_text()

filesToOne(False)


