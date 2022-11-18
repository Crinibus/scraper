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


komplett_handler = KomplettHandler(komplett_test["link"])
komplett_handler._request_product_data()
komplett_handler._get_common_data()

proshop_handler = ProshopHandler(proshop_test["link"])
proshop_handler._request_product_data()
proshop_handler._get_common_data()

computersalg_handler = ComputerSalgHandler(computersalg_test["link"])
computersalg_handler._request_product_data()
computersalg_handler._get_common_data()

elgiganten_handler = ElgigantenHandler(elgiganten_test["link"])
elgiganten_handler._request_product_data()
elgiganten_handler._get_common_data()

avxperten_handler = AvXpertenHandler(avxperten_test["link"])
avxperten_handler._request_product_data()
avxperten_handler._get_common_data()

avcables_handler = AvCablesHandler(avcables_test["link"])
avcables_handler._request_product_data()
avcables_handler._get_common_data()

amazon_handler = AmazonHandler(amazon_test["link"])
amazon_handler._request_product_data()
amazon_handler._get_common_data()

# for url that start with 'ebay.com/itm/'
ebay_handler_with_itm = EbayHandler(ebay_with_itm_test["link"])
ebay_handler_with_itm._request_product_data()
ebay_handler_with_itm._get_common_data()

# for url that start with 'ebay.com/p/'
ebay_handler_with_p = EbayHandler(ebay_with_p_test["link"])
ebay_handler_with_p._request_product_data()
ebay_handler_with_p._get_common_data()

expert_handler = ExpertHandler(expert_test["link"])
expert_handler._request_product_data()
expert_handler._get_common_data()

power_handler = PowerHandler(power_test["link"])
power_handler._request_product_data()
power_handler._get_common_data()

mmvision_handler = MMVisionHandler(mmvision_test["link"])
mmvision_handler._request_product_data()
mmvision_handler._get_common_data()

coolshop_handler = CoolshopHandler(coolshop_test["link"])
coolshop_handler._request_product_data()
coolshop_handler._get_common_data()

sharkgaming_handler = SharkGamingHandler(sharkgaming_test["link"])
sharkgaming_handler._request_product_data()
sharkgaming_handler._get_common_data()

newegg_handler = NeweggHandler(newegg_test["link"])
newegg_handler._request_product_data()
newegg_handler._get_common_data()

hifiklubben_handler = HifiKlubbenHandler(hifiklubben_test["link"])
hifiklubben_handler._request_product_data()
hifiklubben_handler._get_common_data()


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
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=komplett_handler.request_data)
        actual = komplett_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = komplett_handler._get_product_name().lower()
        expected = komplett_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = komplett_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = komplett_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == komplett_test["expected_currency"]

    def test_get_id(self) -> None:
        id = komplett_handler._get_product_id()
        assert isinstance(id, str)
        assert id == komplett_test["expected_id"]


class TestProshopHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=proshop_handler.request_data)
        actual = proshop_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = proshop_handler._get_product_name().lower()
        expected = proshop_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = proshop_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = proshop_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == proshop_test["expected_currency"]

    def test_get_id(self) -> None:
        id = proshop_handler._get_product_id()
        assert isinstance(id, str)
        assert id == proshop_test["expected_id"]


class TestComputersalgHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch(
            "scraper.domains.BaseWebsiteHandler._request_product_data", return_value=computersalg_handler.request_data
        )
        actual = computersalg_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = computersalg_handler._get_product_name().lower()
        expected = computersalg_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = computersalg_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = computersalg_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == computersalg_test["expected_currency"]

    def test_get_id(self) -> None:
        id = computersalg_handler._get_product_id()
        assert isinstance(id, str)
        assert id == computersalg_test["expected_id"]


class TestElgigantenHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=elgiganten_handler.request_data)
        actual = elgiganten_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = elgiganten_handler._get_product_name().lower()
        expected = elgiganten_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = elgiganten_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = elgiganten_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == elgiganten_test["expected_currency"]

    def test_get_id(self) -> None:
        id = elgiganten_handler._get_product_id()
        assert isinstance(id, str)
        assert id == elgiganten_test["expected_id"]


class TestAvXpertenHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=avxperten_handler.request_data)
        actual = avxperten_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = avxperten_handler._get_product_name().lower()
        expected = avxperten_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = avxperten_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = avxperten_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == avxperten_test["expected_currency"]

    def test_get_id(self) -> None:
        id = avxperten_handler._get_product_id()
        assert isinstance(id, str)
        assert id == avxperten_test["expected_id"]


class TestAvCablesHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=avcables_handler.request_data)
        actual = avcables_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = avcables_handler._get_product_name().lower()
        expected = avcables_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = avcables_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = avcables_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == avcables_test["expected_currency"]

    def test_get_id(self) -> None:
        id = avcables_handler._get_product_id()
        assert isinstance(id, str)
        assert id == avcables_test["expected_id"]


class TestAmazonHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=amazon_handler.request_data)
        actual = amazon_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = amazon_handler._get_product_name().lower()
        expected = amazon_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = amazon_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = amazon_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == amazon_test["expected_currency"]

    def test_get_id(self) -> None:
        id = amazon_handler._get_product_id()
        assert isinstance(id, str)
        assert id == amazon_test["expected_id"]


# OBS: There is two Ebay versions - This is for url that start with 'ebay.com/itm/'
class TestEbayHandler_with_itm(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch(
            "scraper.domains.BaseWebsiteHandler._request_product_data", return_value=ebay_handler_with_itm.request_data
        )
        actual = ebay_handler_with_itm.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = ebay_handler_with_itm._get_product_name().lower()
        expected = ebay_with_itm_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = ebay_handler_with_itm._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = ebay_handler_with_itm._get_product_currency()
        assert isinstance(currency, str)
        assert len(currency) == 3
        assert currency == ebay_with_itm_test["expected_currency"]

    def test_get_id(self) -> None:
        id = ebay_handler_with_itm._get_product_id()
        assert isinstance(id, str)
        assert id == ebay_with_itm_test["expected_id"]


# OBS: There is two Ebay versions - This is for url that start with 'ebay.com/p/'
class TestEbayHandler_with_p(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=ebay_handler_with_p.request_data)
        actual = ebay_handler_with_p.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = ebay_handler_with_p._get_product_name().lower()
        expected = ebay_with_p_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = ebay_handler_with_p._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = ebay_handler_with_p._get_product_currency()
        assert isinstance(currency, str)
        assert len(currency) == 3
        # assert currency == ebay_with_p_test["expected_currency"]

    def test_get_id(self) -> None:
        id = ebay_handler_with_p._get_product_id()
        assert isinstance(id, str)
        assert id == ebay_with_p_test["expected_id"]


class TestPowerHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=power_handler.request_data)
        actual = power_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = power_handler._get_product_name().lower()
        expected = power_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = power_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = power_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == power_test["expected_currency"]

    def test_get_id(self) -> None:
        id = power_handler._get_product_id()
        assert isinstance(id, str)
        assert id == power_test["expected_id"]


class TestExpertHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=expert_handler.request_data)
        actual = expert_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = expert_handler._get_product_name().lower()
        expected = expert_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = expert_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = expert_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == expert_test["expected_currency"]

    def test_get_id(self) -> None:
        id = expert_handler._get_product_id()
        assert isinstance(id, str)
        assert id == expert_test["expected_id"]


class TestMMVisionHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=mmvision_handler.request_data)
        actual = mmvision_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = mmvision_handler._get_product_name().lower()
        expected = mmvision_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = mmvision_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = mmvision_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == mmvision_test["expected_currency"]

    def test_get_id(self) -> None:
        id = mmvision_handler._get_product_id()
        assert isinstance(id, str)
        assert id == mmvision_test["expected_id"]


class TestCoolshopHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=coolshop_handler.request_data)
        actual = coolshop_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = coolshop_handler._get_product_name().lower()
        expected = coolshop_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = coolshop_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = coolshop_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == coolshop_test["expected_currency"]

    def test_get_id(self) -> None:
        id = coolshop_handler._get_product_id()
        assert isinstance(id, str)
        assert id == coolshop_test["expected_id"]


class TestSharkGamingHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=sharkgaming_handler.request_data)
        actual = sharkgaming_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = sharkgaming_handler._get_product_name().lower()
        expected = sharkgaming_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = sharkgaming_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = sharkgaming_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == sharkgaming_test["expected_currency"]

    def test_get_id(self) -> None:
        id = sharkgaming_handler._get_product_id()
        assert isinstance(id, str)
        assert id == sharkgaming_test["expected_id"]


class TestNeweggHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=newegg_handler.request_data)
        actual = newegg_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = newegg_handler._get_product_name().lower()
        expected = newegg_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = newegg_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = newegg_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == newegg_test["expected_currency"]

    def test_get_id(self) -> None:
        id = newegg_handler._get_product_id()
        assert isinstance(id, str)
        assert id == newegg_test["expected_id"]


class TestHifiKlubbenHandler(BaseTestWebsiteHandler):
    def test_get_product_info(self, mocker) -> None:
        mocker.patch("scraper.domains.BaseWebsiteHandler._request_product_data", return_value=hifiklubben_handler.request_data)
        actual = hifiklubben_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid

    def test_get_name(self) -> None:
        actual = hifiklubben_handler._get_product_name().lower()
        expected = hifiklubben_test["expected_title"].lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self) -> None:
        price = hifiklubben_handler._get_product_price()
        assert isinstance(price, float)

    def test_get_currency(self) -> None:
        currency = hifiklubben_handler._get_product_currency()
        assert isinstance(currency, str)
        assert currency == hifiklubben_test["expected_currency"]

    def test_get_id(self) -> None:
        id = hifiklubben_handler._get_product_id()
        assert isinstance(id, str)
        assert id == hifiklubben_test["expected_id"]
