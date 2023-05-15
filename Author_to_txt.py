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

def get_data_to_txt2():
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
    for i,val in enumerate(allauth):
        print(f"ID: {i+1} Author: {val}")
    print("===================")


get_data_to_txt2()