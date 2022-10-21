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
    except requests.RequestException:
        logging.getLogger(__name__).exception(f"Module requests exception with url: {url}")


class BaseWebsiteHandler(ABC):
    def __init__(self, url: str) -> None:
        # super().__init__()
        self.url = url
        self.website_name = get_website_name(url)
        self.info: Info = None

    def get_product_info(self) -> Info:
        try:
            self._request_product_data()
            self._get_common_data()
            raw_name = self._get_product_name()
            name = Format.get_user_product_name(raw_name.lower())
            price = self._get_product_price()
            currency = self._get_product_currency()
            id = self._get_product_id()
            self.info = Info(name, price, currency, id)
            return self.info
        except (AttributeError, ValueError, TypeError):
            logging.getLogger(__name__).exception(f"Could not get all the data needed from url: {self.url}")
            return Info(None, None, None, None, valid=False)

    def _request_product_data(self) -> None:
        # option for each specific class to change how the request data is being handled
        response = request_url(self.url)
        self.request_data = BeautifulSoup(response.text, "html.parser")

    def _get_common_data(self) -> None:
        # if the same data needs to be accessed from more than one of the abstract methods,
        # then you can use this method to store the data as a instance variable,
        # so that the other methods can access the data
        pass

    @abstractmethod
    def _get_product_name(self) -> str:
        pass

    @abstractmethod
    def _get_product_price(self) -> float:
        pass

    @abstractmethod
    def _get_product_currency(self) -> str:
        pass

    @abstractmethod
    def _get_product_id(self) -> str:
        pass

    @abstractmethod
    def get_short_url(self) -> str:
        pass


class KomplettHandler(BaseWebsiteHandler):
    def _get_product_name(self) -> str:
        return self.request_data.find("div", class_="product-main-info__info").h1.span.text

    def _get_product_price(self) -> float:
        return float(self.request_data.find("span", class_="product-price-now").text.strip(",-").replace(".", ""))

    def _get_product_currency(self) -> str:
        script_tag = self.request_data.find("script", type="application/ld+json").contents[0]
        currency = json.loads(script_tag).get("offers").get("priceCurrency")
        return currency

    def _get_product_id(self) -> str:
        return self.url.split("/")[4]

    def get_short_url(self) -> str:
        id = self._get_product_id()
        return f"https://www.komplett.dk/product/{id}"


class ProshopHandler(BaseWebsiteHandler):
    def _get_common_data(self):
        soup_script_tag = self.request_data.find("script", type="application/ld+json").contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self) -> str:
        return self.soup_script_tag_json["name"]

    def _get_product_price(self) -> float:
        try:
            # find normal price
            price = float(
                self.request_data.find("span", class_="site-currency-attention")
                .text.replace(".", "")
                .replace(",", ".")
                .strip(" kr")
            )
        except AttributeError:
            try:
                # find discount price
                price = float(
                    self.request_data.find("div", class_="site-currency-attention site-currency-campaign")
                    .text.replace(".", "")
                    .replace(",", ".")
                    .strip(" kr")
                )
            except AttributeError:
                # if campaign is sold out (udsolgt)
                price = float(
                    self.request_data.find("div", class_="site-currency-attention")
                    .text.replace(".", "")
                    .replace(",", ".")
                    .strip(" kr")
                )
        return price

    def _get_product_currency(self) -> str:
        currency = self.soup_script_tag_json.get("offers").get("priceCurrency")
        return currency

    def _get_product_id(self) -> str:
        return self.url.split("/")[-1]

    def get_short_url(self) -> str:
        id = self._get_product_id()
        return f"https://www.proshop.dk/{id}"


class ComputerSalgHandler(BaseWebsiteHandler):
    def _get_product_name(self) -> str:
        return self.request_data.find("header", class_="product-header grid_20").hgroup.h1.text

    def _get_product_price(self) -> float:
        return float(self.request_data.find("span", itemprop="price").text.strip().replace(".", "").replace(",", "."))

    def _get_product_currency(self) -> str:
        return self.request_data.find("span", itemprop="priceCurrency").get("content")

    def _get_product_id(self) -> str:
        return self.url.split("/")[4]

    def get_short_url(self) -> str:
        id = self._get_product_id()
        return f"https://www.computersalg.dk/i/{id}"


