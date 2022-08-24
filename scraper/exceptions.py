class WebsiteNotSupported(Exception):
    def __init__(self, website_name: str, *args: object) -> None:
        super().__init__(*args)
        self.website_name = website_name

    def __str__(self) -> str:
        return f"Website '{self.website_name}' is currently not supported"
