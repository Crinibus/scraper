#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
from scraping import change_name
import argparse


def argparse_setup():
    '''Setup argparse.'''
    parser = argparse.ArgumentParser()

    parser.add_argument('category', 
                        help='the category the product is going to be in',
                        type=str)

    parser.add_argument('url', 
                        help='the url to the product',
                        type=str)

    return parser.parse_args()


def komplett(link):
    '''Get name of product from Komplett-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='product-main-info__info').h1.span.text.lower()
    name = change_name(name)
    return name


def proshop(link):
    '''Get name of product from Proshop-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='col-xs-12 col-sm-7').h1.text.lower()
    name = change_name(name)
    return name


def computersalg(link):
    '''Get name of product from Computersalg-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('h1', itemprop='name').text.lower()
    name = change_name(name)
    return name


def elgiganten(link):
    '''Get name of product from Elgiganten-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('h1', class_='product-title').text.lower()
    name = change_name(name)
    return name


def ændre_æøå(navn):
    '''Change the letters æ, ø and å to international letters to avoid unicode.'''
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


def save(kategori, produkt_navn):
    '''Save (category and) product-name in JSON-file.'''
    with open('records.json', 'r') as json_file:
        data = json.load(json_file)

    with open('records.json', 'w') as json_file:
        if kategori not in data.keys():
            data[kategori] = {}

        data[kategori][produkt_navn] = {
                                            f"{komplett_domain}": {
                                                "info": {
                                                    "part_num": "",
                                                    "url": ""
                                                },
                                                "dates": {}  
                                            },
                                            f"{proshop_domain}": {            
                                                "info": {
                                                    "part_num": "",
                                                    "url": ""
                                                },
                                                "dates": {}
                                            },
                                            f"{computersalg_domain}": {            
                                                "info": {
                                                    "part_num": "",
                                                    "url": ""
                                                },
                                                "dates": {}
                                            },
                                            f"{elgiganten_domain}": {
                                                "info": {
                                                    "part_num": "",
                                                    "url": ""
                                                },
                                                "dates": {}
                                            }
                                        }
        
        json.dump(data, json_file, indent=2)


def main():
    #kategori = input("Kategori f.eks. 'gpu': ")
    kategori = args.category
    #produkt_navn = input('Produkt navn: ')

    #link = input('Indsæt link fra Komplett, Proshop eller Computersalg\n>')
    link = args.url
    URL_domain = link.split('/')[2]

    # to determine which kind of site to find product name on
    if URL_domain == komplett_domain:
        produkt_navn = komplett(link)
    elif URL_domain == proshop_domain:
        produkt_navn = proshop(link)
    elif URL_domain == computersalg_domain:
        produkt_navn = computersalg(link)
    elif URL_domain == elgiganten_domain:
        produkt_navn = elgiganten(link)
    else:
        print(f'Sorry, but I can\'t scrape from this domain: {URL_domain}')
        return

    # Ændre æ, ø og/eller å
    kategori = ændre_æøå(kategori)
    produkt_navn = ændre_æøå(produkt_navn)
    
    save(kategori, produkt_navn)


if __name__ == '__main__':
    komplett_domain = 'www.komplett.dk'
    proshop_domain = 'www.proshop.dk'
    computersalg_domain = 'www.computersalg.dk'
    elgiganten_domain = 'www.elgiganten.dk'
    args = argparse_setup()
    main()
