import requests
import tinydb
from bs4 import BeautifulSoup

def fetch_images_with_initiator(url: str):
    # Request the content of the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    tds = soup.find_all('td')
    

    names = []
    links = []

    for td in tds:
        anchors = td.find('a')

        try:
            for anchor in anchors:
                try:
                    img = td.find('img')
                    links.append(img['src'])
                except:
                    names.append(anchor.get_text())
        except:
           break
    
    return names, links

# Example usage
db = tinydb.TinyDB('./app/database/tms.json', indent = 4)
db.truncate()

url = 'https://wiki.otpokemon.com/index.php/TM_System'  # Replace with the actual URL of the page
try:
    names, links = fetch_images_with_initiator(url)
    for c, name in enumerate(names):
        db.insert({
           "name": name,
           "link": "https://wiki.otpokemon.com" + links[c]
        })
except Exception as e:
    print(f"An error occurred: {e}")