class ElgigantenHandler(BaseWebsiteHandler):
    def _get_common_data(self) -> None:
        self.elgiganten_api_data = self._get_json_api_data()

    def _get_product_name(self) -> str:
        return self.request_data.find("h1", class_="product-title").text

    def _get_product_price(self) -> float:
        return float(self.elgiganten_api_data["data"]["product"]["currentPricing"]["price"]["value"])

    def _get_product_currency(self) -> str:
        return self.elgiganten_api_data["data"]["product"]["currentPricing"]["price"]["currency"]

    def _get_product_id(self) -> str:
        return self.url.split("/")[-1]

    def _get_json_api_data(self) -> dict:
        id_number = self._get_product_id()
        # API link to get price and currency
        api_link = f"https://www.elgiganten.dk/cxorchestrator/dk/api?appMode=b2c&user=anonymous&operationName=getProductWithDynamicDetails&variables=%7B%22articleNumber%22%3A%22{id_number}%22%2C%22withCustomerSpecificPrices%22%3Afalse%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%229bfbc062032a2a6b924883b81508af5c77bbfc5f66cc41c7ffd7d519885ac5e4%22%7D%7D"
        response = request_url(api_link)
        return response.json()

    def get_short_url(self) -> str:
        id = self._get_product_id()
        return f"https://www.elgiganten.dk/product/{id}"


class AvXpertenHandler(BaseWebsiteHandler):
    def _get_common_data(self):
        soup_script_tag = self.request_data.find("script", type="application/ld+json").contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self) -> str:
        return self.request_data.find("div", class_="content-head").h1.text.strip()

    def _get_product_price(self) -> float:
        return float(self.request_data.find("div", class_="price").text.replace("\xa0DKK", ""))

    def _get_product_currency(self) -> str:
        return self.soup_script_tag_json.get("offers").get("priceCurrency")

    def _get_product_id(self) -> str:
        return self.soup_script_tag_json.get("sku")

    def get_short_url(self) -> str:
        return self.url


class AvCablesHandler(BaseWebsiteHandler):
    def _get_product_name(self) -> str:
        return self.request_data.find("h1", class_="title").text

    def _get_product_price(self) -> float:
        return float(
            self.request_data.find("div", class_="regular-price")
            .text.strip()
            .replace("Pris:   ", "")
            .replace("Tilbudspris:   ", "")
            .split(",")[0]
        )

    def _get_product_currency(self) -> str:
        return self.request_data.find("meta", property="og:price:currency").get("content")

    def _get_product_id(self) -> str:
        script_tag = self.request_data.find("script", type="application/ld+json").contents[0]
        id = json.loads(script_tag).get("sku")
        return str(id)

    def get_short_url(self) -> str:
        return self.url


class AmazonHandler(BaseWebsiteHandler):
    def _get_product_name(self) -> str:
        return self.request_data.find("span", id="productTitle").text.strip()

    def _get_product_price(self) -> float:
        try:
            return float(self.request_data.find("input", id="attach-base-product-price").get("value"))
        except (AttributeError, ValueError, TypeError):
            return float(
                self.request_data.find("span", class_="a-price a-text-price a-size-medium").span.text.replace("$", "")
            )

    def _get_product_currency(self) -> str:
        try:
            return self.request_data.find("input", id="attach-currency-of-preference").get("value")
        except (AttributeError, ValueError, TypeError):
            return (
                self.request_data.find("a", id="icp-touch-link-cop").find("span", class_="icp-color-base").text.split(" ")[0]
            )

    def _get_product_id(self) -> str:
        try:
            return self.request_data.find("input", id="ASIN").get("value")
        except (AttributeError, ValueError, TypeError):
            asin_json = json.loads(self.request_data.find("span", id="cr-state-object").get("data-state"))
            return asin_json["asin"]

    def get_short_url(self) -> str:
        return self.url


class EbayHandler(BaseWebsiteHandler):
    def _get_common_data(self):
        self.soup_url = self.request_data.find("meta", property="og:url").get("content")

    def _get_product_name(self) -> str:
        try:
            return self.request_data.find("h1", class_="product-title").text
        except (AttributeError, ValueError, TypeError):
            return self.request_data.find("meta", property="og:title").get("content").replace("  | eBay", "")

    def _get_product_price(self) -> float:
        if self.soup_url.split("/")[3] == "itm":
            price = float(self.request_data.find("span", itemprop="price").get("content"))
        else:
            price = float(
                self.request_data.find("div", class_="display-price")
                .text.replace("DKK ", "")
                .replace("$", "")
                .replace(",", "")
            )

        return price

    def _get_product_currency(self) -> str:
        if self.soup_url.split("/")[3] == "itm":
            currency = self.request_data.find("span", itemprop="priceCurrency").get("content")
        else:
            script_tag = self.request_data.find("script", type="application/ld+json").contents[0]
            currency = (
                json.loads(script_tag)
                .get("mainEntity")
                .get("offers")
                .get("itemOffered")[0]
                .get("offers")[0]
                .get("priceCurrency")
            )

        return currency

    def _get_product_id(self) -> str:
        return self.url.split("/")[4].split("?")[0]

    def get_short_url(self) -> str:
        id = self._get_product_id()

        if self.url.split("/")[3] == "itm":
            return f"https://www.ebay.com/itm/{id}"
        else:
            return f"https://www.ebay.com/p/{id}"


