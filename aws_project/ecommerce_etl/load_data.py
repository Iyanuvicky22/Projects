"""
Data Loading module
"""

import polars as pl

df = pl.read_csv('data/Pakistan Largest Ecommerce Dataset.csv', ignore_errors=True)

print(df.describe())
print(df.columns)

print(df)
