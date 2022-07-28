from typing import Callable
import requests
from requests import Response
from bs4 import BeautifulSoup
import json
import logging
from abc import ABC, abstractmethod
from scraper.format import Format, Info
from scraper.constants import REQUEST_HEADER, REQUEST_COOKIES


def request_url(url: str) -> Response:
    try:
        response = requests.get(url, headers=REQUEST_HEADER, cookies=REQUEST_COOKIES, timeout=10)
        return response
    except requests.exceptions.RequestException:  # temporary try expect for all requests errors
        logging.getLogger(__name__).exception(f"Module requests exception with url: {url}")


class BaseWebsiteHandler(ABC):
    def __init__(self, url: str) -> None:
        # super().__init__()
        self.url = url
        self.website_name = get_website_name(url)

    def get_product_info(self) -> Info:
        try:
            request_data = self._request_product_data()
            self._get_common_data(request_data)
            raw_name = self._get_product_name(request_data)
            name = Format.get_user_product_name(raw_name)
            price = self._get_product_price(request_data)
            currency = self._get_product_currency(request_data)
            id = self._get_product_id(request_data)
            return Info(name, price, currency, id)
        except (AttributeError, ValueError, TypeError):
            logging.getLogger(__name__).exception(f"Could not get all the data needed from url: {self.url}")
            return Info(None, None, None, None, valid=False)

    def _request_product_data(self) -> BeautifulSoup:
        # option for each specific class to change how the request data is being handled
        response = request_url(self.url)
        return BeautifulSoup(response.text, "html.parser")

    def _get_common_data(self, soup) -> None:
        # if the same data needs to be accessed from more than one of the abstract methods,
        # then you can use this method to store the data as a instance variable,
        # so that the other methods can access the data
        pass

    @abstractmethod
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_product_price(self, soup: BeautifulSoup) -> float:
        pass

    @abstractmethod
    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_product_id(self, soup: BeautifulSoup) -> str:
        pass


class KomplettHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("div", class_="product-main-info__info").h1.span.text.lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("span", class_="product-price-now").text.strip(",-").replace(".", ""))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        script_tag = soup.find("script", type="application/ld+json").contents[0]
        currency = json.loads(script_tag).get("offers").get("priceCurrency")
        return currency

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find("span", itemprop="sku").text


class ProshopHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup):
        soup_script_tag = soup.find("script", type="application/ld+json").contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("div", class_="col-xs-12 col-sm-7").h1.text.lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        try:
            # find normal price
            price = float(
                soup.find("span", class_="site-currency-attention").text.replace(".", "").replace(",", ".").strip(" kr")
            )
        except AttributeError:
            try:
                # find discount price
                price = float(
                    soup.find("div", class_="site-currency-attention site-currency-campaign")
                    .text.replace(".", "")
                    .replace(",", ".")
                    .strip(" kr")
                )
            except AttributeError:
                # if campaign is sold out (udsolgt)
                price = float(
                    soup.find("div", class_="site-currency-attention").text.replace(".", "").replace(",", ".").strip(" kr")
                )
        return price

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        currency = self.soup_script_tag_json.get("offers").get("priceCurrency")
        return currency

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        id = self.soup_script_tag_json.get("sku")
        return id


class ComputerSalgHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", itemprop="name").text.lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("span", itemprop="price").text.strip().replace(".", "").replace(",", "."))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("span", itemprop="priceCurrency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find("h2", class_="productIdentifierHeadline").span.text


class ElgigantenHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup) -> None:
        self.elgiganten_api_data = self._get_json_api_data()

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", class_="product-title").text.lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return self.elgiganten_api_data["data"]["product"]["currentPricing"]["price"]["value"]

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return self.elgiganten_api_data["data"]["product"]["currentPricing"]["price"]["currency"]

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return self.url.split("/")[-1]

    def _get_json_api_data(self) -> dict:
        # API link to get price and currency
        # The API link has a placeholder for where the product id should be "{id_number}" 
        elgiganten_api_link = "https://www.elgiganten.dk/cxorchestrator/dk/api?appMode=b2c&user=anonymous&operationName=getProductWithDynamicDetails&variables=%7B%22articleNumber%22%3A%22{id_number}%22%2C%22withCustomerSpecificPrices%22%3Afalse%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%229bfbc062032a2a6b924883b81508af5c77bbfc5f66cc41c7ffd7d519885ac5e4%22%7D%7D"
        id = self.url.split("/")[-1]
        api_link = elgiganten_api_link.replace("{id_number}", id)
        response = request_url(api_link)
        return response.json()


class AvXpertenHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup):
        soup_script_tag = soup.find("script", type="application/ld+json").contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("div", class_="content-head").text.strip().lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("div", class_="price").text.replace("\xa0DKK", ""))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return self.soup_script_tag_json.get("offers").get("priceCurrency")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return self.soup_script_tag_json.get("sku")


class AvCablesHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", class_="title").text.lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(
            soup.find("div", class_="regular-price")
            .text.strip()
            .replace("Pris:   ", "")
            .replace("Tilbudspris:   ", "")
            .split(",")[0]
        )

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="og:price:currency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        script_tag = soup.find("script", type="application/ld+json").contents[0]
        id = json.loads(script_tag).get("sku")
        return id


class AmazonHandler(BaseWebsiteHandler):
    # TODO: FIX GETTING INFO FROM THIS LINK: https://www.amazon.com/PlayStation-5-Console/dp/B09DFCB66S/?_encoding=UTF8&pd_rd_w=mNmTx&content-id=amzn1.sym.90935d8a-16d8-44ec-9874-f910bf2faf89&pf_rd_p=90935d8a-16d8-44ec-9874-f910bf2faf89&pf_rd_r=1RRG12NVBKDZZ01140TG&pd_rd_wg=juN0N&pd_rd_r=672a737c-4c52-4022-a216-2d88acad8f0a&ref_=pd_gw_crs_zg_bs_468642
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("span", id="productTitle").text.strip().lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        try:
            print("first")
            return float(soup.find("input", id="attach-base-product-price").get("value"))
        except:
            print("second")
            return float(soup.find("span", class_="a-price a-text-price a-size-medium").span.text.replace("$", ""))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        try:
            return soup.find("input", id="attach-currency-of-preference").get("value")
        except:
            return soup.find("a", id="icp-touch-link-cop").find("span", class_="icp-color-base").text.split(" ")[0]

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        try:
            return soup.find("input", id="ASIN").get("value")
        except:
            asin_json = json.loads(soup.find("span", id="cr-state-object").get("data-state"))
            return asin_json["asin"]


class EbayHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup):
        self.soup_url = soup.find("meta", property="og:url").get("content")

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="og:title").get("content").strip("  | eBay").lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        if self.soup_url.split("/")[3] == "itm":
            print("this is with itm")
            price = float(soup.find("span", itemprop="price").get("content"))
        else:
            print("this is with WITHOUT itm")
            price = float(soup.find("div", class_="display-price").text.replace("DKK ", "").replace(",", ""))

        return price

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        if self.soup_url.split("/")[3] == "itm":
            currency = soup.find("span", itemprop="priceCurrency").get("content")
        else:
            script_tag = soup.find("script", type="application/ld+json").contents[0]
            currency = (
                json.loads(script_tag)
                .get("mainEntity")
                .get("offers")
                .get("itemOffered")[0]
                .get("offers")[0]
                .get("priceCurrency")
            )

        return currency

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        if self.soup_url.split("/")[3] == "itm":
            id = soup.find("div", id="descItemNumber").text
        else:
            id = soup.find("div", class_="item-details").a.get("data-itemid")

        return id


class PowerHandler(BaseWebsiteHandler):
    # TODO: FIX GETTING INFO FROM THIS LINK: https://www.power.dk/tv-og-lyd/hovedtelefoner/traadloese-hovedtelefoner/jbl-tune-760-nc-over-ear-hovedtelefoner-sort/p-1192020/
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("title").text.replace(" - Power.dk", "").lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("meta", property="product:price:amount")["content"].replace(",", "."))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="product:price:currency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="og:url").get("content").split("/")[-2].strip("p-")


