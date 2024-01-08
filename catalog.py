import requests



def download_catalog() -> None:
    """
    Downloads the up-to-date catalog of the Project Gutenberg eBook collection, and stores it into a CSV file.
    The catalog contains information about each eBook, e.g., title, author, and publication date.
    
    Parameters:
        None
        
    Returns:
        None
    """
    
    # setup URLs and headers 
    catalog_URL = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    # perform request and stores the results
    response = requests.get(catalog_URL, headers=headers)

    with open("./data/catalog.csv", 'wb') as f:
        f.write(response.content)
        
    print("Catalog downloaded successfully.")
    

    
if __file__ == "__main__":
    download_language_reference()