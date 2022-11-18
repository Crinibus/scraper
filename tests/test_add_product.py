import pytest
from contextlib import nullcontext as does_not_raise

from scraper.add_product import add_product
from scraper.exceptions import WebsiteNotSupported


test_domains = [
    ("https://www.amazon.com/", does_not_raise()),
    ("https://www.ebay.com/itm/", does_not_raise()),
    ("https://www.ebay.com/p/", does_not_raise()),
    ("https://www.komplett.dk/", does_not_raise()),
    ("https://www.proshop.dk/", does_not_raise()),
    ("https://www.computersalg.dk/", does_not_raise()),
    ("https://www.elgiganten.dk/", does_not_raise()),
    ("https://www.avxperten.dk/", does_not_raise()),
    ("https://www.av-cables.dk/", does_not_raise()),
    ("https://www.power.dk/", does_not_raise()),
    ("https://www.expert.dk/", does_not_raise()),
    ("https://www.mm-vision.dk/", does_not_raise()),
    ("https://www.coolshop.dk/", does_not_raise()),
    ("https://sharkgaming.dk/", does_not_raise()),
    ("https://www.newegg.com/", does_not_raise()),
    ("https://www.hifiklubben.dk/", does_not_raise()),
    ("https://www.notsupported.com/", pytest.raises(WebsiteNotSupported)),
]


# Tests to make sure the websites that are supported can be added to be scraped
@pytest.mark.parametrize("url,expectation", test_domains)
def test_add_product(url, expectation, mocker):
    mocker.patch("scraper.Scraper.scrape_info", return_value=None)
    mocker.patch("scraper.Scraper.save_info", return_value=None)
    mocker.patch("scraper.filemanager.Filemanager.add_product_to_csv", return_value=None)
    mocker.patch("scraper.add_product.check_if_product_exists", return_value=False)
    mocker.patch("scraper.add_product.check_if_product_exists_csv", return_value=False)
    mocker.patch("scraper.add_product.add_product_to_records", return_value=None)
    mocker.patch("scraper.add_product.save_product", return_value=None)

    with expectation:
        add_product("test", url)
