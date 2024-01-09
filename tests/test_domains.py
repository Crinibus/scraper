from dataclasses import dataclass
import pytest

from scraper.domains import get_website_name


@dataclass
class UrlSetting:
    keep_tld: bool
    keep_http: bool
    keep_www: bool
    keep_subdomain: bool


test_websites = [
    ("https://www.amazon.com/", UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=True), "amazon"),
    ("https://www.komplett.dk/", UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=True), "komplett"),
    (
        "https://www.av-cables.dk/",
        UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=True),
        "av-cables",
    ),
    ("https://nowww.com/", UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=True), "nowww"),
    (
        "https://no-ending-slash.com",
        UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=True),
        "no-ending-slash",
    ),
    (
        "https://www.test.testing.com/",
        UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=True),
        "test.testing",
    ),
    (
        "https://www.test.hello.com/hello/world",
        UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=True),
        "test.hello",
    ),
    ("https://sub.main.com", UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=False), "main"),
    ("https://www.sub.main.com", UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=False), "main"),
    ("https://main.com", UrlSetting(keep_tld=False, keep_http=False, keep_www=False, keep_subdomain=False), "main"),
    ("https://main.com", UrlSetting(keep_tld=False, keep_http=True, keep_www=False, keep_subdomain=False), "https://main"),
    ("https://www.main.com", UrlSetting(keep_tld=False, keep_http=True, keep_www=False, keep_subdomain=False), "https://main"),
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
