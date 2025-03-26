"""
Testing of Functions

Name: Arowosegbe Victor\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""

from processor.url_load import extract_from_url
from processor.load_data import *
from processor.clean import *

URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"


def test_url_load():
    """
    Testing data extraction from website.
    """
    test_res = extract_from_url(url=URL)
    assert test_res == 200


def test_pd_read_data():
    """
    Testing data loading.
    """
    pd_df = read_pandas()
    assert isinstance(pd_df, pd.DataFrame)


def test_pl_read_data():
    """
    Testing data loading.
    """
    pl_df = read_polars()
    assert isinstance(pl_df, pl.DataFrame)


def test_compare_time():
    """
    Testing time comparison
    """
    res = compare_time(read_pandas, read_polars)
    assert isinstance(res, list)


def test_pd_na_handler():
    """
    Testing Pandas Na Handler
    """
    list_raw = [{"Description": [1, None, 3, 5]}, {"Customer ID": [12, 23, None, 32]}]
    df = pd.DataFrame(list_raw)
    res = pd_na_handler(df=df)
    assert res.columns.isna().sum() == 0


def test_pl_na_handler():
    """
    Testing Polars Na Handler
    """
    list_raw = {
        "Invoice": [1, 3, 3, None],
        "Description": [1, None, 3, 5],
        "Customer ID": [12, 23, None, 32],
    }
    df = pl.DataFrame(list_raw)
    res = pl_na_handler(df=df)
    assert res.null_count().sum_horizontal().item() == 0


def test_pd_outlier_identifier():
    """
    Testing Pandas outlier identifier function.
    """
    list_raw = {
        "Invoice": [1, 3, 3, 125],
        "Description": [1, 4, 3, 5],
        "Customer ID": [12, 23, 1000, 32],
    }
    df = pd.DataFrame(list_raw)
    res = check_outliers_info_pandas(df=df, col="Invoice")
    assert res["Max Outlier Value"] == 125


def test_pl_outlier_identifier():
    """
    Testing Pandas outlier identifier function.
    """
    list_raw = {
        "Invoice": [1, 3, 3, 125],
        "Description": [1, 4, 3, 5],
        "Customer ID": [12, 23, 1000, 32],
    }
    df = pl.DataFrame(list_raw)
    res = check_outliers_info_polars(df=df, col="Customer ID")
    assert res["Max Outlier Value"][:, -1] == 1000
