from bs4 import BeautifulSoup
import requests


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
        
        return publications
    else:
        print("Error fetching data from DBLP:", response.status_code)
        return []