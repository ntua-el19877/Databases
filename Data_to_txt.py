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
            title = replace_special_characters(book.get("title", "*"))
            book_titles.append(title)
            publisher = replace_special_characters(book.get("publisher", "*"))
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
                if not replace_special_characters(auth) in allauth:
                    AuthorID=len(allauth)+1
                    allauth.append(replace_special_characters(auth))
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


def category_to_text():
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\Category.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        all_categories=[]
        for i, book in enumerate(data):
            categories=book.get("categories")
            for j,categ in enumerate(categories):
                if not replace_special_characters(categ) in all_categories:
                    CategoryID=len(all_categories)+1
                    all_categories.append(replace_special_characters(categ))
                    file.write("Insert into Category\n")
                    file.write("(`CategoryID`,`CategoryName`)\n")
                    file.write("Values\n")
                    file.write(f"('{CategoryID}','{categ}')\n")
                    file.write(";\n\n")
    print("Data exported to", output_file)
    return all_categories

def book_category_to_text(all_book_titles,all_categories):
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\Book_Category.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        Book_Categories=[]
        for i, book in enumerate(data):
            title=replace_special_characters(book.get("title"))
            BookID=all_book_titles.index(title)+1
            categories=book.get("categories")
            for categ in categories:
                CatId=all_categories.index(replace_special_characters(categ))+1

                file.write("Insert into Book_Category\n")
                file.write("(`BookID`,`CategoryID`)\n")
                file.write("Values\n")
                file.write(f"('{BookID}','{CatId}')\n")
                file.write(";\n\n")
                Book_Categories.append((BookID,CatId))
    print("Data exported to", output_file)
    return Book_Categories

def keywords_to_text():
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\Keyword.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        all_categories=[]
        for i, book in enumerate(data):
            categories=book.get("keywords")
            for j,categ in enumerate(categories):
                if not replace_special_characters(categ) in all_categories:
                    CategoryID=len(all_categories)+1
                    all_categories.append(replace_special_characters(categ))
                    file.write("Insert into Keyword\n")
                    file.write("(`KeywordsID`,`KeywordName`)\n")
                    file.write("Values\n")
                    file.write(f"('{CategoryID}','{categ}')\n")
                    file.write(";\n\n")
    print("Data exported to", output_file)
    return all_categories

def book_keywords_to_text(all_book_titles,all_categories):
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\Book_Keyword.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        Book_Categories=[]
        for i, book in enumerate(data):
            title=replace_special_characters(book.get("title"))
            BookID=all_book_titles.index(title)+1
            categories=book.get("keywords")
            for categ in categories:
                CatId=all_categories.index(replace_special_characters(categ))+1

                file.write("Insert into Book_Keyword\n")
                file.write("(`BookID`,`KeywordID`)\n")
                file.write("Values\n")
                file.write(f"('{BookID}','{CatId}')\n")
                file.write(";\n\n")
                Book_Categories.append((BookID,CatId))
    print("Data exported to", output_file)
    return Book_Categories

def summary_to_text():
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\Summary.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        all_categories=[]
        for i, book in enumerate(data):
            categories=book.get("keywords")
            summary=book.get("summary")
            all_categories.append(replace_special_characters(summary))
            file.write("Insert into Summary\n")
            file.write("(`BookID`,`Summary`)\n")
            file.write("Values\n")
            file.write(f"('{i+1}','{summary}')\n")
            file.write(";\n\n")
    print("Data exported to", output_file)
    return all_categories

#===================================================

# all_book_titles=book_to_text()

# all_authors=author_to_text()

# all_book_authors=book_author_to_text(all_book_titles,all_authors)

# all_categories=category_to_text()

# all_book_categories=book_category_to_text(all_book_titles,all_categories)

# all_keywords=keywords_to_text()

# all_book_keywords=book_keywords_to_text(all_book_titles,all_keywords)

all_summary=summary_to_text()