class ExpertHandler(BaseWebsiteHandler):
    # TODO: UPDATE TO GET INFO FROM THIS LINK: https://www.expert.dk/mobil/mobiltelefoner/apple-iphone-13-pro-128-gb-skyfri-blaa/p-1204160/
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="og:title")["content"].lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("meta", property="product:price:amount")["content"].replace(",", "."))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="product:price:currency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="og:url").get("content").split("/")[-2].strip("p-")


class MMVisionHandler(BaseWebsiteHandler):
    # TODO: UPDATE TO GET INFO FROM THIS LINK: https://www.mm-vision.dk/visiongaming/vision-first-gaming-VG-pc
    def _get_common_data(self, soup):
        soup_script_tag = soup.find_all("script", type="application/ld+json")[1].contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", itemprop="name").text.strip().lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("h3", class_="product-price text-right").text.replace(",-", "").replace(".", ""))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        currency = self.soup_script_tag_json.get("offers").get("priceCurrency")
        return currency

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        id = self.soup_script_tag_json.get("productID")
        return id


class CoolshopHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        # TODO: UPDATE TO GET INFO FROM THIS LINK: https://www.coolshop.dk/produkt/23C5P8/
        return soup.find("div", class_="thing-header").text.strip().lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("meta", property="product:price:amount")["content"].split(".")[0])

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="product:price:currency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find_all("div", id="attributeSku")[1].text.strip()


class SharkGamingHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="og:title").get("content").lower()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("meta", property="product:price:amount").get("content"))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="product:price:currency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", itemprop="productID").get("content")


class NeweggHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup):
        script_data_raw = soup.find_all("script", type="application/ld+json")[2].text
        self.product_data = json.loads(script_data_raw)

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return self.product_data.get("name")

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(self.product_data.get("offers").get("price"))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return self.product_data.get("offers").get("priceCurrency")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return self.product_data.get("sku")


def get_website_name(url: str) -> str:
    domain = url.split("/")[2]

    # Remove "www." and the TLD/DNS name (such as ".com")
    website_name_list = domain.strip("www.").split(".")[:-1]
    website_name = ".".join(website_name_list)
    return website_name


def get_website_handler(url: str) -> BaseWebsiteHandler:
    website_name = get_website_name(url).lower()

    match website_name:
        case "komplett":
            return KomplettHandler(url)
        case "proshop":
            return ProshopHandler(url)
        case "computersalg":
            return ComputerSalgHandler(url)
        case "elgiganten":
            return ElgigantenHandler(url)
        case "avxperten":
            return AvXpertenHandler(url)
        case "av-cables":
            return AvCablesHandler(url)
        case "amazon":
            return AmazonHandler(url)
        case "ebay":
            return EbayHandler(url)
        case "power":
            return PowerHandler(url)
        case "expert":
            return ExpertHandler(url)
        case "mm-vision":
            return MMVisionHandler(url)
        case "coolshop":
            return CoolshopHandler(url)
        case "sharkgaming":
            return SharkGamingHandler(url)
        case "newegg":
            return NeweggHandler(url)
        case _:
            logging.getLogger(__name__).error(
                f"Can't find a website handler - website: '{website_name}' possibly not supported"
            )
            return None


def komplett(soup: BeautifulSoup) -> Info:
    name = soup.find("div", class_="product-main-info__info").h1.span.text.lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("span", class_="product-price-now").text.strip(",-").replace(".", ""))
    script_tag = soup.find("script", type="application/ld+json").contents[0]
    currency = json.loads(script_tag).get("offers").get("priceCurrency")
    id = soup.find("span", itemprop="sku").text
    return Info(product_user_name, price, currency, id)


def proshop(soup: BeautifulSoup) -> Info:
    name = soup.find("div", class_="col-xs-12 col-sm-7").h1.text.lower()
    product_user_name = Format.get_user_product_name(name)
    try:
        # find normal price
        price = float(soup.find("span", class_="site-currency-attention").text.replace(".", "").replace(",", ".").strip(" kr"))
    except AttributeError:
        try:
            # find discount price
            price = float(
                soup.find("div", class_="site-currency-attention site-currency-campaign")
                .text.replace(".", "")
                .replace(",", ".")
                .strip(" kr")
            )
        except AttributeError:
            # if campaign is sold out (udsolgt)
            price = float(
                soup.find("div", class_="site-currency-attention").text.replace(".", "").replace(",", ".").strip(" kr")
            )
    script_tag = soup.find("script", type="application/ld+json").contents[0]
    currency = json.loads(script_tag).get("offers").get("priceCurrency")
    id = json.loads(script_tag).get("sku")
    return Info(product_user_name, price, currency, id)


