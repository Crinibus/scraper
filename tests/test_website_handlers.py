from scraper.domains import KomplettHandler
from scraper.format import Info


komplett_handler = KomplettHandler("https://www.komplett.dk/product/1168438")
komplett_soup = komplett_handler._request_product_data()
komplett_handler._get_common_data(komplett_soup)


class TestKomplettHandler:
    def test_get_product_info(self):
        actual = komplett_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = komplett_handler._get_product_name(komplett_soup)
        expected = "ASUS GeForce RTX 3090 ROG Strix OC".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = komplett_handler._get_product_price(komplett_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = komplett_handler._get_product_currency(komplett_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = komplett_handler._get_product_id(komplett_soup)
        assert isinstance(id, str)
        assert id == "1168438"
