from dataclasses import dataclass, field
import re


@dataclass
class Info:
    """Scraped info about product"""

    name: str
    price: float
    currency: str
    id: str
    valid: bool = True


@dataclass
class Datapoint:
    date: str
    price: float


@dataclass
class Product:
    product_name: str
    category: str
    url: str
    id: str
    currency: str
    website: str
    datapoints: list[Datapoint]
    is_up_to_date: bool

    def get_all_dates(self) -> list[str]:
        return [datapoint.date for datapoint in self.datapoints]

    def get_all_prices(self) -> list[float]:
        return [datapoint.price for datapoint in self.datapoints]

    def to_string_format(self, format: str) -> str:
        """Return a string representing the product, controlled by an explicit format string.

        >>> p = Product("ASUS RTX 4090", "GPU", "https://www.example.com/", "123", "USD", "example", [datepoints], True)
        >>> p.to_string_format("Name: %name, Category: %category, URL: %url, ID: %id, Website: %website")
        'Name: ASUS RTX 4090, Category: GPU, URL: https://www.example.com/, ID: 123, Website: example'
        """
        # inspiration from https://docs.python.org/3/library/re.html#writing-a-tokenizer
        token_specification = [
            ("NAME", r"(%name)"),
            ("CATEGORY", r"(%category)"),
            ("URL", r"(%url)"),
            ("ID", r"(%id)"),
            ("CURRENCY", r"(%currency)"),
            ("WEBSITE", r"(%website)"),
        ]
        format_to = {
            "NAME": self.product_name,
            "CATEGORY": self.category,
            "URL": self.url,
            "ID": self.id,
            "CURRENCY": self.currency,
            "WEBSITE": self.website,
        }

        tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
        new_string = format

        for mo in re.finditer(tok_regex, format):
            kind = mo.lastgroup
            value = mo.group()

            new_string = new_string.replace(value, format_to[kind], 1)

        return new_string


@dataclass
class MasterProduct:
    product_name: str
    category: str
    products: list[Product] = field(default_factory=list)
