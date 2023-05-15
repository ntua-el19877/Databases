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
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.txt"

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:
        for i, book in enumerate(data):
            book_id = i
            title = replace_special_characters2(book.get("title", "*"))
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


get_data_to_txt2()