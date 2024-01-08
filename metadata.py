import tarfile
import rdflib
import csv
import re
import os
import requests
import pandas as pd



def download_metadata_tar(folder_path: str) -> None:
    """Downloads the metadata tar file from the Project Gutenberg repo. 
    This file contains the metadata for all the books on the Gutenberg Project in RDF/XML format.
    
    Parameters:
        folder_path (str): The path to the folder where the metadata tar file will be downloaded. The folder will be created if it does not exist.
    
    Returns:
        None. The metadata tar file is downloaded into the specified folder.
    """
    
    # Check if metadata already downloaded. If so, return. Otherwise, download and extract. 
    output_path = os.path.join(folder_path, "metadata.tar.bz2")
    if os.path.exists(output_path):
        print("Metadata already downloaded.")
        return
    
    # setup URLs and headers
    metadata_URL = "https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    # perform the request and storest the results
    response = requests.get(metadata_URL, headers=headers)

    with open("./data/metadata.tar.bz2", 'wb') as f:
        f.write(response.content)
    
    print("Metadata downloaded.")




def extract_metadata_tar(folder_path: str) -> None:
    """Extracts the metadata tar file from the Project Gutenberg repo into a folder. 
    This folder contains the metadata for all the books on the Gutenberg Project in RDF/XML format.
    
    Parameters:
        folder_path (str): The path to the folder where the metadata tar file will be extracted. The folder will be created if it does not exist.
    
    Returns:
        None. The metadata tar file is extracted into the specified folder.
    """
    
    # Check if metadata already extracted. If so, return. Otherwise, extract.
    output_path = os.path.join(folder_path, "metadata")
    if os.path.exists(output_path):
        print("Metadata already extracted.")
        return
    
    # Extract tar file into a new folder
    with tarfile.open("./data/metadata.tar.bz2", "r:bz2") as f:
        f.extractall("./data/metadata")
        
    print("Metadata extracted.")
        




def extract_rdf_data(book_id: int, books_path: str) -> dict:
    """
    Extracts relevant inofrmation from an RDF data given a book ID from the Project Gutenberg repo. 
    It will extract its title, publisher, license, issue date, rights, download counts, authors, type, language, categories, and available formats.
    The extracted data is stored in a dictionary and returned.
    
    Parameters:
        book_id (int): The ID of the book to extract RDF data for.
        books_path (str): The path to the folder containing the extracted metadata.
    
    Returns:
        dict: A dictionary containing the extracted RDF data for the given book. The keys are the RDF property names, and the values are the corresponding RDF values.    
    """
    
    filepath = os.path.join(books_path, str(book_id), f"pg{str(book_id)}.rdf")
    
    g = rdflib.Graph()
    g.parse(filepath)
    
    prefixes = """
        PREFIX pgterms: <http://www.gutenberg.org/2009/pgterms/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX base: <http://www.gutenberg.org/>
    """

    results = g.query(prefixes + """
        SELECT *
        WHERE {
            ?ebook rdf:type pgterms:ebook .
            OPTIONAL { ?ebook dcterms:title ?title . }
            OPTIONAL { ?ebook dcterms:publisher ?publisher . }
            OPTIONAL { ?ebook dcterms:license ?license . }
            OPTIONAL { ?ebook dcterms:issued ?issued . }
            OPTIONAL { ?ebook dcterms:rights ?rights . }
            OPTIONAL { ?ebook pgterms:downloads ?downloads . }
            OPTIONAL { ?ebook dcterms:creator ?agent .
                       ?agent pgterms:name ?creator_name . }
            OPTIONAL { ?ebook dcterms:type ?type_element .
                       ?type_element rdf:value ?type . }
            OPTIONAL { ?ebook dcterms:language ?language_element .
                       ?language_element rdf:value ?language . }
            OPTIONAL { ?ebook pgterms:bookshelf ?bookshelf_element .
                       ?bookshelf_element rdf:value ?bookshelf .}
            OPTIONAL { ?ebook dcterms:hasFormat ?hasFormat_element .
                       ?hasFormat_element dcterms:format ?format_element . 
                       ?format_element rdf:value ?format . }
        }
    """)


    data_list = []
    
    for row in results:
        data = {str(var): str(row[var]) for var in results.vars}
        data['book_id'] = book_id
        
        del data['agent']
        del data['language_element']
        del data['type_element']
        del data['bookshelf_element']
        del data['hasFormat_element']
        del data['format_element']
        
        data_list.append(data)
        
    return merge_rdf_data(data_list)




def merge_rdf_data(data_list: list[dict]) -> dict:
    """
    Merges multiple RDF data dictionaries that might contain multiple entities (e.g., authors, categories) into a single dictionary.
    The merged dictionary will contain the same keys as the input dictionaries, but with a list of values for each key.
    
    Parameters:
        data_list (list[dict]): A list of RDF data dictionaries to merge.
    
    Returns:
        dict: A merged dictionary containing the same keys as the input dictionaries, but with a list of values for each key.
    """
    
    merged = None
    
    for data in data_list:
        
        if not merged:
            merged = data
            
            merged["creator_names"] = [data["creator_name"]]
            merged["bookshelves"] = [data["bookshelf"]]
            merged["available_formats"] = [data["format"]]
            
            del merged["creator_name"]
            del merged["bookshelf"]
            del merged["format"]
            
        else:
            if not data["creator_name"] in merged["creator_names"]:
                merged["creator_names"].append(data["creator_name"])
            if not data["bookshelf"] in merged["bookshelves"]:
                merged["bookshelves"].append(data["bookshelf"])
            if not data["format"] in merged["available_formats"]:
                merged["available_formats"].append(data["format"])
                
    return merged




def metadata_to_csv(folder_path: str) -> None:
    """
    Extracts the metadata from the Project Gutenberg repo and stores it in a CSV file.
    The CSV file contains the following columns:
    - book_id: The ID of the book.
    - type: The type of the book.
    - issued: The issue date of the book.
    - downloads: The number of downloads of the book.
    - title: The title of the book.
    - language: The language of the book.
    - ebook: The link of the book.
    - creator_names: A list of the names of the creators of the book.
    - bookshelves: A list of the bookshelves the book is in.
    - publisher: The publisher of the book.
    - license: The license of the book.
    - rights: The rights of the book.
    - available_formats: A list of the available formats of the book.
    
    Parameters:
        folder_path (str): The path to the folder containing the extracted metadata.
    
    Returns:
        None. The extracted metadata is written to a CSV file. The file is saved in the data folder.
    """
    
    books_path = os.path.join(folder_path, "metadata/cache/epub")
    book_ids = os.listdir(books_path)
    n_books = len(book_ids)
        
    filename = "./data/metadata1.csv"
    fieldnames = ["book_id", "type", "issued", "downloads", "title", "language", "ebook", "creator_names", "bookshelves", "publisher", "license", "rights", "available_formats"]
        
    for i, book_id in enumerate(book_ids):
        if i+1 % 1000 == 0:
            print(f"Processing book {i+1}/{n_books}")
        
        try:
            data = extract_rdf_data(book_id, books_path)
            
            with open(filename, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # write headers only at the first line of the output.csv
                if f.tell() == 0:
                    writer.writeheader()

                # Write the row data
                writer.writerow(data)
        except Exception as e:
            print(f"Error processing book {book_id}: {e}")
            continue


if __name__ == "__main__":
    folder_path = "./data/"    
    
    download_metadata_tar(folder_path)
    extract_metadata_tar(folder_path)
    metadata_to_csv(folder_path)