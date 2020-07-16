import requests
from bs4 import BeautifulSoup
import json


def komplett(link):
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='product-main-info__info').h1.span.text.lower()
    return name


def proshop(link):
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='col-xs-12 col-sm-7').h1.text.lower()
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

link = input('Indsæt link fra Komplett eller Proshop\n>')
URL_domain = link.split('/')[2]

komplett_domain = 'www.komplett.dk'
proshop_domain = 'www.proshop.dk'

# to determine which kind of site to find product name on (komplett or proshop)
if URL_domain == komplett_domain:
    produkt_navn = komplett(link)
elif URL_domain == proshop_domain:
    produkt_navn = proshop(link)

# Ændre æ, ø og/eller å
kategori = ændre_æøå(kategori)
produkt_navn = ændre_æøå(produkt_navn)


with open('records.json', 'r') as json_file:
    data = json.load(json_file)

with open('records.json', 'w') as json_file:
    if kategori not in data.keys():
        data[kategori] = {}
    data[kategori][produkt_navn] = {}
    data[kategori][produkt_navn][komplett_domain] = {}
    data[kategori][produkt_navn][komplett_domain]["info"] = {}
    data[kategori][produkt_navn][komplett_domain]["info"]["part_num"] = ""
    data[kategori][produkt_navn][komplett_domain]["dates"] = {}
    data[kategori][produkt_navn][proshop_domain] = {}
    data[kategori][produkt_navn][proshop_domain]["info"] = {}
    data[kategori][produkt_navn][proshop_domain]["info"]["part_num"] = ""
    data[kategori][produkt_navn][proshop_domain]["dates"] = {}

    #data[kategori][produkt_navn]['www.komplett.dk']["dates"][date] = {"pris": pris}
    #data[kategori][produkt_navn]['www.proshop.dk']["dates"][date_2] = {"pris": pris_2}

    json.dump(data, json_file, indent=2)


#print(data)