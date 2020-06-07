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

logger = log_setup()


class Product:
    def __init__(self, URL):
        logger.debug('Initiating instance of class "Product"')
        self.URL = URL
        try:
            self.get_info()
        except Exception as err:
            logger.error(f'Failed in method "Product.get_info()": {err}', exc_info=True)
        try:
            self.save_record()
        except Exception as err:
            logger.error(f'Failed in method "Product.save_record()": {err}', exc_info=True)

    def get_info(self):
        logger.info('Getting response from URL...')
        self.response = requests.get(self.URL)
        logger.info('Got response from URL')
        self.html_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.name = self.html_soup.find_all('div', class_='product-main-info__info')[0].h1.span.text
        self.price = ''.join(self.html_soup.find_all('div', class_='price-freight')[0].div.span.text.strip('.,-').split('.'))
        self.date = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))

    def print_info(self):
        print(f'Navn: {self.name}\nPris: {self.price} kr.\nDato: {self.date}\n')

    def save_record(self):
        #print('Saving record...')
        logger.info('Saving record...')
        with open('records.json', 'r') as json_file:
            data = json.load(json_file)
            data['dates'][self.date] = {"name": f"{self.name}", "price": f"{self.price}"}
        with open('records.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
        #print('Record saved')
        logger.info('Record saved')



test1 = Product('https://www.komplett.dk/product/1103205/hardware/pc-komponenter/grafikkort/asus-geforce-rtx-2080-ti-rog-strix-oc#')
#test1.print_info()
#test1.save_record()



def multiple_links():
    with open('links.txt', 'r') as txt_file:
        text_lines = txt_file.readlines()

    count = 1
    for line in text_lines:
        print(f'Produkt {count}:')
        print(f'Link: {line.strip()}')
        Product(line.strip()).print_info()
        count += 1
