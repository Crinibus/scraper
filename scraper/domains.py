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
        self.info: Info = None

    def get_product_info(self) -> Info:
        try:
            request_data = self._request_product_data()
            self._get_common_data(request_data)
            raw_name = self._get_product_name(request_data)
            name = Format.get_user_product_name(raw_name.lower())
            price = self._get_product_price(request_data)
            currency = self._get_product_currency(request_data)
            id = self._get_product_id(request_data)
            self.info = Info(name, price, currency, id)
            return self.info
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

    @abstractmethod
    def get_short_url(self) -> str:
        pass


class KomplettHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("div", class_="product-main-info__info").h1.span.text

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("span", class_="product-price-now").text.strip(",-").replace(".", ""))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        script_tag = soup.find("script", type="application/ld+json").contents[0]
        currency = json.loads(script_tag).get("offers").get("priceCurrency")
        return currency

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find("span", itemprop="sku").text

    def get_short_url(self) -> str:
        if not self.info:
            return None
        return f"https://www.komplett.dk/product/{self.info.id}"


class ProshopHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup):
        soup_script_tag = soup.find("script", type="application/ld+json").contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("div", class_="col-xs-12 col-sm-7").h1.text

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

    def get_short_url(self) -> str:
        if not self.info:
            return None
        return f"https://www.proshop.dk/{self.info.id}"


class ComputerSalgHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", itemprop="name").text

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("span", itemprop="price").text.strip().replace(".", "").replace(",", "."))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("span", itemprop="priceCurrency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find("h2", class_="productIdentifierHeadline").span.text

    def get_short_url(self) -> str:
        if not self.info:
            return None
        return f"https://www.computersalg.dk/i/{self.info.id}"


class ElgigantenHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup) -> None:
        self.elgiganten_api_data = self._get_json_api_data()

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", class_="product-title").text

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(self.elgiganten_api_data["data"]["product"]["currentPricing"]["price"]["value"])

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

    def get_short_url(self) -> str:
        if not self.info:
            return None
        return f"https://www.elgiganten.dk/product/{self.info.id}"


class AvXpertenHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup):
        soup_script_tag = soup.find("script", type="application/ld+json").contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("div", class_="content-head").h1.text.strip()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("div", class_="price").text.replace("\xa0DKK", ""))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return self.soup_script_tag_json.get("offers").get("priceCurrency")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return self.soup_script_tag_json.get("sku")

    def get_short_url(self) -> str:
        return self.url

class AvCablesHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", class_="title").text

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
        return str(id)

    def get_short_url(self) -> str:
        return self.url


class AmazonHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("span", id="productTitle").text.strip()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        try:
            return float(soup.find("input", id="attach-base-product-price").get("value"))
        except:
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

    def get_short_url(self) -> str:
        return self.url


class EbayHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup):
        self.soup_url = soup.find("meta", property="og:url").get("content")

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        try:
            return soup.find("h1", class_="product-title").text
        except:
            return soup.find("meta", property="og:title").get("content").strip("  | eBay")

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        if self.soup_url.split("/")[3] == "itm":
            price = float(soup.find("span", itemprop="price").get("content"))
        else:
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

    def get_short_url(self) -> str:
        if self.url.split("/")[3] != "itm":
            return self.url.split("?")[0]

        if not self.info:
            return None
        return f"https://www.ebay.com/itm/{self.info.id}"


class PowerHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup) -> None:
        self.id = self.url.split("/")[-2].strip("p-")
        self.api_json = request_url(f"https://www.power.dk/api/v2/products?ids={self.id}").json()

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return self.api_json[0].get("title")

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(self.api_json[0].get("price"))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return "DKK"

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return self.id

    def get_short_url(self) -> str:
        if not self.info:
            return None
        url_id = self.url.split('/')[3]
        return f"https://www.power.dk/{url_id}/p-{self.info.id}"


class ExpertHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup) -> None:
        self.id = self.url.split("/")[-2].strip("p-")
        self.api_json = request_url(f"https://www.expert.dk/api/v2/products?ids={self.id}").json()

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return self.api_json[0].get("title")

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(self.api_json[0].get("price"))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return "DKK"

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return self.id

    def get_short_url(self) -> str:
        if not self.info:
            return None
        url_id = self.url.split("/")[3]
        return f'https://www.expert.dk/{url_id}/p-{self.info.id}'


class MMVisionHandler(BaseWebsiteHandler):
    def _get_common_data(self, soup):
        soup_script_tag = soup.find_all("script", type="application/ld+json")[1].contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", itemprop="name").text.strip()

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("h3", class_="product-price text-right").text.strip("fra ").strip().strip(",-"))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        currency = self.soup_script_tag_json.get("offers").get("priceCurrency")
        return currency

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        id = self.soup_script_tag_json.get("productID")
        return id

    def get_short_url(self) -> str:
        return self.url


class CoolshopHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("div", class_="thing-header").h1.text.strip().replace("\n", " ")

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("meta", property="product:price:amount")["content"].split(".")[0])

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="product:price:currency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find_all("div", id="attributeSku")[1].text.strip()

    def get_short_url(self) -> str:
        url_id = self.url.split("/")[-2]
        return f'https://www.coolshop.dk/produkt/{url_id}/'


class SharkGamingHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", class_="page-title").span.text

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("meta", property="product:price:amount").get("content"))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return soup.find("meta", property="product:price:currency").get("content")

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return json.loads(soup.find_all("script", type="application/ld+json")[3].text).get("productID")

    def get_short_url(self) -> str:
        return self.url


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

    def get_short_url(self) -> str:
        if not self.info:
            return None
        return f"https://www.newegg.com/p/{self.info.id}"


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


SUPPORTED_DOMAINS = {
    "komplett",
    "proshop",
    "computersalg",
    "elgiganten",
    "avxperten",
    "av-cables",
    "amazon",
    "ebay",
    "power",
    "expert",
    "mm-vision",
    "coolshop",
    "sharkgaming",
    "newegg",
}
