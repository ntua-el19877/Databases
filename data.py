import requests
import json
# Define the search terms
def add_v(term,maxres=40):
    search_terms = term
    output_file = "C:\\Users\\Aggelos\\Documents\\GitHub\\Databases\\output.json"
    dataold=list(json.load(open(output_file)))
    with open(output_file, "w") as file:

        url = f"https://www.googleapis.com/books/v1/volumes?q={search_terms}"
        params = {
            "maxResults": maxres
        }
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the JSON response
            data = response.json()
            my_dict={}
            # Access the list of books
            books = data.get("items", [])
            # print(books[1])
            # Process the books or perform further actions
            count=0
            for i,book in enumerate(books):
                # Extract relevant information from each book
                try:
                    title = book["volumeInfo"]["title"]
                    authors = book["volumeInfo"]["authors"]
                    # categories = book["volumeInfo"]["categories"]
                    my_dict["title"]=title
                    my_dict["authors"]=authors
                    # my_dict["categories"]=categories
                    dataold.append(my_dict)
                except:
                    # print(f"=======================================")
                    count+=1
                my_dict={}
            print(f"Error at {count} books")
                

        else:
            # Handle the error case
            print("Error:", response.status_code)
            print("Reason:", response.text)
        # Write the JSON data to the file
        json.dump(dataold, file, indent=4)

    print("Values added to the JSON file:", output_file)

add_v('a')