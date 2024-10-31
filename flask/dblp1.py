import requests
import json
from bs4 import BeautifulSoup

def search_dblp(author_name):
    # DBLP API endpoint
    base_url = 'https://dblp.org/search/publ/api'
    
    # Define parameters for the API request
    params = {
        'q': author_name,
        'h': 100,  # Number of results to return
        'format': 'xml'
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        # Parse XML response
        publications = []
        xml_data = response.text
        
        # Use BeautifulSoup to parse the XML
        soup = BeautifulSoup(xml_data, 'xml')
        
        for hit in soup.find_all('hit'):
            title = hit.find('title').text
            link = hit.find('url').text
            publications.append({'title': title, 'link': link})
        
        # Save publications to a JSON file
        save_to_json(author_name, publications)
        
        return publications
    else:
        print("Error fetching data from DBLP:", response.status_code)
        return []

def save_to_json(author_name, publications):
    # Prepare the filename
    filename = f"{author_name.replace(' ', '_')}_dblp_publications.json"
    
    # Create a dictionary to store the author and their publications
    author_data = {
        'author': author_name,
        'publications': publications
    }
    
    # Write the data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(author_data, json_file, indent=4)
    
    print(f"Publications saved to {filename}")

# Example usage
author_name = "Shajil Kumar P A"  # Replace with the author's name you want to search
search_dblp(author_name)
