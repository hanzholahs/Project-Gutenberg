import requests
import ast
import pandas as pd


def download_language_reference() -> None:
    """
    Downloads the list of languages from wikipedia using Wikitable2JSON API and stores it into a CSV file.
    The language table contains information about ISO 639 language codes, names, and other relevant information.
    
    Parameters: 
        None
        
    Returns:
        None
    """
    
    # setup URLs, headers, and output file path
    lang_reference_URL = "https://www.wikitable2json.com/api/List_of_ISO_639-2_codes"
      
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    output_path = "./data/languages.csv"

    # perform request and stores the results
    response = requests.get(lang_reference_URL, headers=headers)

    with open(output_path, 'wb') as f:
        f.write(response.content)
        
    # read the table from the file and convert it into an appropriate pandas dataframe        
    with open(output_path, "r", encoding="UTF-8") as f:
        table = f.read()
        
    cols = ast.literal_eval(table)[0][0]
    rows = ast.literal_eval(table)[0][1:]

    languages = pd.DataFrame(rows, columns=cols)
    
    # stores the output
    languages.to_csv(output_path, index=False)
    
    print("Language reference downloaded successfully.")
    
if __file__ == "__main__":
    download_language_reference()