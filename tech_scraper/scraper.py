#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging


def log_setup():
    """Setup and return logger."""
    # Gets or creates a logger
    logger = logging.getLogger(__name__)

    # Check if logger already has a handler
    if logger.hasHandlers():
        logger.handlers.clear()

    # set log level (lowest level)
    logger.setLevel(logging.DEBUG)

    # define file handler and set formatter
    file_handler = logging.FileHandler('logfile.log')
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)
    return logger


class Scraper:
    def __init__(self, category, URL):
        self.logger = log_setup()
        self.logger.debug(f'Initiating class "{self.__class__.__name__}"')
        self.cat = category
        self.URL = URL
        self.URL_domain = self.URL.split('/')[2]
        self.logger.debug(f'Category: {self.cat}')
        self.logger.debug(f'URL: {self.URL}')

        try:
            self.get_response()
        except Exception as err:
            self.logger.error(f'Failed in method "{self.__class__.__name__}.get_response()": {err}', exc_info=True)

        try:
            self.get_info()
        except Exception as err:
            self.logger.error(f'Failed in method "{self.__class__.__name__}.get_info()": {err}', exc_info=True)

        self.name = change_æøå(change_name(self.name))
        self.date = str(datetime.today().strftime('%Y-%m-%d'))
        self.get_part_num()
        self.shorten_url()
        self.check_part_num()

        try:
            self.save_record()
        except Exception as err:
            self.logger.error(f'Failed in method "{self.__class__.__name__}.save_record()": {err}', exc_info=True)

    def get_info(self):  # gets overwritten
        """Get name and price of product."""
        self.name = ''
        self.price = ''

    def get_response(self):
        """Get response from URL."""
        self.logger.info('Getting response from URL...')
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
        cookies = dict(cookies_are='working')
        self.response = requests.get(self.URL, headers=headers, cookies=cookies)
        self.logger.info('Got response from URL')
        self.html_soup = BeautifulSoup(self.response.text, 'html.parser')

    def get_part_num(self):
        """Get part number from URL or from HTML."""
        self.part_num = ''
        if self.URL_domain == domains['komplett']:
            self.part_num = self.URL.split('/')[4]
        elif self.URL_domain == domains['proshop']:
            self.part_num = self.URL.split('/')[5]
        elif self.URL_domain == domains['computersalg']:
            self.part_num = self.URL.split('/')[4]
        elif self.URL_domain == domains['elgiganten']:
            self.part_num = self.html_soup.find('p', class_='sku discrete').text.replace('Varenr.:\xa0', '')
        elif self.URL_domain == domains['avxperten']:
            self.part_num = self.html_soup.find('div', class_='description-foot').p.text.replace('Varenummer: ', '')
        elif self.URL_domain == domains['av-cables']:
            self.part_num = self.html_soup.find('div', class_='text-right model').text.strip().replace('[ ', '').replace(']', '').split(': ')[1]
        elif self.URL_domain == domains['amazon']:
            self.part_num = self.URL.split('/')[5]
        elif self.URL_domain == domains['ebay']:
            if self.URL.split('/')[3] == 'itm':
                # Find "eBay item number"
                self.part_num = self.html_soup.find('div', id='descItemNumber').text
            else:
                # Find id number
                self.part_num = self.URL.split('=')[1]
        elif self.URL_domain == domains['power']:
            self.part_num = self.URL.split('/')[-2].replace('p-', '')
        elif self.URL_domain == domains['expert']:
            self.part_num = self.URL.split('/')[-2].replace('p-', '')
        elif self.URL_domain == domains['mm-vision']:
            self.part_num = self.html_soup.find('input', type='radio')['value']
        elif self.URL_domain == domains['coolshop']:
            self.part_num = self.html_soup.find_all('div', id='attributeSku')[1].text.strip()
        elif self.URL_domain == domains['sharkgaming']:
            self.part_num = 'Not existing on Sharkgaming'

    def check_part_num(self):
        """
        Checks if a product has a part number in the JSON-file,
        if it doesn't, it gets added to the JSON-file.
        """
        changed = False
        with open('records.json', 'r') as json_file:
            data = json.load(json_file)

        part_num_from_data = data[self.cat][self.name][self.URL_domain]['info']['part_num']

        if part_num_from_data == '':
            data[self.cat][self.name][self.URL_domain]['info']['part_num'] = self.part_num
            changed = True
        elif not self.part_num == part_num_from_data:
            data[self.cat][self.name][self.URL_domain]['info']['part_num_2'] = self.part_num
            changed = True

        if changed:
            with open('records.json', 'w') as json_file:
                json.dump(data, json_file, indent=2)

    def check_url(self):
        """
        Check if a product has a url in the JSON-file,
        if it doesn't, it gets added to the JSON-file.
        """
        changed = False
        with open('records.json', 'r') as json_file:
            data = json.load(json_file)

        url_from_data = data[self.cat][self.name][self.URL_domain]['info']['url']

        if url_from_data == '':
            data[self.cat][self.name][self.URL_domain]['info']['url'] = self.short_url
            changed = True
        elif not self.short_url == url_from_data:
            data[self.cat][self.name][self.URL_domain]['info']['url_2'] = self.short_url
            changed = True

        if changed:
            with open('records.json', 'w') as json_file:
                json.dump(data, json_file, indent=2)

    def shorten_url(self):
        """
        Shorten url to be as short as possible,
        usually domain.dk/product_number.
        """
        self.short_url = ''
        if self.URL_domain == domains['komplett']:
            self.short_url = f'https://www.komplett.dk/product/{self.part_num}'
        elif self.URL_domain == domains['proshop']:
            self.short_url = f'https://www.proshop.dk/{self.part_num}'
        elif self.URL_domain == domains['computersalg']:
            self.short_url = f'https://www.computersalg.dk/i/{self.part_num}'
        elif self.URL_domain == domains['elgiganten']:
            self.short_url = f'https://www.elgiganten.dk/product/{self.part_num}/'
        elif self.URL_domain == domains['avxperten']:
            self.short_url = self.URL
        elif self.URL_domain == domains['av-cables']:
            self.short_url = self.URL
        elif self.URL_domain == domains['amazon']:
            self.short_url = self.URL
        elif self.URL_domain == domains['ebay']:
            if self.URL.split('/')[3] == 'itm':
                self.short_url = f'https://www.ebay.com/itm/{self.part_num}'
            else:
                self.short_url = self.URL.split('?')[0]
        elif self.URL_domain == domains['power']:
            self.short_url = f'https://www.power.dk/{self.URL.split("/")[3]}/p-{self.part_num}'
        elif self.URL_domain == domains['expert']:
            self.short_url = f'https://www.expert.dk/{self.URL.split("/")[3]}/p-{self.part_num}'
        elif self.URL_domain == domains['mm-vision']:
            self.short_url = self.URL
        elif self.URL_domain == domains['coolshop']:
            self.short_url = f'https://www.coolshop.dk/produkt/{self.URL.split("/")[-2]}/'
        elif self.URL_domain == domains['sharkgaming']:
            self.short_url = self.URL

    def print_info(self):
        """Print info about the product in the terminal."""
        print(f'Category: {self.cat}\n'
              f'Name: {self.name}\n'
              f'Price: {self.price} kr.\n'
              f'Date: {self.date}\n'
              f'From domain: {self.URL_domain}\n'
              f'Product number: {self.part_num}\n')

    def save_record(self):
        """Save the price of the product in the JSON-file."""
        self.logger.info('Saving record...')
        self.check_url()
        with open('records.json', 'r') as json_file:
            data = json.load(json_file)
            data[self.cat][self.name][self.URL_domain]["dates"][self.date] = {"price": self.price}
        with open('records.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
        self.logger.info('Record saved')


def change_name(name):
    """
    Change the name of the product, so if a similiar product is also
    being scraped, the similar products goes under the same name.
    """
    if 'asus' in name and 'rtx' in name and '2080' in name and 'ti' in name and 'rog' in name and 'strix' in name:
        name = 'asus geforce rtx 2080 ti rog strix oc'
    elif 'asus' in name and 'rtx' in name and '3080' in name and 'rog' in name and 'strix' in name and 'oc' in name:
        name = 'asus geforce rtx 3080 rog strix oc'
    elif 'corsair' in name and 'mp600' in name and '1tb' in name and 'm.2' in name:
        name = 'corsair force mp600 1tb m.2'
    return name


def change_æøå(name):
    """Change the letters æ, ø and å to international letters to avoid unicode and return the new name."""
    replace_letters = {
        "æ": "ae",
        "ø": "oe",
        "å": "aa"
    }

    for letter in replace_letters:
        name = name.replace(letter, replace_letters[letter])

    return name


class Komplett(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('div', class_='product-main-info__info').h1.span.text.lower()
        self.price = self.html_soup.find('span', class_='product-price-now').text.strip(',-').replace('.', '')


class Proshop(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('div', class_='col-xs-12 col-sm-7').h1.text.lower()
        try:
            # find normal price
            self.price = self.html_soup.find('span', class_='site-currency-attention').text.split(',')[0].replace('.', '')
        except AttributeError:
            try:
                # find discount price
                self.price = self.html_soup.find('div', class_='site-currency-attention site-currency-campaign').text.split(',')[0].replace('.', '')
            except AttributeError:
                # if campaign is sold out (udsolgt)
                self.price = self.html_soup.find('div', class_='site-currency-attention').text.split(',')[0].replace('.', '')


class Computersalg(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('h1', itemprop='name').text.lower()
        self.price = self.html_soup.find('span', itemprop='price').text.strip().split(',')[0].replace('.', '')


class Elgiganten(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('h1', class_='product-title').text.lower()
        self.price = self.html_soup.find('div', class_='product-price-container').text.strip().replace(u'\xa0', '')


class AvXperten(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('div', class_='content-head').text.strip().lower()
        self.price = self.html_soup.find('div', class_='price').text.replace(u'\xa0DKK', '')


class AvCables(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('h1', class_='title').text.lower()
        self.price = self.html_soup.find('div', class_='regular-price').text.strip().replace('Pris:   ', '').split(',')[0]


class Amazon(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('span', id='productTitle').text.strip().lower()
        self.price = self.html_soup.find('span', id='priceblock_ourprice').text.replace('$', '')


class eBay(Scraper):
    def get_info(self):
        if self.URL.split('/')[3] == 'itm':
            self.name = self.URL.split('/')[4].replace('-', ' ').lower()
            self.price = self.html_soup.find('span', id='convbinPrice').text.replace('(including shipping)', '').replace('DKK ', '').replace(',', '')
        else:
            self.name = self.html_soup.find('h1', class_='product-title').text.lower()
            self.price = self.html_soup.find('div', class_='display-price').text.replace('DKK ', '').replace(',', '')


class Power(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('title').text.replace(' - Power.dk', '').lower()
        self.price = self.html_soup.find('meta', property='product:price:amount')['content'].split(',')[0]


class Expert(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('meta', property='og:title')['content'].lower()
        self.price = self.html_soup.find('meta', property='product:price:amount')['content'].split(',')[0]


class MMVision(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('h1', itemprop='name').text.strip().lower()
        self.price = self.html_soup.find('h3', class_='product-price text-right').text.replace(',-', '').replace('.', '')


class Coolshop(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('div', class_='thing-header').text.strip().lower()
        self.price = self.html_soup.find('meta', property='product:price:amount')['content'].split('.')[0]


class Sharkgaming(Scraper):
    def get_info(self):
        self.name = self.html_soup.find('div', class_='product-name').text.strip().lower()
        self.price = self.html_soup.find('span', class_='price').text.replace(' kr.', '').replace('.', '')


domains = {
    "komplett": "www.komplett.dk",
    "proshop": "www.proshop.dk",
    "computersalg": "www.computersalg.dk",
    "elgiganten": "www.elgiganten.dk",
    "avxperten": "www.avxperten.dk",
    "av-cables": "www.av-cables.dk",
    "amazon": "www.amazon.com",
    "ebay": "www.ebay.com",
    "power": "www.power.dk",
    "expert": "www.expert.dk",
    "mm-vision": "www.mm-vision.dk",
    "coolshop": "www.coolshop.dk",
    "sharkgaming": "sharkgaming.dk"
}


if __name__ == '__main__':
    print('If you want to scrape your products, then run "scrape_links.py" instead of this file')
