import datetime
import random
from numpy import split
import requests
import json
import names
import re
import codecs
import secrets
import time

# path='/home/angelos/Documents/GitHub/Databases/'
path='C:/Users/Aggelos/Documents/GitHub/Databases/'

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
    removedata(output_file2)
    removedata(output_file3)
    removedata(output_file4)
    removedata(output_file5)

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file1, "w", encoding="utf-8") as file:
        #5 schools
        Auth=[]
        Cat=[]
        Sum=[]
        Key=[]
        for SchoolID in range(1,6):
            book_id=1
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
                    file.write("(`BookID`,`SchoolID`,`Title`,`Publisher`,`ISBN`,`NumOfPages`,`Inventory`,`Image`,`Language`)\n")
                    file.write("Values\n")
                    file.write(f"('{book_id}','{SchoolID}','{title}','{publisher}','{isbn}','{num_of_pages}','{inventory}','{image}','{language}')\n")
                    file.write(";\n\n")
                    Auth=addAuthor(isbn,book,output_file2,Auth)
                    Key=addKeyword(output_file3,book,isbn,Key)
                    Sum=addSummary(output_file4,book,isbn,Sum)
                    Cat=addCategory(output_file5,book,isbn,Cat)
                    # addAuthor(SchoolID,book_id,book,output_file2)
                    # addKeyword(output_file3,book,book_id,SchoolID)
                    # addSummary(output_file4,book,book_id,SchoolID)
                    # addCategory(output_file5,book,book_id,SchoolID)
                    book_id+=1

    print("Data exported")



def addAuthor(isbn,book,output_file,L):
    if not isbn in L:
        with open(output_file, "a", encoding="utf-8") as file:
            authors=book.get("authors")
            for j,auth in enumerate(authors):
                file.write("Insert into Author\n")
                file.write("(`ISBN`,`AuthorName`)\n")
                file.write("Values\n")
                file.write(f"('{isbn},'{replace_special_characters(auth)}')\n")
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
    removedata(output_file2)
    removedata(output_file3)
    with open(output_file, "w", encoding="utf-8") as file:
        #5 schools
        for i in range(5):
            #100 people in school
            resID=1
            L=[]
            reviewid=1
            for j in range(100):
                Password=secrets.token_urlsafe(13)
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
                elif j==99:
                    Role='Administrator'
                file.write("Insert into User\n")
                file.write("(`UserID`,`SchoolID`,`Username`,`Password`,`Role`,`FirstName`,`LastName`,`BorrowerCard`)\n")
                file.write("Values\n")
                file.write(f"('{j+1}','{i+1}','{Username}','{Password}','{Role}','{FirstName}','{LastName}','{BorrowerCard}')\n")
                file.write(";\n\n")
                if random.randint(0, 5)==0:
                    reviewid=addReview(output_file3,j+1,i+1,reviewid)
                if random.randint(0, 5)==0:
                    L,resID=addReservation(output_file2,j+1,i+1,resID,L)
    print("Data exported to", output_file)

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

book_to_text()

user_to_text()