#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
from scraping import change_name, change_æøå
import argparse


def argparse_setup():
    """Setup and return argparse."""
    parser = argparse.ArgumentParser()

    parser.add_argument('category',
                        help='the category the product is going to be in',
                        type=str)

    parser.add_argument('url',
                        help='the url to the product',
                        type=str)

    parser.add_argument('--komplett',
                        help='add only komplett-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--proshop',
                        help='add only proshop-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--computersalg',
                        help='add only computersalg-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--elgiganten',
                        help='add only elgiganten-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--avxperten',
                        help='add only avxperten-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--avcables',
                        help='add only avcables-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--amazon',
                        help='add only amazon-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--ebay',
                        help='add only ebay-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--power',
                        help='add only power-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--expert',
                        help='add only expert-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--mmvision',
                        help='add only mm-vision-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--coolshop',
                        help='add only coolshop-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--sharkgaming',
                        help='add only sharkgaming-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    return parser.parse_args()


def get_product_name(link):
    """Get and return name of the product from the link."""
    URL_domain = link.split('/')[2]

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
    cookies = dict(cookies_are='working')
    response = requests.get(link, headers=headers, cookies=cookies)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    if URL_domain == domains['komplett']:
        return change_name(html_soup.find('div', class_='product-main-info__info').h1.span.text.lower())
    elif URL_domain == domains['proshop']:
        return change_name(html_soup.find('div', class_='col-xs-12 col-sm-7').h1.text.lower())
    elif URL_domain == domains['computersalg']:
        return change_name(html_soup.find('h1', itemprop='name').text.lower())
    elif URL_domain == domains['elgiganten']:
        return change_name(html_soup.find('h1', class_='product-title').text.lower())
    elif URL_domain == domains['avxperten']:
        return change_name(html_soup.find('div', class_='content-head').text.strip().lower())
    elif URL_domain == domains['av-cables']:
        return change_name(html_soup.find('h1', class_='title').text.lower())
    elif URL_domain == domains['amazon']:
        return change_name(html_soup.find('span', id='productTitle').text.strip().lower())
    elif URL_domain == domains['ebay']:
        if link.split('/')[3] == 'itm':
            return change_name(link.split('/')[4].replace('-', ' ').lower())
        else:
            return change_name(html_soup.find('h1', class_='product-title').text.lower())
    elif URL_domain == domains['power']:
        return change_name(html_soup.find('title').text.replace(' - Power.dk', '').lower())
    elif URL_domain == domains['expert']:
        return change_name(html_soup.find('meta', property='og:title')['content'].lower())
    elif URL_domain == domains['mm-vision']:
        return change_name(html_soup.find('h1', itemprop='name').text.strip().lower())
    elif URL_domain == domains['coolshop']:
        return change_name(html_soup.find('div', class_='thing-header').text.strip().lower())
    elif URL_domain == domains['sharkgaming']:
        return change_name(html_soup.find('div', class_='product-name').text.strip().lower())
    else:
        return None


def check_arguments():
    """Check if any of the optional domain arguments is giving to the script
       and returns those that are as one json-object."""
    json_object = json.loads('{}')
    if args.komplett or args.proshop or args.computersalg or args.elgiganten or args.avxperten or args.avcables or args.amazon or args.ebay or args.power or args.expert or args.mmvision or args.coolshop or args.sharkgaming:
        if args.komplett:
            json_object.update({
                                    f"{domains['komplett']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.proshop:
            json_object.update({
                                    f"{domains['proshop']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.computersalg:
            json_object.update({
                                    f"{domains['computersalg']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.elgiganten:
            json_object.update({
                                    f"{domains['elgiganten']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.avxperten:
            json_object.update({
                                    f"{domains['avxperten']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.avcables:
            json_object.update({
                                    f"{domains['av-cables']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.amazon:
            json_object.update({
                                    f"{domains['amazon']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.ebay:
            json_object.update({
                                    f"{domains['ebay']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.power:
            json_object.update({
                                    f"{domains['power']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.expert:
            json_object.update({
                                    f"{domains['expert']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.mmvision:
            json_object.update({
                                    f"{domains['mm-vision']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.coolshop:
            json_object.update({
                                    f"{domains['coolshop']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.sharkgaming:
            json_object.update({
                                    f"{domains['sharkgaming']}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
    else:
        json_object = {
                            f"{domains['komplett']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['proshop']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['computersalg']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['elgiganten']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['avxperten']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['av-cables']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['amazon']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['ebay']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['power']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['expert']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['mm-vision']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['coolshop']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{domains['sharkgaming']}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            }
                        }
    return json_object


def save_json(kategori, produkt_navn):
    """Save (category and) product-name in JSON-file."""
    with open('records.json', 'r') as json_file:
        data = json.load(json_file)

    with open('records.json', 'w') as json_file:
        if kategori not in data.keys():
            data[kategori] = {}

        data[kategori][produkt_navn] = check_arguments()

        json.dump(data, json_file, indent=2)


def find_domain(domain):
    """Return the domain of the url without "www." and ".dk"."""
    if domain == domains['komplett']:
        return 'Komplett'
    elif domain == domains['proshop']:
        return 'Proshop'
    elif domain == domains['computersalg']:
        return 'Computersalg'
    elif domain == domains['elgiganten']:
        return 'Elgiganten'
    elif domain == domains['avxperten']:
        return 'AvXperten'
    elif domain == domains['av-cables']:
        return 'AvCables'
    elif domain == domains['amazon']:
        return 'Amazon'
    elif domain == domains['ebay']:
        return 'eBay'
    elif domain == domains['power']:
        return 'Power'
    elif domain == domains['expert']:
        return 'Expert'
    elif domain == domains['mm-vision']:
        return 'MMVision'
    elif domain == domains['coolshop']:
        return 'Coolshop'
    elif domain == domains['sharkgaming']:
        return 'Sharkgaming'


def add_to_scraper(kategori, link, url_domain):
    """Add line to scraping.py, so scraping.py can scrape the new product."""
    domain = find_domain(url_domain)

    with open('scraping.py', 'a+') as python_file:
        python_file.write(f'    {domain}(\'{kategori}\', \'{link}\')\n')
        print(f'{kategori}\n{link}')


def main(kategori, link):
    URL_domain = link.split('/')[2]

    produkt_navn = get_product_name(link)

    if not produkt_navn:
        print(f'Sorry, but I can\'t scrape from this domain: {URL_domain}')
        return

    # Change æ, ø and/or å
    kategori = change_æøå(kategori)
    produkt_navn = change_æøå(produkt_navn)

    save_json(kategori, produkt_navn)
    add_to_scraper(kategori, link, URL_domain)


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
    args = argparse_setup()
    main(args.category, args.url)