class PowerHandler(BaseWebsiteHandler):
    def _get_common_data(self) -> None:
        id = self._get_product_id()
        self.api_json = request_url(f"https://www.power.dk/api/v2/products?ids={id}").json()

    def _get_product_name(self) -> str:
        return self.api_json[0].get("title")

    def _get_product_price(self) -> float:
        return float(self.api_json[0].get("price"))

    def _get_product_currency(self) -> str:
        return "DKK"

    def _get_product_id(self) -> str:
        return self.url.split("/")[-2].strip("p-")

    def get_short_url(self) -> str:
        id = self._get_product_id()
        url_id = self.url.split("/")[3]
        return f"https://www.power.dk/{url_id}/p-{id}"


class ExpertHandler(BaseWebsiteHandler):
    def _get_common_data(self) -> None:
        id = self._get_product_id()
        self.api_json = request_url(f"https://www.expert.dk/api/v2/products?ids={id}").json()

    def _get_product_name(self) -> str:
        return self.api_json[0].get("title")

    def _get_product_price(self) -> float:
        return float(self.api_json[0].get("price"))

    def _get_product_currency(self) -> str:
        return "DKK"

    def _get_product_id(self) -> str:
        return self.url.split("/")[-2].strip("p-")

    def get_short_url(self) -> str:
        id = self._get_product_id()
        url_id = self.url.split("/")[3]
        return f"https://www.expert.dk/{url_id}/p-{id}"


class MMVisionHandler(BaseWebsiteHandler):
    def _get_common_data(self):
        soup_script_tag = self.request_data.find_all("script", type="application/ld+json")[1].contents[0]
        self.soup_script_tag_json = json.loads(soup_script_tag)

    def _get_product_name(self) -> str:
        return self.request_data.find("h1", itemprop="name").text.strip()

    def _get_product_price(self) -> float:
        return float(self.request_data.find("h3", class_="product-price text-right").text.strip("fra ").strip().strip(",-"))

    def _get_product_currency(self) -> str:
        return self.soup_script_tag_json.get("offers").get("priceCurrency")

    def _get_product_id(self) -> str:
        return self.soup_script_tag_json.get("productID")

    def get_short_url(self) -> str:
        return self.url


class CoolshopHandler(BaseWebsiteHandler):
    def _get_product_name(self) -> str:
        return self.request_data.find("div", class_="thing-header").h1.text.strip().replace("\n", " ")

    def _get_product_price(self) -> float:
        return float(self.request_data.find("meta", property="product:price:amount")["content"].split(".")[0])

    def _get_product_currency(self) -> str:
        return self.request_data.find("meta", property="product:price:currency").get("content")

    def _get_product_id(self) -> str:
        return self.request_data.find_all("div", id="attributeSku")[1].text.strip()

    def get_short_url(self) -> str:
        url_id = self.url.split("/")[-2]
        return f"https://www.coolshop.dk/produkt/{url_id}/"


class SharkGamingHandler(BaseWebsiteHandler):
    def _get_product_name(self) -> str:
        return self.request_data.find("h1", class_="page-title").span.text

    def _get_product_price(self) -> float:
        return float(self.request_data.find("meta", property="product:price:amount").get("content"))

    def _get_product_currency(self) -> str:
        return self.request_data.find("meta", property="product:price:currency").get("content")

    def _get_product_id(self) -> str:
        return json.loads(self.request_data.find_all("script", type="application/ld+json")[3].text).get("productID")

    def get_short_url(self) -> str:
        return self.url


class NeweggHandler(BaseWebsiteHandler):
    def _get_common_data(self):
        script_data_raw = self.request_data.find_all("script", type="application/ld+json")[2].text
        self.product_data = json.loads(script_data_raw)

    def _get_product_name(self) -> str:
        return self.product_data.get("name")

    def _get_product_price(self) -> float:
        return float(self.product_data.get("offers").get("price"))

    def _get_product_currency(self) -> str:
        return self.product_data.get("offers").get("priceCurrency")

    def _get_product_id(self) -> str:
        return self.url.split("/")[5].split("?")[0]

    def get_short_url(self) -> str:
        id = self._get_product_id()
        return f"https://www.newegg.com/p/{id}"


class HifiKlubbenHandler(BaseWebsiteHandler):
    def _get_product_name(self) -> str:
        brand_name = self.request_data.find("span", class_="product-page__brand-name").text
        model_name = self.request_data.find("span", class_="product-page__model-name").text
        return f"{brand_name} {model_name}"

    def _get_product_price(self) -> float:
        return float(self.request_data.find("meta", itemprop="price").get("content"))

    def _get_product_currency(self) -> str:
        return self.request_data.find("meta", itemprop="priceCurrency").get("content")

    def _get_product_id(self) -> str:
        return self.url.split("/")[4]

    def get_short_url(self) -> str:
        id = self._get_product_id()
        return f"https://www.hifiklubben.dk/{id}"


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
        case "hifiklubben":
            return HifiKlubbenHandler(url)
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
    "hifiklubben",
}
