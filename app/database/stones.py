import requests
import tinydb
from bs4 import BeautifulSoup

def fetch_images_with_initiator(url: str, initiator_prefix: str = "Stones"):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    images = soup.find_all('img')

    filtered_images = []
    links = []

    for img in images:

        if 'Itens evolução.png' in img['alt']:
            pass
        elif 'Pure Stone.png' in img['alt']:
            pass
        elif 'Roll Stone.png' in img['alt']:
            pass
        elif 'Roll Stone.png' in img['alt']:
            pass
        elif 'Necklace of Spirit.png' in img['alt']:
            pass
        elif 'Zapdos Feather.png' in img['alt']:
            pass
        elif 'Magmarizer.png' in img['alt']:
            pass
        elif 'Powered by MediaWiki' in img['alt']:
            pass
        elif 'DubiousDisc.png' in img['alt']:
            pass
        else:
            img['alt'] = img['alt'].replace(" ", "_")
            img['alt'] = img['alt'].replace('.png', "")
            img['alt'] = img['alt'].lower()

            filtered_images.append(img['alt'])
            links.append(img['src'])
            

            print(img['alt'])


    return filtered_images, links

db = tinydb.TinyDB('./app/database/stones.json', indent = 4)
db.truncate()

url = 'https://wiki.otpokemon.com/index.php/Itens_de_Evolução'

try:
    images, links = fetch_images_with_initiator(url)
    for c, img_src in enumerate(images):
        db.insert({
            "name": img_src,
            "link": "https://wiki.otpokemon.com" + links[c]
        })
except Exception as e:
    print(f"An error occurred: {e}")