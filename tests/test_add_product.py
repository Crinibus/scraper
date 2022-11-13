import pytest
from contextlib import nullcontext as does_not_raise

from scraper.filemanager import Filemanager
from scraper.add_product import add_product
from scraper.exceptions import WebsiteNotSupported

test_objects_json = Filemanager.read_json("./tests/test_objects.json")
test_json = test_objects_json["test_website_handlers"]

test_domains = [
    (test_json["amazon"]["link"], does_not_raise()),
    (test_json["ebay_with_itm"]["link"], does_not_raise()),
    (test_json["ebay_with_p"]["link"], does_not_raise()),
    (test_json["komplett"]["link"], does_not_raise()),
    (test_json["proshop"]["link"], does_not_raise()),
    (test_json["computersalg"]["link"], does_not_raise()),
    (test_json["elgiganten"]["link"], does_not_raise()),
    (test_json["avxperten"]["link"], does_not_raise()),
    (test_json["av-cables"]["link"], does_not_raise()),
    (test_json["power"]["link"], does_not_raise()),
    (test_json["expert"]["link"], does_not_raise()),
    (test_json["mm-vision"]["link"], does_not_raise()),
    (test_json["coolshop"]["link"], does_not_raise()),
    (test_json["sharkgaming"]["link"], does_not_raise()),
    (test_json["newegg"]["link"], does_not_raise()),
    (test_json["hifiklubben"]["link"], does_not_raise()),
    ("https://www.notsupported.com/", pytest.raises(WebsiteNotSupported)),
]


# Tests to make sure the websites that are supported can be added to be scraped
@pytest.mark.parametrize("url,expectation", test_domains)
def test_add_product(url, expectation, mocker) -> None:
    mocker.patch("scraper.Scraper.scrape_info", return_value=None)
    mocker.patch("scraper.Scraper.save_info", return_value=None)
    mocker.patch("scraper.filemanager.Filemanager.add_product_to_csv", return_value=None)
    mocker.patch("scraper.add_product.check_if_product_exists", return_value=False)
    mocker.patch("scraper.add_product.check_if_product_exists_csv", return_value=False)
    mocker.patch("scraper.add_product.add_product_to_records", return_value=None)

    with expectation:
        add_product("test", url)
