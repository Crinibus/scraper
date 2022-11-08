from typing import List
import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy

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
