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

# def random_date_time(start,end,prop):


# path='/home/angelos/Documents/GitHub/Databases/'
path='C:/Users/Aggelos/Documents/GitHub/Databases/'

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
        for SchoolID in range(1,6):
            book_id=1
            #get all possible books
            for i, book in enumerate(data):
                #add 0-3 books to the school
                for j in range(random.randint(0,3)):
                    title = replace_special_characters(book.get("title", "*"))
                    publisher = replace_special_characters(book.get("publisher", "*"))
                    isbn = book.get("isbn", "*")
                    num_of_pages = book.get("pageCount", "*")
                    inventory = book.get("Inventory", "True")
                    image = book.get("thumbnail", "*")
                    language = book.get("language", "*")
                    file.write("Insert into Book\n")
                    file.write("(`BookID`,`SchoolID`,`Title`,`Publisher`,`ISBN`,`NumOfPages`,`Inventory`,`Image`,`Language`)\n")
                    file.write("Values\n")
                    file.write(f"('{book_id}','{SchoolID}','{title}','{publisher}','{isbn}','{num_of_pages}','{inventory}','{image}','{language}')\n")
                    file.write(";\n\n")
                    addAuthor(SchoolID,book_id,book,output_file2)
                    addKeyword(output_file3,book,book_id,SchoolID)
                    addSummary(output_file4,book,book_id,SchoolID)
                    addCategory(output_file5,book,book_id,SchoolID)
                    book_id+=1

    print("Data exported")

def addAuthor(SchID,BookID,book,output_file):

    with open(output_file, "a", encoding="utf-8") as file:
        authors=book.get("authors")
        for j,auth in enumerate(authors):
            file.write("Insert into Author\n")
            file.write("(`BookID`,`SchoolID`,`AuthorName`)\n")
            file.write("Values\n")
            file.write(f"('{BookID}','{SchID}','{replace_special_characters(auth)}')\n")
            file.write(";\n\n")

def addKeyword(output_file,book,bookid,schid):
    with open(output_file, "a", encoding="utf-8") as file:
        categories=book.get("keywords")
        for j,categ in enumerate(categories):
            file.write("Insert into Keyword\n")
            file.write("(`BookID`,`SchoolID`,`KeywordName`)\n")
            file.write("Values\n")
            file.write(f"('{bookid}','{schid}','{categ}')\n")
            file.write(";\n\n")

def addSummary(output_file,book,book_id,SchoolID):
    with open(output_file, "a", encoding="utf-8") as file:
        summary=book.get("summary")
        file.write("Insert into Summary\n")
        file.write("(`BookID`,`SchoolID`,`Summary`)\n")
        file.write("Values\n")
        file.write(f"('{book_id}','{SchoolID}','{summary}')\n")
        file.write(";\n\n")

def addCategory(output_file,book,book_id,SchoolID):

    with open(output_file, "a", encoding="utf-8") as file:
            categories=book.get("categories")
            for j,categ in enumerate(categories):
                    file.write("Insert into Category\n")
                    file.write("(`BookID`,`SchoolID`,`CategoryName`)\n")
                    file.write("Values\n")
                    file.write(f"('{book_id}','{SchoolID}','{replace_special_characters(categ)}')\n")
                    file.write(";\n\n")
#########################################

def user_to_text():
    
    output_file = path+"Data/User.sql"
    output_file2 = path+"Data/Reservation.sql"
    removedata(output_file2)
    with open(output_file, "w", encoding="utf-8") as file:
        #5 schools
        for i in range(5):
            #100 people in school
            resID=1
            L=[]
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
                # if random.randint(0, 5)==0:
                #     addReview()
                if random.randint(0, 5)==0:
                    L=addReservation(output_file2,j+1,i+1,resID,L)
                    resID+=1
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
                Active=False
            else:
                Active=True
            
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
            file.write(f"('{ReservationID}','{schoolid}','{userid}','{bookid}','{us}','{ExpirationDates}','{str(Active)}')\n")
            file.write(";\n\n")
    return L


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

# def author_to_text():
#     input_file = path+"output.json"
#     output_file = path+"Data/Author.txt"

#     with open(input_file, "r") as file:
#         data = json.load(file)

#     with open(output_file, "w", encoding="utf-8") as file:
#         allauth=[]
#         for i, book in enumerate(data):
#             authors=book.get("authors")
#             for j,auth in enumerate(authors):
#                 if not replace_special_characters(auth) in allauth:
#                     AuthorID=len(allauth)+1
#                     allauth.append(replace_special_characters(auth))
#                     file.write("Insert into Author\n")
#                     file.write("(`AuthorID`,`AuthorName`)\n")
#                     file.write("Values\n")
#                     file.write(f"('{AuthorID}','{auth}')\n")
#                     file.write(";\n\n")
#     print("Data exported to", output_file)
#     return allauth

# def book_author_to_text(all_book_titles,all_authors):
#     input_file = path+"output.json"
#     output_file = path+"Data/Book_Author.txt"

#     with open(input_file, "r") as file:
#         data = json.load(file)

