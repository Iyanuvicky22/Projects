"""
Testing the Web Scraping Module
"""
import sys
sys.path.append("../")

from etl_pipe.web_scraper import *


def test_access_api():
    """
    Testing Access to IMDB APIs
    """
    for url in URLS:
        access_1 = imdb_scraper(url=url)
        assert access_1 is not None

    access_2 = top_1000_movies(url=URL_1000, page=1)
    assert access_2 is not None


def test_get_scrapers():
    """
    Testing Web Scraper access to IMDB API
    """
    scraper_1 = get_1000_movies(pages=10)
    scraper_2 = get_imdb_movies(urls=URLS)
    assert scraper_1 is not None
    assert scraper_2 is not None


def test_access_api_types():
    """
    Testing request response type.
    """
    for url in URLS:
        access_1 = imdb_scraper(url=url)
        assert isinstance(access_1, list)
    access_2 = top_1000_movies(url=URL_1000, page=1)
    assert isinstance(access_2, list)


def test_scraper_types():
    """
    Testing scrapers datatypes
    """
    scraper_1 = get_1000_movies(pages=10)
    scraper_2 = get_imdb_movies(urls=URLS)
    assert isinstance(scraper_1, pd.DataFrame)
    assert isinstance(scraper_2, pd.DataFrame)
