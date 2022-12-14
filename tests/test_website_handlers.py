from abc import ABC, abstractmethod
from typing import Dict
from scraper.domains import (
    AmazonHandler,
    AvCablesHandler,
    AvXpertenHandler,
    ComputerSalgHandler,
    CoolshopHandler,
    EbayHandler,
    ElgigantenHandler,
    ExpertHandler,
    KomplettHandler,
    MMVisionHandler,
    NeweggHandler,
    PowerHandler,
    ProshopHandler,
    SharkGamingHandler,
    HifiKlubbenHandler,
)
from scraper.format import Info
from scraper.filemanager import Filemanager

test_objects_json = Filemanager.read_json("./tests/test_objects.json")
test_website_handlers_json: Dict[str, Dict[str, str]] = test_objects_json["test_website_handlers"]

komplett_test = test_website_handlers_json["komplett"]
proshop_test = test_website_handlers_json["proshop"]
computersalg_test = test_website_handlers_json["computersalg"]
elgiganten_test = test_website_handlers_json["elgiganten"]
avxperten_test = test_website_handlers_json["avxperten"]
avcables_test = test_website_handlers_json["av-cables"]
amazon_test = test_website_handlers_json["amazon"]
ebay_with_itm_test = test_website_handlers_json["ebay_with_itm"]
ebay_with_p_test = test_website_handlers_json["ebay_with_p"]
expert_test = test_website_handlers_json["expert"]
power_test = test_website_handlers_json["power"]
mmvision_test = test_website_handlers_json["mm-vision"]
coolshop_test = test_website_handlers_json["coolshop"]
sharkgaming_test = test_website_handlers_json["sharkgaming"]
newegg_test = test_website_handlers_json["newegg"]
hifiklubben_test = test_website_handlers_json["hifiklubben"]


class BaseTestWebsiteHandler(ABC):
    @abstractmethod
    def test_get_product_info(self) -> None:
        pass

    @abstractmethod
    def test_get_name(self) -> None:
        pass

    @abstractmethod
    def test_get_price(self) -> None:
        pass

    @abstractmethod
    def test_get_currency(self) -> None:
        pass

    @abstractmethod
    def test_get_id(self) -> None:
        pass


class TestKomplettHandler(BaseTestWebsiteHandler):
    test_handler = KomplettHandler(komplett_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = komplett_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == komplett_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == komplett_test["expected_id"]


class TestProshopHandler(BaseTestWebsiteHandler):
    test_handler = ProshopHandler(proshop_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = proshop_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == proshop_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == proshop_test["expected_id"]


class TestComputersalgHandler(BaseTestWebsiteHandler):
    test_handler = ComputerSalgHandler(computersalg_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = computersalg_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == computersalg_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == computersalg_test["expected_id"]


class TestElgigantenHandler(BaseTestWebsiteHandler):
    test_handler = ElgigantenHandler(elgiganten_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = elgiganten_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == elgiganten_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == elgiganten_test["expected_id"]


class TestAvXpertenHandler(BaseTestWebsiteHandler):
    test_handler = AvXpertenHandler(avxperten_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = avxperten_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == avxperten_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == avxperten_test["expected_id"]


class TestAvCablesHandler(BaseTestWebsiteHandler):
    test_handler = AvCablesHandler(avcables_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = avcables_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == avcables_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == avcables_test["expected_id"]


class TestAmazonHandler(BaseTestWebsiteHandler):
    test_handler = AmazonHandler(amazon_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = amazon_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == amazon_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == amazon_test["expected_id"]


# OBS: There is two Ebay versions - This is for url that start with 'ebay.com/itm/'
class TestEbayHandler_with_itm(BaseTestWebsiteHandler):
    test_handler = EbayHandler(ebay_with_itm_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = ebay_with_itm_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert len(currency) == 3
        assert currency == ebay_with_itm_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == ebay_with_itm_test["expected_id"]


# OBS: There is two Ebay versions - This is for url that start with 'ebay.com/p/'
class TestEbayHandler_with_p(BaseTestWebsiteHandler):
    test_handler = EbayHandler(ebay_with_p_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = ebay_with_p_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert len(currency) == 3
        # assert currency == ebay_with_p_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == ebay_with_p_test["expected_id"]


class TestPowerHandler(BaseTestWebsiteHandler):
    test_handler = PowerHandler(power_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = power_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == power_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == power_test["expected_id"]


class TestExpertHandler(BaseTestWebsiteHandler):
    test_handler = ExpertHandler(expert_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = expert_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == expert_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == expert_test["expected_id"]


class TestMMVisionHandler(BaseTestWebsiteHandler):
    test_handler = MMVisionHandler(mmvision_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = mmvision_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == mmvision_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == mmvision_test["expected_id"]


class TestCoolshopHandler(BaseTestWebsiteHandler):
    test_handler = CoolshopHandler(coolshop_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = coolshop_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == coolshop_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == coolshop_test["expected_id"]


class TestSharkGamingHandler(BaseTestWebsiteHandler):
    test_handler = SharkGamingHandler(sharkgaming_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = sharkgaming_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == sharkgaming_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == sharkgaming_test["expected_id"]


class TestNeweggHandler(BaseTestWebsiteHandler):
    test_handler = NeweggHandler(newegg_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = newegg_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == newegg_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == newegg_test["expected_id"]


class TestHifiKlubbenHandler(BaseTestWebsiteHandler):
    test_handler = HifiKlubbenHandler(hifiklubben_test["link"])
    test_handler._request_product_data()
    test_handler._get_common_data()

    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=self.test_handler.request_data)
        actual = self.test_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = self.test_handler._get_product_name().lower()
        expected = hifiklubben_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = self.test_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = self.test_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == hifiklubben_test["expected_currency"]

    def test_get_id(self) -> None:
        id = self.test_handler._get_product_id()
        assert isinstance(id, str)
        assert id == hifiklubben_test["expected_id"]
