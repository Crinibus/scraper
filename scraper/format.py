from scraper.filemanager import Config
from scraper.domains import Info


class Format:
    @staticmethod
    def shorten_url(website_name: str, url: str, info: Info) -> str:

        short_urls = {
            "komplett": f'https://www.komplett.dk/product/{info.partnum}',
            "proshop": f'https://www.proshop.dk/{info.partnum}',
            "computersalg": f'https://www.computersalg.dk/i/{info.partnum}',
            "elgiganten": f'https://www.elgiganten.dk/product/{info.partnum}/',
            "avxperten": url,
            "avcables": url,
            "amazon": url,
            "power": f'https://www.power.dk/{url.split("/")[3]}/p-{info.partnum}',
            "expert": f'https://www.expert.dk/{url.split("/")[3]}/p-{info.partnum}',
            "mmvision": url,
            "coolshop": f'https://www.coolshop.dk/produkt/{url.split("/")[-2]}/',
            "sharkgaming": url,
        }

        if website_name == "ebay":
            if url.split('/')[3] == 'itm':
                short_url = f'https://www.ebay.com/itm/{info.partnum}'
            else:
                short_url = url.split('?')[0]
        else:
            short_url = short_urls.get(website_name)

        return short_url

    @staticmethod
    def get_user_product_name(product_name: str) -> str:
        user_product_names = Config.get_user_product_names()

        for item in user_product_names:
            if "key" in item:
                key_list = user_product_names[item].split(',')
                value_key = f'value{item.strip("key")}'
                if all(elem in product_name for elem in key_list):
                    return user_product_names[value_key]
        return product_name