def computersalg(soup: BeautifulSoup) -> Info:
    name = soup.find("h1", itemprop="name").text.lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("span", itemprop="price").text.strip().replace(".", "").replace(",", "."))
    currency = soup.find("span", itemprop="priceCurrency").get("content")
    id = soup.find("h2", class_="productIdentifierHeadline").span.text
    return Info(product_user_name, price, currency, id)


def elgiganten(soup: BeautifulSoup) -> Info:
    name = soup.find("h1", class_="product-title").text.lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("div", class_="product-price-container").text.strip().replace("\xa0", ""))
    currency = soup.find("meta", itemprop="priceCurrency").get("content")
    id = soup.find("meta", itemprop="sku").get("content")
    return Info(product_user_name, price, currency, id)


def avxperten(soup: BeautifulSoup) -> Info:
    name = soup.find("div", class_="content-head").text.strip().lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("div", class_="price").text.replace("\xa0DKK", ""))
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
    name = soup.find("meta", property="og:title").get("content").strip("  | eBay").lower()
    product_user_name = Format.get_user_product_name(name)

    url = soup.find("meta", property="og:url").get("content")

    if url.split("/")[3] == "itm":
        price = float(soup.find("span", itemprop="price").get("content"))
        currency = soup.find("span", itemprop="priceCurrency").get("content")
        id = soup.find("div", id="descItemNumber").text
    else:
        price = float(soup.find("div", class_="display-price").text.replace("DKK ", "").replace(",", ""))
        script_tag = soup.find("script", type="application/ld+json").contents[0]
        currency = (
            json.loads(script_tag).get("mainEntity").get("offers").get("itemOffered")[0].get("offers")[0].get("priceCurrency")
        )
        id = soup.find("div", class_="item-details").a.get("data-itemid")

    return Info(product_user_name, price, currency, id)


def power(soup: BeautifulSoup) -> Info:
    name = soup.find("title").text.replace(" - Power.dk", "").lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("meta", property="product:price:amount")["content"].replace(",", "."))
    currency = soup.find("meta", property="product:price:currency").get("content")
    id = soup.find("meta", property="og:url").get("content").split("/")[-2].strip("p-")
    return Info(product_user_name, price, currency, id)


def expert(soup: BeautifulSoup) -> Info:
    name = soup.find("meta", property="og:title")["content"].lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("meta", property="product:price:amount")["content"].replace(",", "."))
    currency = soup.find("meta", property="product:price:currency").get("content")
    id = soup.find("meta", property="og:url").get("content").split("/")[-2].strip("p-")
    return Info(product_user_name, price, currency, id)


def mmvision(soup: BeautifulSoup) -> Info:
    name = soup.find("h1", itemprop="name").text.strip().lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("h3", class_="product-price text-right").text.replace(",-", "").replace(".", ""))
    script_tag = soup.find_all("script", type="application/ld+json")[1].contents[0]
    currency = json.loads(script_tag).get("offers").get("priceCurrency")
    id = json.loads(script_tag).get("productID")
    return Info(product_user_name, price, currency, id)


def coolshop(soup: BeautifulSoup) -> Info:
    name = soup.find("div", class_="thing-header").text.strip().lower()
    product_user_name = Format.get_user_product_name(name)
    price = float(soup.find("meta", property="product:price:amount")["content"].split(".")[0])
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


def newegg(soup: BeautifulSoup) -> Info:
    script_data_raw = soup.find_all("script", type="application/ld+json")[2].text
    product_data = json.loads(script_data_raw)
    name = product_data.get("name")
    product_user_name = Format.get_user_product_name(name)
    price = float(product_data.get("offers").get("price"))
    currency = product_data.get("offers").get("priceCurrency")
    id = product_data.get("sku")
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
    "newegg": newegg,
}
