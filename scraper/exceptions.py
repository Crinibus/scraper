from scraper.constants import URL_SCHEMES


class WebsiteNotSupported(Exception):
    def __init__(self, website_name: str, *args: object) -> None:
        super().__init__(*args)
        self.website_name = website_name

    def __str__(self) -> str:
        return f"Website '{self.website_name}' is currently not supported"


class URLMissingSchema(Exception):
    def __init__(self, url, *args: object) -> None:
        super().__init__(*args)
        self.url = url

    def __str__(self) -> str:
        return f"Missing schema in url '{self.url}'. Consider prefixing the url with one of following schemes: {', '.join(URL_SCHEMES)}"
