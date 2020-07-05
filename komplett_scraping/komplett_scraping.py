#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging


def log_setup():
    # Gets or creates a logger
    logger = logging.getLogger(__name__)

    # set log level (lowest level)
    logger.setLevel(logging.DEBUG)

    # define file handler and set formatter
    file_handler = logging.FileHandler('logfile.log')
    formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)
    return logger


class Scraper:
    def __init__(self, category, URL):
        logger.debug(f'Initiating instance of class "{self.__class__.__name__}"')
        self.cat = category
        self.URL = URL
        self.URL_domain = self.URL.split('/')[2]
        logger.debug(f'Category: {self.cat}')
        logger.debug(f'URL: {self.URL}')
        try:
            self.get_info()
        except Exception as err:
            logger.error(f'Failed in method "{self.__class__.__name__}.get_info()": {err}', exc_info=True)

        try:
            self.save_record()
        except Exception as err:
            logger.error(f'Failed in method "{self.__class__.__name__}.save_record()": {err}', exc_info=True)

    def get_info(self): # gets overwritten
        self.name = ''
        self.price = ''
        self.date = ''
        self.part_num = ''

    def print_info(self):
        print(f'Kategori: {self.cat}\nNavn: {self.name}\nPris: {self.price} kr.\nDato: {self.date}\nFra domain: {self.URL_domain}\nProdukt nummer: {self.part_num}\n')

    def save_record(self):
        #print('Saving record...')
        logger.info('Saving record...')
        with open('records.json', 'r') as json_file:
            data = json.load(json_file)
            #data[self.cat][self.date] = {"name": f"{self.name}", "price": f"{self.price}", "from": f'{self.URL_domain}', "part_num": f'{self.part_num}'}
            data[self.cat][self.name][self.URL_domain]["dates"][self.date] = {"price": f"{self.price}"}
        with open('records.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
            #json.dump(data, json_file)
        #print('Record saved')
        logger.info('Record saved')


class Komplett(Scraper):
    def get_info(self):
        logger.info('Getting response from URL...')
        self.response = requests.get(self.URL)
        logger.info('Got response from URL')
        self.html_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.name = self.html_soup.find_all('div', class_='product-main-info__info')[0].h1.span.text.lower()
        try:
            self.price = ''.join(self.html_soup.find_all('div', class_='price-freight')[0].div.span.text.strip('.,-').split('.'))
        except AttributeError:
            self.price = ''.join(self.html_soup.find_all('div', class_='price-freight')[0].span.text.strip('.,-').split('.'))
        self.part_num = self.URL.split('/')[4]
        self.date = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))


class Proshop(Scraper):
    def get_info(self):
        logger.info('Getting response from URL...')
        self.response = requests.get(self.URL)
        logger.info('Got response from URl')
        self.html_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.name = self.html_soup.find_all('div', class_='col-xs-12 col-sm-7')[0].h1.text.lower()
        if "asus geforce rtx 2080 ti rog strix oc" in self.name:
            self.name = "asus geforce rtx 2080 ti rog strix oc"
        self.price = ''.join(self.html_soup.find_all('div', class_='col-md-7')[0].span.span.text.strip('.-kr').split(',')[0].split('.'))
        self.part_num = self.html_soup.find('small', class_='col-xs-12 text-center').strong.text
        self.date = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))


def multiple_links(file_name):
    with open(f'{file_name}', 'r') as file:
        lines = file.readlines()

    count = 1
    for line in lines:
        print(f'Produkt {count}:')
        print(f'Link: {line.strip()}')
        Product(line.strip()).print_info()
        count += 1


if __name__ == '__main__':
    logger = log_setup()
    Komplett('gpu', 'https://www.komplett.dk/product/1103205/hardware/pc-komponenter/grafikkort/asus-geforce-rtx-2080-ti-rog-strix-oc#')
    Komplett('ssd', 'https://www.komplett.dk/product/1133452/hardware/lagring/harddiskssd/ssd-m2/corsair-force-series-mp600-1tb-m2-ssd#')
    Proshop('gpu', 'https://www.proshop.dk/Grafikkort/ASUS-GeForce-RTX-2080-Ti-ROG-STRIX-OC-11GB-GDDR6-RAM-Grafikkort/2679518')