#     with open(output_file, "w", encoding="utf-8") as file:
#         book_authors=[]
#         for i, book in enumerate(data):
#             title=book.get("title")
#             BookID=all_book_titles.index(title)+1
#             authors=book.get("authors")
#             for author in authors:
#                 AuthorID=all_authors.index(author)+1

#                 file.write("Insert into Book_Author\n")
#                 file.write("(`BookID`,`AuthorID`)\n")
#                 file.write("Values\n")
#                 file.write(f"('{BookID}','{AuthorID}')\n")
#                 file.write(";\n\n")
#                 book_authors.append((BookID,AuthorID))
#     print("Data exported to", output_file)
#     return book_authors


# def category_to_text():
#     input_file = path+"output.json"
#     output_file = path+"Data/Category.txt"

#     with open(input_file, "r") as file:
#         data = json.load(file)

#     with open(output_file, "w", encoding="utf-8") as file:
#         all_categories=[]
#         for i, book in enumerate(data):
#             categories=book.get("categories")
#             for j,categ in enumerate(categories):
#                 if not replace_special_characters(categ) in all_categories:
#                     CategoryID=len(all_categories)+1
#                     all_categories.append(replace_special_characters(categ))
#                     file.write("Insert into Category\n")
#                     file.write("(`CategoryID`,`CategoryName`)\n")
#                     file.write("Values\n")
#                     file.write(f"('{CategoryID}','{categ}')\n")
#                     file.write(";\n\n")
#     print("Data exported to", output_file)
#     return all_categories

# def book_category_to_text(all_book_titles,all_categories):
#     input_file = path+"output.json"
#     output_file = path+"Data/Book_Category.txt"

#     with open(input_file, "r") as file:
#         data = json.load(file)

#     with open(output_file, "w", encoding="utf-8") as file:
#         Book_Categories=[]
#         for i, book in enumerate(data):
#             title=replace_special_characters(book.get("title"))
#             BookID=all_book_titles.index(title)+1
#             categories=book.get("categories")
#             for categ in categories:
#                 CatId=all_categories.index(replace_special_characters(categ))+1

#                 file.write("Insert into Book_Category\n")
#                 file.write("(`BookID`,`CategoryID`)\n")
#                 file.write("Values\n")
#                 file.write(f"('{BookID}','{CatId}')\n")
#                 file.write(";\n\n")
#                 Book_Categories.append((BookID,CatId))
#     print("Data exported to", output_file)
#     return Book_Categories

# def keywords_to_text():
#     input_file = path+"output.json"
#     output_file = path+"Data/Keyword.txt"

#     with open(input_file, "r") as file:
#         data = json.load(file)

#     with open(output_file, "w", encoding="utf-8") as file:
#         all_categories=[]
#         for i, book in enumerate(data):
#             categories=book.get("keywords")
#             for j,categ in enumerate(categories):
#                 if not replace_special_characters(categ) in all_categories:
#                     CategoryID=len(all_categories)+1
#                     all_categories.append(replace_special_characters(categ))
#                     file.write("Insert into Keyword\n")
#                     file.write("(`KeywordsID`,`KeywordName`)\n")
#                     file.write("Values\n")
#                     file.write(f"('{CategoryID}','{categ}')\n")
#                     file.write(";\n\n")
#     print("Data exported to", output_file)
#     return all_categories

# def book_keywords_to_text(all_book_titles,all_categories):
#     input_file = path+"output.json"
#     output_file = path+"Data/Book_Keyword.txt"

#     with open(input_file, "r") as file:
#         data = json.load(file)

#     with open(output_file, "w", encoding="utf-8") as file:
#         Book_Categories=[]
#         for i, book in enumerate(data):
#             title=replace_special_characters(book.get("title"))
#             BookID=all_book_titles.index(title)+1
#             categories=book.get("keywords")
#             for categ in categories:
#                 CatId=all_categories.index(replace_special_characters(categ))+1

#                 file.write("Insert into Book_Keyword\n")
#                 file.write("(`BookID`,`KeywordID`)\n")
#                 file.write("Values\n")
#                 file.write(f"('{BookID}','{CatId}')\n")
#                 file.write(";\n\n")
#                 Book_Categories.append((BookID,CatId))
#     print("Data exported to", output_file)
#     return Book_Categories

# def summary_to_text():
#     input_file = path+"output.json"
#     output_file = path+"Data/Summary.txt"

#     with open(input_file, "r") as file:
#         data = json.load(file)

#     with open(output_file, "w", encoding="utf-8") as file:
#         all_categories=[]
#         for i, book in enumerate(data):
#             categories=book.get("keywords")
#             summary=book.get("summary")
#             all_categories.append(replace_special_characters(summary))
#             file.write("Insert into Summary\n")
#             file.write("(`BookID`,`Summary`)\n")
#             file.write("Values\n")
#             file.write(f"('{i+1}','{summary}')\n")
#             file.write(";\n\n")
#     print("Data exported to", output_file)
#     return all_categories

# num_of_students=500
# num_of_schools=5

