import requests
from bs4 import BeautifulSoup


class Product:
    def __init__(self, URL):
        self.URL = URL
        #self.eng_weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self.eng_weekday = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
        self.dk_weekday = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag']
        self.get_info()

    def get_info(self):
        self.response = requests.get(self.URL)
        self.html_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.name = self.html_soup.find_all('div', class_='OfferViewer__OfferInfo-sc-1szo1sw-3 iWnqqD')[0].h1.text
        self.price = self.html_soup.find_all('div', class_='OfferPriceTag__BlockPrice-sc-1pyebvs-6 bnLaAp')[0].text
        self.amount = f"{''.join(self.html_soup.find_all('div', class_ = 'OfferPriceTag__BlockUnitPricing-sc-1pyebvs-7 gLfEkT')[0].text.split('cl')[0])}cl"
        self.date = ' '.join(self.html_soup.find_all('time')[0].text.split(' ')[0:4])
        self.weekday = self.html_soup.find_all('time')[0].text.split(' ')[3]
        if self.weekday.lower() in self.eng_weekday:
            self.translate_weekday()
        self.expire = self.html_soup.find_all('time')[0].text.split(' ')[4]
        if int(self.expire) > 1:
            self.expire += ' dage'
        else:
            self.expire += ' dag'

    def print_info(self):
        print(f'Navn: {self.name}\nPris: {self.price}\nMængde:  {self.amount}\nSenest dato: {self.date}\nUdløber om: {self.expire}\n')

    def translate_weekday(self):
        for weekday in self.eng_weekday:
            if self.weekday.lower() == weekday:
                self.weekday = self.dk_weekday[self.eng_weekday[weekday]]
                self.date = f'Til og med {self.weekday}'



#test1 = Product('https://etilbudsavis.dk/offers/FQWpw4qoy5ReOKnG0PwIL')
#test1.print_info()

#test2 = Product('https://etilbudsavis.dk/offers/6zYhqybnRknD6js0tQTLp')
#test2.print_info()



with open('etilbudsavis_links.txt', 'r') as txt_file:
    text_lines = txt_file.readlines()

count = 1
for line in text_lines:
    print(f'Produkt {count}:')
    print(f'Link: {line.strip()}')
    Product(line.strip()).print_info()
    count += 1
