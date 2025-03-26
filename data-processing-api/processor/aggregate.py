"""
This function perform aggregation
of the dataset using pandas and polars.

Name: Arowosegbe Victor\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""

import pandas as pd
import polars as pl


def aggregate_pandas(df: pd.DataFrame):
    """
    Aggregation function using pandas

    Args:
        df (pd.DataFrame): _description_
    """
    try:
        return round(
            df.groupby(["NameOfDay"])["Price"].agg(["sum", "mean", "count"]), 2
        )
    except Exception as e:
        print(f"Error while aggregating Polars DataFrame: {e}")
        return df


def aggregate_polars(df: pl.DataFrame):
    """
    Aggregation function using pandas

    Args:
        df (pl.DataFrame): _description_
    """
    try:
        return df.group_by("NameOfDay").agg(
            [
                pl.col("Price").sum().alias("sum"),
                pl.col("Price").mean().alias("mean"),
                pl.col("Price").count().alias("count"),
            ]
        )
    except Exception as e:
        print(f"Error while aggregating Polars DataFrame: {e}")
        return df
