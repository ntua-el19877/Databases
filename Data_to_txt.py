import random
import requests
import json
import names
import re
import codecs


def replace_special_characters2(string):
    pattern = r'\\u([0-9a-fA-F]{4})'

    def replace(match):
        hex_code = match.group(1)
        character = codecs.decode(hex_code, 'unicode_escape')
        return character

    replaced_string = re.sub(pattern, replace, string)
    return replaced_string

def book_to_text():
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\Book.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        book_titles=[]
        for i, book in enumerate(data):
            book_id = i+1
            title = replace_special_characters2(book.get("title", "*"))
            book_titles.append(title)
            publisher = replace_special_characters2(book.get("publisher", "*"))
            isbn = book.get("isbn", "*")
            num_of_pages = book.get("pageCount", "*")
            inventory = book.get("Inventory", "True")
            image = book.get("thumbnail", "*")
            language = book.get("language", "*")

            file.write("Insert into Book\n")
            file.write("(`BookId`,`Title`,`Publisher`,`ISBN`,`NumOfPages`,`Inventory`,`Image`,`Language`)\n")
            file.write("Values\n")
            file.write(f"('{book_id}','{title}','{publisher}','{isbn}','{num_of_pages}','{inventory}','{image}','{language}')\n")
            file.write(";\n\n")

    print("Data exported to", output_file)
    return book_titles


def replace_special_characters(string):
    pattern = r'\\u([0-9a-fA-F]{4})'

    def replace(match):
        hex_code = match.group(1)
        character = codecs.decode(hex_code, 'unicode_escape')
        return character

    replaced_string = re.sub(pattern, replace, string)
    return replaced_string

def author_to_text():
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\Author.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        allauth=[]
        for i, book in enumerate(data):
            authors=book.get("authors")
            for j,auth in enumerate(authors):
                if not auth in allauth:
                    AuthorID=len(allauth)+1
                    allauth.append(auth)
                    file.write("Insert into Author\n")
                    file.write("(`AuthorID`,`AuthorName`)\n")
                    file.write("Values\n")
                    file.write(f"('{AuthorID}','{auth}')\n")
                    file.write(";\n\n")
    print("Data exported to", output_file)
    return allauth

def book_author_to_text(all_book_titles,all_authors):
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\Book_Author.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        book_authors=[]
        for i, book in enumerate(data):
            title=book.get("title")
            BookID=all_book_titles.index(title)+1
            authors=book.get("authors")
            for author in authors:
                AuthorID=all_authors.index(author)+1

                file.write("Insert into Book_Author\n")
                file.write("(`BookID`,`AuthorID`)\n")
                file.write("Values\n")
                file.write(f"('{BookID}','{AuthorID}')\n")
                file.write(";\n\n")
                book_authors.append((BookID,AuthorID))
    print("Data exported to", output_file)
    return book_authors


#only ren once
all_book_titles=book_to_text()
# for i,val in enumerate(book_titles):
#     print(f"ID: {i+1} Book: {val}")
# print("===================")

#get author text
all_authors=author_to_text()
# for i,val in enumerate(all_authors):
#     print(f"ID: {i+1} Author: {val}")
# print("===================")

all_book_authors=book_author_to_text(all_book_titles,all_authors)
# for i,val in enumerate(all_book_authors):
#     print(f"Book_Author: {val}")
# print("===================")