import requests
from bs4 import BeautifulSoup
import chardet

# URL of the webpage to scrape
url = "https://vsit.edu.in/bscit.html"
# Fetch the webpage content
response = requests.get(url=url)

# Detect encoding using chardet
detected = chardet.detect(response.content)
encoding = detected['encoding'] if detected['encoding'] else 'utf-8'  # Fallback to utf-8

# Decode the content
content = response.content.decode(encoding, errors='ignore')  # Ignore errors if decoding fails

# Parse the webpage content with BeautifulSoup
soup = BeautifulSoup(content, 'lxml')

# Find the first <p> tag
s1 = soup.find("h1",{"class":"text-center"})

# Print the content of the first <p> tag
if s1:
    print(s1.text)
else:
    print("No <p> tag found.")
