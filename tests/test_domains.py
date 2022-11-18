import pytest

from scraper.domains import get_website_name

test_websites = [
    ("https://www.amazon.com/", "amazon"),
    ("https://www.komplett.dk/", "komplett"),
    ("https://www.av-cables.dk/", "av-cables"),
    ("https://nowww.com/", "nowww"),
    ("https://no-ending-slash.com", "no-ending-slash"),
    ("https://www.test.testing.com/", "test.testing"),
    ("https://www.test.hello.com/hello/world", "test.hello"),
]


@pytest.mark.parametrize("url,expected", test_websites)
def test_get_website_name(url, expected) -> None:
    result = get_website_name(url)
    assert result == expected
