"""
Goal: IMDb Web Scraper for movies and shows

Author: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
Github: https://github.com/Iyanuvicky22
"""
import sys
sys.path.append("../")

import os
import requests
from dotenv import load_dotenv
import pandas as pd
from logger.logger import etl_logger




logger = etl_logger()

pd.set_option("display.max_columns", None)

load_dotenv(dotenv_path=".env")

# API-KEY
APIKEY = os.getenv("APIKEY")

# URLS API_1
URL_250_MOV = os.getenv("URL_250_MOV")
URL_TOP_10 = os.getenv("URL_TOP_10")
URL_250_SHOW = os.getenv("URL_250_SHOW")
URL_POP_MOV = os.getenv("URL_POP_MOV")
URL_POP_SHOW = os.getenv("URL_POP_SHOW")
URL_IND_1 = os.getenv("URL_IND_1")
URL_IND_2 = os.getenv("URL_IND_2")
URL_IND_3 = os.getenv("URL_IND_3")
URL_IND_4 = os.getenv("URL_IND_4")
URL_IND_5 = os.getenv("URL_IND_5")
URL_IND_6 = os.getenv("URL_IND_6")
URL_IND_7 = os.getenv("URL_IND_7")

# URL API_2
URL_1000 = os.getenv("URL_1000")

URLS = [
    URL_250_MOV,
    URL_TOP_10,
    URL_250_SHOW,
    URL_POP_MOV,
    URL_POP_SHOW,
    URL_IND_1,
    URL_IND_2,
    URL_IND_3,
    URL_IND_4,
    URL_IND_5,
    URL_IND_6,
    URL_IND_7,
]

# API HOST
API_HOST_IMDB_1 = os.getenv("API_HOST_IMDB_1")
API_HOST_IMDB_2 = os.getenv("API_HOST_IMDB_2")


def imdb_scraper(url: str) -> list:
    """
    Getting series of movies and shows.
    Args:
        url (str): website to be scraped.
        api_key (str): IMDb Api key.
    """
    try:
        headers = {"x-rapidapi-key": APIKEY,
                   "x-rapidapi-host": API_HOST_IMDB_1}

        response = requests.get(url, headers=headers, timeout=60)
        res_json = response.json()
        return res_json
    except requests.exceptions.ConnectionError:
        logger.error("Connection Error")
    except requests.exceptions.HTTPError:
        logger.error("HTTPs Error")
    except requests.exceptions.InvalidURL:
        logger.error(
            "URL Error. Check the URL again for correctness."
            "Copy and paste from the API."
        )
    except requests.exceptions.RequestException as e:
        logger.error("Exception Raised: %s", e)


def top_1000_movies(url: str, page: int) -> list:
    """
    Web scraping from the second IMDb API (1000 Movies)
    Args:
        page (int): _description_

    Returns:
        list: _description_
    """
    try:
        url = URL_1000 + str(page)
        headers = {"x-rapidapi-key": APIKEY,
                   "x-rapidapi-host": API_HOST_IMDB_2}

        response = requests.get(url, headers=headers, timeout=40)
        res = response.json()
        page, result = res.values()
        result = result[0:100]
        return result
    except requests.exceptions.ConnectionError:
        logger.error("Connection Error")
    except requests.exceptions.HTTPError:
        logger.error("HTTPs Error")
    except requests.exceptions.InvalidURL:
        logger.error(
            "URL Error. Check the URL again for correctness."
            "Copy and paste from the API."
        )
    except requests.exceptions.RequestException as e:
        logger.error("Exception Raised: %s", e)


def get_1000_movies(pages: int = 10) -> pd.DataFrame:
    """
    Calling and getting the a specific amount
    or all of  1000 movies by pages.
    This API is API_HOST_IMDB_2

    A pages yields 100 movies.
    Args:
        pages (int, optional. Max = 10): _description_. Defaults to 10.

    Returns:
        list: _description_
    """
    movies_1000 = []
    try:
        for item in range(1, pages + 1):
            res = top_1000_movies(url=URL_1000, page=item)
            movies_1000.append(res)
            flat_data = [movie for sublist in movies_1000 for movie in sublist]
            movies_df = pd.DataFrame(flat_data)
        logger.info("Top 1000 movies successfully scraped!")
        return movies_df

    except requests.exceptions.ConnectionError:
        logger.error("Connection Error")
    except requests.exceptions.HTTPError:
        logger.error("HTTPs Error")
    except requests.exceptions.InvalidURL:
        logger.error(
            "URL Error. Check the URL again for correctness."
            "Copy and paste from the API."
        )
    except requests.exceptions.RequestException as e:
        logger.error("Exception Raised: %s", e)


def get_imdb_movies(urls: list) -> pd.DataFrame:
    """
    Function to get all movies request points from the
    first IMDb Movies API. (API_HOST_IMDB_1)

    Args:
        URLS (list): List of IMDb URls to scraped

    Returns:
        pd.DataFrame: Dataframe of scraped data
    """
    df_list = []
    try:
        for url in urls:
            res = imdb_scraper(url=url)
            df_list.append(res)

        flat_data_2 = [movie for sublist in df_list for movie in sublist]
        df_2 = pd.DataFrame(flat_data_2)
        logger.info("Movies & Series successfully scraped [Octupusteam IMDB]")
        return df_2
    except requests.exceptions.ConnectionError:
        logger.error("Connection Error")
    except requests.exceptions.HTTPError:
        logger.error("HTTPs Error")
    except requests.exceptions.InvalidURL:
        logger.error(
            "URL Error. Check the URL again for correctness."
            "Copy and paste from the API."
        )
    except requests.exceptions.RequestException as e:
        logger.error("Exception Raised: %s", e)
