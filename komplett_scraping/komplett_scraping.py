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


class Komplett:
    def __init__(self, category, URL):
        logger.debug(f'Initiating instance of class "{self.__class__.__name__}"')
        self.cat = category
        self.URL = URL
        self.URL_domain = self.URL.split('/')[2]
        logger.debug(f'category: {self.cat}, from url: {self.URL}')
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
        self.part_num = self.URL.split('/')[4]
        self.date = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))

    def print_info(self):
        print(f'Kategori: {self.cat}\nNavn: {self.name}\nPris: {self.price} kr.\nDato: {self.date}\nFra domain: {self.URL_domain}\nProdukt nummer: {self.part_num}\n')

    def save_record(self):
        #print('Saving record...')
        logger.info('Saving record...')
        with open('records.json', 'r') as json_file:
            data = json.load(json_file)
            data[self.cat][self.date] = {"name": f"{self.name}", "price": f"{self.price}", "from": f'{self.URL_domain}', "part_num": f'{self.part_num}'}
        with open('records.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
        #print('Record saved')
        logger.info('Record saved')



gpu = Komplett('gpu', 'https://www.komplett.dk/product/1103205/hardware/pc-komponenter/grafikkort/asus-geforce-rtx-2080-ti-rog-strix-oc#')
ssd = Komplett('ssd', 'https://www.komplett.dk/product/1133452/hardware/lagring/harddiskssd/ssd-m2/corsair-force-series-mp600-1tb-m2-ssd#')

gpu.print_info()
ssd.print_info()
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
