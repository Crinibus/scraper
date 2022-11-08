from typing import Dict, List
import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy

from scraper.scrape import Scraper
from scraper.filemanager import Filemanager
from scraper.domains import get_website_name


def add_dataframe_column(df: pd.DataFrame, column_name: str, column_data: List[any]) -> pd.DataFrame:
    df[column_name] = column_data
    return df


def group_df(df: pd.DataFrame, column_name: str, group_keys: bool) -> DataFrameGroupBy:
    grouped_df = df.groupby(column_name, group_keys=group_keys)
    return grouped_df


def get_products_df_grouped_by_domains() -> DataFrameGroupBy:
    product_df = Filemanager.get_products_data()
    domain_names = [get_website_name(url) for url in product_df["url"]]
    df = add_dataframe_column(product_df, "domain", domain_names)
    grouped_df = group_df(df, "domain", True)
    return grouped_df


def get_products_grouped_by_domain(grouped_products_df: DataFrameGroupBy) -> Dict[str, List[Scraper]]:
    domains_dict: Dict[str, List[Scraper]] = {}

    for domain_name in grouped_products_df.groups:
        group_products = grouped_products_df.get_group(domain_name)
        domains_dict[domain_name] = [Scraper(category, url) for category, url in zip(group_products["category"], group_products["url"])]
    return domains_dict
