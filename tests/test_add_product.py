import pytest

from scraper.add_product import add_product

test_domains = [
    "https://www.amazon.com/",
    "https://www.ebay.com/",
    "https://www.komplett.dk/",
    "https://www.proshop.dk/",
    "https://www.computersalg.dk/",
    "https://www.elgiganten.dk/",
    "https://www.avxperten.dk/",
    "https://www.av-cables.dk/",
    "https://www.power.dk/",
    "https://www.expert.dk/",
    "https://www.mm-vision.dk/",
    "https://www.coolshop.dk/",
    "https://www.sharkgaming.dk/",
    "https://www.newegg.com/",
]


# Tests to make sure the websites that are supported can be added to be scraped
@pytest.mark.parametrize("url", test_domains)
def test_add_product(url, mocker):
    mocker.patch("scraper.Scraper.scrape_info", return_value=None)
    mocker.patch("scraper.Scraper.save_info", return_value=None)
    mocker.patch("scraper.filemanager.Filemanager.add_product_to_csv", return_value=None)
    mocker.patch("scraper.add_product.check_if_product_exists", return_value=False)
    mocker.patch("scraper.add_product.check_if_product_exists_csv", return_value=False)
    mocker.patch("scraper.add_product.add_product_to_records", return_value=None)

    # expecting no exceptions
    add_product("test", url)
