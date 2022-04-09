from typing import Callable
from bs4 import BeautifulSoup
import json
from scraper.format import Format, Info


def get_website_name(url: str) -> str:
    domain = url.split("/")[2]

    # Remove "www." and the TLD/DNS name (such as ".com")
    website_name_list = domain.strip("www.").split(".")[:-1]
    website_name = ".".join(website_name_list)
    return website_name


def get_website_function(website_name: str) -> Callable[[BeautifulSoup], Info]:
    return domains[website_name]


def komplett(soup: BeautifulSoup) -> Info:
    name = soup.find("div", class_="product-main-info__info").h1.span.text.lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(
        soup.find("span", class_="product-price-now").text.strip(",-").replace(".", "")
    )
    script_tag = soup.find("script", type="application/ld+json").contents[0]
    currency = json.loads(script_tag).get("offers").get("priceCurrency")
    id = soup.find("span", itemprop="sku").text
    return Info(product_user_name, price, currency, id)


def proshop(soup: BeautifulSoup) -> Info:
    name = soup.find("div", class_="col-xs-12 col-sm-7").h1.text.lower()
    product_user_name = Format.get_user_product_name(name)
    try:
        # find normal price
        price = float(
            soup.find("span", class_="site-currency-attention")
            .text.replace(".", "")
            .replace(",", ".")
            .strip(" kr")
        )
    except AttributeError:
        try:
            # find discount price
            price = float(
                soup.find(
                    "div", class_="site-currency-attention site-currency-campaign"
                )
                .text.replace(".", "")
                .replace(",", ".")
                .strip(" kr")
            )
        except AttributeError:
            # if campaign is sold out (udsolgt)
            price = float(
                soup.find("div", class_="site-currency-attention")
                .text.replace(".", "")
                .replace(",", ".")
                .strip(" kr")
            )
    script_tag = soup.find("script", type="application/ld+json").contents[0]
    currency = json.loads(script_tag).get("offers").get("priceCurrency")
    id = json.loads(script_tag).get("sku")
    return Info(product_user_name, price, currency, id)


def computersalg(soup: BeautifulSoup) -> Info:
    name = soup.find("h1", itemprop="name").text.lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(
        soup.find("span", itemprop="price")
        .text.strip()
        .replace(".", "")
        .replace(",", ".")
    )
    currency = soup.find("span", itemprop="priceCurrency").get("content")
    id = soup.find("h2", class_="productIdentifierHeadline").span.text
    return Info(product_user_name, price, currency, id)


def elgiganten(soup: BeautifulSoup) -> Info:
    name = soup.find("h1", class_="product-title").text.lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(
        soup.find("div", class_="product-price-container")
        .text.strip()
        .replace(u"\xa0", "")
    )
    currency = soup.find("meta", itemprop="priceCurrency").get("content")
    id = soup.find("meta", itemprop="sku").get("content")
    return Info(product_user_name, price, currency, id)


def avxperten(soup: BeautifulSoup) -> Info:
    name = soup.find("div", class_="content-head").text.strip().lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("div", class_="price").text.replace(u"\xa0DKK", ""))
    script_tag = soup.find("script", type="application/ld+json").contents[0]
    currency = json.loads(script_tag).get("offers").get("priceCurrency")
    id = json.loads(script_tag).get("sku")
    return Info(product_user_name, price, currency, id)


def avcables(soup: BeautifulSoup) -> Info:
    name = soup.find("h1", class_="title").text.lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(
        soup.find("div", class_="regular-price")
        .text.strip()
        .replace("Pris:   ", "")
        .replace("Tilbudspris:   ", "")
        .split(",")[0]
    )
    currency = soup.find("meta", property="og:price:currency").get("content")
    script_tag = soup.find("script", type="application/ld+json").contents[0]
    id = json.loads(script_tag).get("sku")
    return Info(product_user_name, price, currency, id)


def amazon(soup: BeautifulSoup) -> Info:
    name = soup.find("span", id="productTitle").text.strip().lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("input", id="attach-base-product-price").get("value"))
    currency = soup.find("input", id="attach-currency-of-preference").get("value")
    id = soup.find("input", id="ASIN").get("value")
    return Info(product_user_name, price, currency, id)


def ebay(soup: BeautifulSoup) -> Info:
    name = (
        soup.find("meta", property="og:title").get("content").strip("  | eBay").lower()
    )
    product_user_name = Format.get_user_product_name(name)

    url = soup.find("meta", property="og:url").get("content")

    if url.split("/")[3] == "itm":
        price = float(soup.find("span", itemprop="price").get("content"))
        currency = soup.find("span", itemprop="priceCurrency").get("content")
        id = soup.find("div", id="descItemNumber").text
    else:
        price = float(
            soup.find("div", class_="display-price")
            .text.replace("DKK ", "")
            .replace(",", "")
        )
        script_tag = soup.find("script", type="application/ld+json").contents[0]
        currency = (
            json.loads(script_tag)
            .get("mainEntity")
            .get("offers")
            .get("itemOffered")[0]
            .get("offers")[0]
            .get("priceCurrency")
        )
        id = soup.find("div", class_="item-details").a.get("data-itemid")

    return Info(product_user_name, price, currency, id)


def power(soup: BeautifulSoup) -> Info:
    name = soup.find("title").text.replace(" - Power.dk", "").lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(
        soup.find("meta", property="product:price:amount")["content"].replace(",", ".")
    )
    currency = soup.find("meta", property="product:price:currency").get("content")
    id = soup.find("meta", property="og:url").get("content").split("/")[-2].strip("p-")
    return Info(product_user_name, price, currency, id)


def expert(soup: BeautifulSoup) -> Info:
    name = soup.find("meta", property="og:title")["content"].lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(
        soup.find("meta", property="product:price:amount")["content"].replace(",", ".")
    )
    currency = soup.find("meta", property="product:price:currency").get("content")
    id = soup.find("meta", property="og:url").get("content").split("/")[-2].strip("p-")
    return Info(product_user_name, price, currency, id)


def mmvision(soup: BeautifulSoup) -> Info:
    name = soup.find("h1", itemprop="name").text.strip().lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(
        soup.find("h3", class_="product-price text-right")
        .text.replace(",-", "")
        .replace(".", "")
    )
    script_tag = soup.find_all("script", type="application/ld+json")[1].contents[0]
    currency = json.loads(script_tag).get("offers").get("priceCurrency")
    id = json.loads(script_tag).get("productID")
    return Info(product_user_name, price, currency, id)


def coolshop(soup: BeautifulSoup) -> Info:
    name = soup.find("div", class_="thing-header").text.strip().lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(
        soup.find("meta", property="product:price:amount")["content"].split(".")[0]
    )
    currency = soup.find("meta", property="product:price:currency").get("content")
    id = soup.find_all("div", id="attributeSku")[1].text.strip()
    return Info(product_user_name, price, currency, id)


def sharkgaming(soup: BeautifulSoup) -> Info:
    name = soup.find("meta", property="og:title").get("content").lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("meta", property="product:price:amount").get("content"))
    currency = soup.find("meta", property="product:price:currency").get("content")
    id = soup.find("meta", itemprop="productID").get("content")
    return Info(product_user_name, price, currency, id)


domains = {
    "komplett": komplett,
    "proshop": proshop,
    "computersalg": computersalg,
    "elgiganten": elgiganten,
    "avxperten": avxperten,
    "av-cables": avcables,
    "amazon": amazon,
    "ebay": ebay,
    "power": power,
    "expert": expert,
    "mm-vision": mmvision,
    "coolshop": coolshop,
    "sharkgaming": sharkgaming,
}
