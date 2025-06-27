"""
Idempotent ETL Job Script.

Name: Arowosegbe Victor Iyanuoluwa
Email: iyanuvicky@gmail.com
Github: https://github.com/Iyanuvicky22/Projects
"""
from pathlib import Path
from utils.utils import read_data, clean_data, transform_data
from utils.models import upsert_agents
import pandas as pd
from utils.utils import fetch_latest_csv_from_s3, fetch_db_records, merging_dfs
from utils.logger_config import logger
from utils.models import DB_URL


def run_basic_etl() -> pd.DataFrame:
    """
    Basic ETL Job.
    Returns:
        pd.DataFrame: Ai tools data to run etl job on.
    """
    # download latest file from s3
    scraped_data_source = fetch_latest_csv_from_s3()

    scraped_df = read_data(scraped_data_source)

    clean_scraped_df = clean_data(scraped_df)

    trans_scraped_df = transform_data(clean_scraped_df)

    existing_db_df = fetch_db_records()

    final_df = merging_dfs(trans_scraped_df, existing_db_df)
    final_df = final_df.drop_duplicates(subset=['name'], keep='last')

    upsert_agents(final_df)
    logger.info(f"📦 ETL complete: {len(final_df)} total tools after merge.")

    return final_df


if __name__ == "__main__":
    run_basic_etl()
