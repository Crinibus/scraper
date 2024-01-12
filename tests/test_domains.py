from dataclasses import dataclass
import pytest

from scraper.domains import get_website_name


@dataclass
class UrlSetting:
    keep_tld: bool = False
    keep_http: bool = False
    keep_www: bool = False
    keep_subdomain: bool = True


test_websites = [
    ("https://www.amazon.com/", UrlSetting(), "amazon"),
    ("https://www.komplett.dk/", UrlSetting(), "komplett"),
    ("https://www.av-cables.dk/", UrlSetting(), "av-cables"),
    ("https://nowww.com/", UrlSetting(), "nowww"),
    ("https://no-ending-slash.com", UrlSetting(), "no-ending-slash"),
    ("https://www.test.testing.com/", UrlSetting(), "test.testing"),
    ("https://www.test.hello.com/hello/world", UrlSetting(), "test.hello"),
    ("https://sub.main.com", UrlSetting(keep_subdomain=False), "main"),
    ("https://www.sub.main.com", UrlSetting(keep_subdomain=False), "main"),
    ("https://main.com", UrlSetting(keep_subdomain=False), "main"),
    ("https://main.com", UrlSetting(keep_http=True, keep_subdomain=False), "https://main"),
    ("https://www.main.com", UrlSetting(keep_http=True, keep_subdomain=False), "https://main"),
    ("https://www.main.com/", UrlSetting(keep_http=True, keep_subdomain=False), "https://main"),
    ("https://www.sub.main.com/", UrlSetting(keep_http=True), "https://sub.main"),
]


@pytest.mark.parametrize("url,setting,expected", test_websites)
def test_get_website_name(url: str, setting: UrlSetting, expected: str) -> None:
    result = get_website_name(
        url,
        keep_tld=setting.keep_tld,
        keep_http=setting.keep_http,
        keep_www=setting.keep_www,
        keep_subdomain=setting.keep_subdomain,
    )
    assert result == expected
