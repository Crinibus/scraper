import requests
from bs4 import BeautifulSoup
import json
from komplett_scraping import change_name

def komplett(link):
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='product-main-info__info').h1.span.text.lower()
    name = change_name(name)
    return name


def proshop(link):
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='col-xs-12 col-sm-7').h1.text.lower()
    name = change_name(name)
    return name


def computersalg(link):
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('h1', itemprop='name').text.lower()
    name = change_name(name)
    return name


def ændre_æøå(navn):
    nyt_navn = ''
    for bogstav in navn:
        if bogstav in 'æøå':
            if bogstav == 'æ':
                bogstav = 'ae'
            elif bogstav == 'ø':
                bogstav = 'oe'
            elif bogstav == 'å':
                bogstav = 'aa'
        nyt_navn += bogstav
    return nyt_navn


kategori = input("Kategori f.eks. 'gpu': ")
#produkt_navn = input('Produkt navn: ')

link = input('Indsæt link fra Komplett, Proshop eller Computersalg\n>')
URL_domain = link.split('/')[2]

komplett_domain = 'www.komplett.dk'
proshop_domain = 'www.proshop.dk'
computersalg_domain = 'www.computersalg.dk'

# to determine which kind of site to find product name on (komplett or proshop)
if URL_domain == komplett_domain:
    produkt_navn = komplett(link)
elif URL_domain == proshop_domain:
    produkt_navn = proshop(link)
elif URL_domain == computersalg_domain:
    produkt_navn = computersalg(link)

# Ændre æ, ø og/eller å
kategori = ændre_æøå(kategori)
produkt_navn = ændre_æøå(produkt_navn)


with open('records.json', 'r') as json_file:
    data = json.load(json_file)

with open('records.json', 'w') as json_file:
    if kategori not in data.keys():
        data[kategori] = {}

    data[kategori][produkt_navn] = {
                                        f"{komplett_domain}": {
                                            "info": {
                                                "part_num": ""
                                            },
                                            "dates": {}  
                                        },
                                        f"{proshop_domain}": {            
                                            "info": {
                                                "part_num": ""
                                            },
                                            "dates": {}
                                        },
                                        f"{computersalg_domain}": {            
                                            "info": {
                                                "part_num": ""
                                            },
                                            "dates": {}
                                        }
                                    }
    
    json.dump(data, json_file, indent=2)


#print(data)