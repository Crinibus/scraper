import scraper.database as db
from scraper.scrape import Scraper


class Format:
    def db_products_to_scrapers(products: list[db.Product]) -> list[Scraper]:
        scrapers = []
        for product in products:
            scraper = Format.db_product_to_scraper(product)
            scrapers.append(scraper)
        return scrapers

    @staticmethod
    def db_product_to_scraper(product: db.Product) -> Scraper:
        return Scraper(category=product.category, url=product.short_url)

    @staticmethod
    def scraper_to_db_product(product: Scraper, isActive: bool) -> db.Product:
        return db.Product(
            product_code=product.product_info.id,
            name=product.product_info.name,
            category=product.category,
            domain=product.website_handler.website_name,
            url=product.url,
            short_url=product.website_handler.get_short_url(),
            isActive=isActive,
        )
