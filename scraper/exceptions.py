from typing import Callable
import logging
from scraper.constants import URL_SCHEMES


def log_exception(func: Callable):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logging.getLogger(func.__name__).exception(f"Function '{func.__name__}' raised an exception")
            raise ex

    return inner


class WebsiteNotSupported(Exception):
    def __init__(self, website_name: str, *args: object) -> None:
        super().__init__(*args)
        self.website_name = website_name

    def __str__(self) -> str:
        return f"Website '{self.website_name}' is currently not supported"


class WebsiteVersionNotSupported(Exception):
    def __init__(self, website_name: str, *args: object) -> None:
        super().__init__(*args)
        self.website_name = website_name

    def __str__(self) -> str:
        return f"Website version '{self.website_name}' is currently not supported"


class URLMissingSchema(Exception):
    def __init__(self, url, *args: object) -> None:
        super().__init__(*args)
        self.url = url

    def __str__(self) -> str:
        return f"Missing schema in url '{self.url}'. Consider prefixing the url with one of following schemes: {', '.join(URL_SCHEMES)}"
