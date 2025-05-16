"""
Goal: Data transformation for scraped movies and shows
      from IMDb APIs

Author: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
Github: https://github.com/Iyanuvicky22
"""

from sys import exception
import logging
import pandas as pd
import pandas.errors as pd_err
from etl_pipe.web_scraper import *
from logger.logger import etl_logger

logger = etl_logger()


# Calling the Scraping Functions to get the datasets.
df_1 = get_1000_movies(pages=10)
df_2 = get_imdb_movies(urls=URLS)


def clean_df_1(data: pd.DataFrame) -> pd.DataFrame:
    """
    Data cleaning of scraped data from API_HOST_IMDB_1
    -> df_1 = get_1000_movies(pages=10)

    Returns:
        pd.DataFrame: Cleaned Dataframe
    """
    drop_cols = [
        "rank",
        "Poster_Link",
        "Certificate",
        "Star1",
        "Star2",
        "Star3",
        "Star4",
        "Meta_score",
    ]
    df_1_cols_dropped = data.drop(drop_cols, axis=1)
    df_1_new = df_1_cols_dropped.rename(
        {
            "Series_Title": "title",
            "Overview": "description",
            "IMDB_Rating": "rating",
            "No_of_Votes": "votes_count",
            "Released_Year": "release_year",
            "Gross": "total_sales",
            "Runtime": "runtime",
            "Genre": "genres",
            "Director": "director",
        },
        axis=1,
    )
    df_1_new["type"] = "movie"

    return df_1_new


def clean_df_2(data: pd.DataFrame) -> pd.DataFrame:
    """
    Data Cleaning of scraped data from API_HOST_IMDB_2
    df_2 = get_imdb_movies(urls=URLS)

    Returns:
        pd.DataFrame: Cleaned Dataframe
    """
    cols_drop = [
        "url",
        "primaryTitle",
        "primaryImage",
        "contentRating",
        "releaseDate",
        "lifetimeGrossAmount",
        "endYear",
        "interests",
        "countriesOfOrigin",
        "externalLinks",
        "spokenLanguages",
        "filmingLocations",
        "productionCompanies",
        "weekendGrossAmount",
        "weekendGrossCurrency",
        "lifetimeGrossCurrency",
        "weeksRunning",
        "id",
        "isAdult",
    ]
    df_2_cols_dropped = data.drop(cols_drop, axis=1)
    df_2_new = df_2_cols_dropped.rename(
        {
            "originalTitle": "title",
            "averageRating": "rating",
            "numVotes": "votes_count",
            "grossWorldwide": "total_sales",
            "runtimeMinutes": "runtime",
            "startYear": "release_year",
        },
        axis=1,
    )
    df_2_new["genres"] = df_2_new["genres"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else str(x)
    )
    df_2_dup_dropped = df_2_new.drop_duplicates().reset_index().drop("index", axis=1)
    df_2_dup_dropped["director"] = None

    return df_2_dup_dropped


def join_dfs(df_1000: pd.DataFrame, df_imdb: pd.DataFrame) -> pd.DataFrame:
    """
    Joining the two cleaned data for further transformation

    Returns:
        pd.DataFrame: Joined dataframe
    """
    data_1 = clean_df_1(data=df_1000)
    data_2 = clean_df_2(data=df_imdb)

    frames = [data_1, data_2]
    new_df = pd.concat(frames, ignore_index=True)

    return new_df


def transform_df(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform joined dataframe
    Returns:
        pd.DataFrame: Transformed Dataframe
    """
    try:
        joined_df = data
        joined_df = joined_df.dropna(
            subset=["votes_count", "rating", "description", "release_year"]
        )
        joined_df["runtime"] = joined_df["runtime"].astype(str).str.extract(r"(\d+)")
        joined_df["runtime"] = pd.to_numeric(joined_df["runtime"], errors="coerce")
        joined_df["total_sales"] = (
            joined_df["total_sales"].astype(str).replace(r"\,", "", regex=True)
        )
        joined_df["total_sales"] = pd.to_numeric(joined_df["total_sales"], errors="coerce")
        joined_df.loc[joined_df["release_year"] == "PG", "release_year"] = "1995"
        joined_df["release_year"] = joined_df["release_year"].astype(int).astype(str)

        joined_df["rating"] = joined_df["rating"].astype(float)
        joined_df["votes_count"] = joined_df["votes_count"].astype(float)
        cols_to_drop = ["budget, metascore"]
        for col in cols_to_drop:
            if col in joined_df.columns.to_list():
                joined_df = joined_df.drop(columns=col)

        joined_df.to_parquet("data/processed_data.parquet")
        logging.info("Data successfully transformed")
        return joined_df
    except pd_err as e:
        logging.error("Datatype Error %s", e)
    except exception as e:
        logging.error('Exception Raised %s', e)
