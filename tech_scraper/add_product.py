#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
from scraper import change_name, change_æøå, domains
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
    data = {}

    # Check for if any of the optional arguments is true
    if any([args.komplett, args.proshop, args.computersalg, args.elgiganten, args.avxperten, args.avcables,
            args.amazon, args.ebay, args.power, args.expert, args.mmvision, args.coolshop, args.sharkgaming]):
        # Add only the chosen domain arguments to json-file
        [data.update({f"{domains[domain]}": {"info": {"part_num": "", "url": ""}, "dates": {}}}) for domain in domains.keys() if args_domains[domain]]
    else:
        # If none of the optional arguments is giving (true), then add all of the domains to the json_object
        [data.update({f"{domains[domain]}": {"info": {"part_num": "", "url": ""}, "dates": {}}}) for domain in domains.keys()]

    return data


def save_json(category, product_name):
    """Save (category and) product-name in JSON-file."""
    with open('records.json', 'r') as json_file:
        data = json.load(json_file)

    with open('records.json', 'w') as json_file:
        if category not in data.keys():
            data[category] = {}

        data[category][product_name] = check_arguments()

        json.dump(data, json_file, indent=2)


def find_domain(domain):
    """Return the domain name of the url. Used to determine which class to call in scrape_link.py"""

    class_domains = {
        "www.komplett.dk": "Komplett",
        "www.proshop.dk": "Proshop",
        "www.computersalg.dk": "Computersalg",
        "www.elgiganten.dk": "Elgiganten",
        "www.avxperten.dk": "AvXperten",
        "www.av-cables.dk": "AvCables",
        "www.amazon.com": "Amazon",
        "www.ebay.com": "eBay",
        "www.power.dk": "Power",
        "www.expert.dk": "Expert",
        "www.mm-vision.dk": "MMVision",
        "www.coolshop.dk": "Coolshop",
        "sharkgaming.dk": "Sharkgaming",
    }

    return class_domains[domain]


def add_to_scraper(category, link, url_domain):
    """Add line to scraping.py, so scraping.py can scrape the new product."""
    domain = find_domain(url_domain)

    with open('scrape_links.py', 'a+') as python_file:
        python_file.write(f'scraper.{domain}(\'{category}\', \'{link}\')\n')
        print(f'{category}\n{link}')


def main(category, link):
    URL_domain = link.split('/')[2]

    product_name = get_product_name(link)

    if not product_name:
        print(f'Sorry, but I can\'t scrape from this domain: {URL_domain}')
        return

    # Change æ, ø and/or å
    category = change_æøå(category)
    product_name = change_æøå(product_name)

    save_json(category, product_name)
    add_to_scraper(category, link, URL_domain)


if __name__ == '__main__':
    args = argparse_setup()

    args_domains = {
        "komplett": args.komplett,
        "proshop": args.proshop,
        "computersalg": args.computersalg,
        "elgiganten": args.elgiganten,
        "avxperten": args.avxperten,
        "av-cables": args.avcables,
        "amazon": args.amazon,
        "ebay": args.ebay,
        "power": args.power,
        "expert": args.expert,
        "mm-vision": args.mmvision,
        "coolshop": args.coolshop,
        "sharkgaming": args.sharkgaming
    }

    main(args.category, args.url)
