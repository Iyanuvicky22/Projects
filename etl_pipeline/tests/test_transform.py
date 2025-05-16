"""
Testing the transformation module
"""
import sys
from etl_pipe.data_transform import *

sys.path.append("../")

def test_dataframes():
    """
    Testing Dataframes calls from web_scraper
    """
    assert isinstance(df_1, pd.DataFrame)
    assert isinstance(df_2, pd.DataFrame)


def test_cleaning_return():
    """
    Testing to check cleaning function
    return call.
    """
    data_1 = clean_df_1(df_1)
    data_2 = clean_df_2(df_2)
    assert isinstance(data_1, pd.DataFrame)
    assert isinstance(data_2, pd.DataFrame)


def test_cleaning_new_columns():
    """
    Testing specific cleaning calls.
    New column creation and
    """
    data_1 = clean_df_1(df_1)
    data_2 = clean_df_2(df_2)
    assert data_1['type'].isna().sum() == 0
    assert data_1['type'].nunique() == 1
    assert data_2['director'].isna().sum() == len(data_2['director'])