# def user_to_text():
#     output_file = path+"Data/User.txt"

#     with open(output_file, "w", encoding="utf-8") as file:
#         all_categories=[]
#         all_operators=[]
#         all_admins=[]
#         for i in range(num_of_schools):
#             for j in range(100):

#                 Password=secrets.token_urlsafe(13)
#                 Roles=['Professor',"Student",
#                     'Student','Student','Student',
#                     'Student','Student','Student',
#                     'Student','Professor']
#                 Role=random.choice(Roles)
#                 FirstName=names.get_first_name()
#                 Username=FirstName+str(random.randint(100, 999))
#                 all_categories.append(Username)
#                 LastName=names.get_last_name()
#                 if j==98:
#                     Role='Operator'
#                     all_operators.append(FirstName+' '+LastName)
#                 elif j==99:
#                     Role='Administrator'
#                     all_admins.append(FirstName+' '+LastName)
#                 file.write("Insert into User\n")
#                 file.write("(`UserID`,`SchoolID`,`Username`,`Password`,`Role`,`FirstName`,`LastName`)\n")
#                 file.write("Values\n")
#                 file.write(f"('{j+1}','{i+1}','{Username}','{Password}','{Role}','{FirstName}','{LastName}')\n")
#                 file.write(";\n\n")
#         L=all_admins+all_operators
#     print("Data exported to", output_file)
#     return all_categories,L

# def school_to_text(all_lib_operators):
#     output_file = path+"Data/School.txt"

#     with open(output_file, "w", encoding="utf-8") as file:
#         all_categories=[]
#         for i in range(num_of_schools):

#             Fir=['Cape Coral','Riverdale','Pinewood','Lakewood','Livanates']
#             Sec=['Institute','School of Fine Arts','High','Technical School']
#             SchoolName=random.choice(Fir)+' '+random.choice(Sec)
#             Fir=['2969 Charmaine Lane','2537 Commerce Boulevard','2066 North Bend River Road']
#             Sec=['Patricia','Paris','Somerset']
#             Thi=['79373','68669','78234']
#             Address=random.choice(Fir)+','+random.choice(Thi)
#             City=random.choice(Sec)
#             PhoneNumber=random.randint(6_970_000_000, 6_979_999_999)
#             Email=SchoolName+'@'+'mail.com'
#             SchoolDirectorFullName=names.get_full_name()
#             file.write("Insert into School\n")
#             file.write("(`SchoolID`,`SchoolName`,`Address`,`City`,`PhoneNumber`,`Email`,`SchoolLibraryOperatorFullName`,`SchoolDirectorFullName`)\n")
#             file.write("Values\n")
#             file.write(f"('{i+1}','{SchoolName}','{Address}','{City}','{PhoneNumber}','{Email}','{all_lib_operators[i+num_of_schools]}','{SchoolDirectorFullName})\n")
#             file.write(";\n\n")
#     print("Data exported to", output_file)
#     return all_categories


# def borrowercard_to_text(all_users):
#     output_file = path+"Data/BorrowerCard.txt"

#     with open(output_file, "w", encoding="utf-8") as file:
#         all_categories=[]
#         count=0
#         for i,user in enumerate(all_users):
#             count+=1
#             UserID=count
#             if not count>98:
#                 file.write("Insert into BorrowerCard\n")
#                 file.write("(`BorrowerCardID`,`UserID`)\n")
#                 file.write("Values\n")
#                 file.write(f"('{random.randint(10**12, (10**13)-1)}','{UserID}')\n")
#                 file.write(";\n\n")
#             elif count==100:
#                 count=0
#     print("Data exported to", output_file)
#     return all_categories

# def borrowercard_to_text(all_users):
#     output_file = path+"Data/BorrowerCard.txt"

#     with open(output_file, "w", encoding="utf-8") as file:
#         all_categories=[]
#         count=0
#         for i,user in enumerate(all_users):
#             count+=1
#             UserID=count
#             if not count>98:
#                 file.write("Insert into BorrowerCard\n")
#                 file.write("(`BorrowerCardID`,`UserID`)\n")
#                 file.write("Values\n")
#                 file.write(f"('{random.randint(10**12, (10**13)-1)}','{UserID}')\n")
#                 file.write(";\n\n")
#             elif count==100:
#                 count=0
#     print("Data exported to", output_file)
#     return all_categories
# #===================================================

# book_to_text()

user_to_text()
# all_authors=author_to_text()

# all_book_authors=book_author_to_text(all_book_titles,all_authors)

# all_categories=category_to_text()

# all_book_categories=book_category_to_text(all_book_titles,all_categories)

# all_keywords=keywords_to_text()

# all_book_keywords=book_keywords_to_text(all_book_titles,all_keywords)

# all_summary=summary_to_text()

#these give each time different values
#we have 100 users for each of the 5 schools
# all_users,oper_5_admin_5=user_to_text()

# all_schools=school_to_text(oper_5_admin_5)

# all_borrowercards=borrowercard_to_text(all_users)

# review_to_text(all_users)