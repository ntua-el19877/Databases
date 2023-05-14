import random
import requests
import json
import names
import re
import codecs

def replace_special_characters(string):
    return re.sub('[^a-zA-Z0-9 \n\.]', '', string)

def generate_name():
    first_names = ["Alice", "Bob", "Charlie","Jack"]
    last_names = ["Smith", "Johnson", "Williams", "Jones"]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    return f"{first_name} {last_name}"

def generate_name2():
    first_names = ["Bill", "Joseph", "Julius","Borat"]
    last_names = ["Stark", "Perry", "Jackson", "Loukas"]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    return f"{first_name} {last_name}"

def generate_name_pub():
    first_names = ["Frank", "Grace", "Henry", "Ivy"]
    last_names = [ "Brown", "Davis", "Miller", "Wilson"]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    return f"{first_name} {last_name}"

def get_book_count():
    file_path = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    with open(file_path) as file:
        data = json.load(file)
        print("Number of books:", len(data))
# Define the search terms
def add_v(search_terms, start_index=0, maxres=40):
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    dataold = list(json.load(open(output_file)))
    with open(output_file, "w") as file:
        url = f"https://www.googleapis.com/books/v1/volumes?q={search_terms}"
        params = {
            "maxResults": maxres,
            "startIndex": start_index
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            books = data.get("items", [])
            count = 0
            keywords = []  # List to store extracted keywords
            for book in books:
                try:
                    
                    volume_info = book.get("volumeInfo", {})
                    title = volume_info.get("title")
                    title=replace_special_characters(title)
                    try:
                        authors = volume_info.get("authors", [])
                        if len(authors)==0:
                            raise Exception()
                    except:
                        authors=[generate_name(),generate_name2()]
                    try:
                        pageCount = volume_info.get("pageCount")
                        if pageCount==None:
                            raise Exception()
                    except:
                        pageCount=random.randint(100, 999)
                    try:
                        language = volume_info.get("language")
                    except:
                        language='en'
                    try:
                        publisher = volume_info.get("publisher")
                    except:
                        publisher=generate_name_pub()
                    if publisher==None:
                        publisher=generate_name_pub()

                    identifiers = volume_info.get("industryIdentifiers", [])
                    isbn = None
                    for identifier in identifiers:
                        if identifier.get("type") == "ISBN_13":
                            isbn = identifier.get("identifier")
                            break
                    if isbn==None:
                        isbn=random_number = random.randint(10**12, (10**13)-1)
                    summary = replace_special_characters(volume_info.get("description"))
                    categories = volume_info.get("categories", [])
                    image_links = volume_info.get("imageLinks", {})
                    thumbnail = image_links.get("thumbnail")

                    # Extract keywords from relevant fields
                    book_keywords = [replace_special_characters(keyword.lower()) for keyword in title.split()]
                    book_keywords.extend([replace_special_characters(author.lower()) for author in authors])
                    book_keywords.extend([replace_special_characters(word.lower()) for word in summary.split() if len(word) > 2])
                    book_keywords.extend([replace_special_characters(category.lower()) for category in categories])

                    keywords.extend(book_keywords)
                    
                    book_data = {
                        "title": title,
                        "authors": authors,
                        "pageCount": pageCount,
                        "language": language,
                        "publisher": publisher,
                        "isbn": isbn,
                        "summary": summary,
                        "categories": categories,
                        "thumbnail": thumbnail,
                        "keywords": book_keywords
                    }
                    dataold.append(book_data)
                except:
                    count+=1
            print("===========================")
            print(f"Error at {count} books")
        else:
            print("Error:", response.status_code)
            print("Reason:", response.text)

        dataold.sort(key=lambda x: x['title'])
        json.dump(dataold, file, indent=4)

    print("Values added to the JSON file:", output_file)

def remove_duplicates_by_isbn():
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    data = list(json.load(open(output_file)))

    # Create a dictionary to store unique books based on ISBN
    unique_books = {}
    for book in data:
        isbn = book.get("title")
        if isbn is not None:
            unique_books[isbn] = book

    # Convert the unique books back to a list
    data = list(unique_books.values())

    # Write the updated data to the file
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)

    print("Duplicate books removed from the JSON file:", output_file)

def get_data_to_txt():
    # Specify the input JSON file path
    input_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"

    # Specify the output text file path
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.txt"

    # Load data from the JSON file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Open the output text file in write mode
    with open(output_file, "w") as file:
        # Iterate over each book in the data
        for i,book in enumerate(data):
            book_id = i
            title = replace_special_characters(book.get("title", "*"))
            publisher = replace_special_characters(book.get("Publisher", "*"))
            isbn = book.get("ISBN", "*")
            num_of_pages = book.get("NumOfPages", "*")
            summary = replace_special_characters(book.get("Summary", "*"))
            inventory = book.get("Inventory", "*")
            image = book.get("Image", "*")
            language = book.get("Language", "*")
            keywords = replace_special_characters(book.get("Keywords", "*"))

            # Write the formatted data to the output file
            file.write("Insert into Book\n")
            file.write("(`BookId`,`Title`,`Publisher`,`ISBN`,`NumOfPages`,`Summary`,`Inventory`,`Image`,`Language`,`Keywords`)\n")
            file.write("Values\n")
            file.write(f"('{book_id}','{title}','{publisher}','{isbn}','{num_of_pages}','{summary}','{inventory}','{image}','{language}','{keywords}')\n")
            file.write(";\n\n")

    print("Data exported to", output_file)

#add 40*24 values
# stri='a'
# for j in range(3):
#     for i in range(24):
#         add_v(chr(ord(stri) + i),start_index=j*40)

# #add 40*20 values
# stri='a'
# for i in range(24):
#     add_v(chr(ord(stri) + i))

# #for testing add 40 values
add_v('a')

# # Call the function to remove duplicate books by ISBN
remove_duplicates_by_isbn()


# Usage example:
book_count = get_book_count()

get_data_to_txt()

