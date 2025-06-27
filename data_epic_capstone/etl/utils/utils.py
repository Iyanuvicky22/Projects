"""
Utils function for ETL Job.

Name: Arowosegbe Victor Iyanuoluwa
Email: iyanuvicky@gmail.com
Github: https://github.com/Iyanuvicky22/Projects
*** remove created_at()
"""

from pathlib import Path
import os
from datetime import datetime, timezone
import boto3
from dotenv import load_dotenv
from utils.logger_config import logger
from utils.models import connect_db
import pandas as pd

load_dotenv()
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
s3 = boto3.client("s3", region_name=AWS_REGION,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_KEY)
print(AWS_REGION)
bucket_name = 'scraped-ai-agent'

def read_data(source_path: str) -> pd.DataFrame:
    """

    Args:
        source_path (str): Data Path

    Raises:
        ValueError: Raises error for unsupported data type.

    Returns:
        dataframe: Pandas Dataframe.
    """

    try:
        ext = Path(source_path).suffix
        if ext == ".csv":
            return pd.read_csv(source_path)
        elif ext == ".json":
            return pd.read_json(source_path)
        elif ext == ".parquet":
            return pd.read_parquet(source_path)
        logger.info("Data successfully read!")
    except Exception as e:
        logger.error(
            "Error raised at data loading. Unsupported file format! Use csv, json or parquet: %s",
            e,
            exc_info=True,
        )


def remove_hashtags(tags):
    """
    Method to clean category column from "https://aitoolsdirectory.com/"
    Args:
        tags (Series): Column to be cleaned

    Returns:
        Series: Cleaned column.
    """
    try:
        if isinstance(tags, list):
            clean = [tag for tag in tags if "#" not in tag]
        elif isinstance(tags, str):
            clean = [tags] if "#" not in tags else []
        else:
            clean = []
        clean = ",".join(clean)

        if len(clean) < 4:
            clean = clean.upper()
        else:
            clean = clean.lower().capitalize()
        return clean
    except Exception as e:
        logger.error("Error Raised at tags column cleaning:  %s", e, exc_info=True)


def clean_data(df):
    """
    Custom function to clean scraped/manual ai_tools dataset
    Args:
        df (pd.DataFrame): Scraped/manually created ai_tools dataset.

    Returns:
        pd.DataFrame: Cleaned ai_tools dataset.
    """
    try:
        df = df.drop(columns=[col for col in ["pricing", "page"] if col in df.columns])
        new_df = df.dropna()
        new_df = new_df.reset_index(drop=True)

        if "category" in df.columns:
            new_df["category"] = new_df["category"].apply(remove_hashtags)
        else:
            pass

        logger.info(
            "Columns dropped and null values dropped.",
            extra={
                "Cols dropped": ["pricing", "page"],
                "Null Values Dropped": len(df) - len(new_df),
            },
        )
        logger.info("Tags Column Successfully cleaned.")
        logger.info("Data successfully cleaned!")
        return new_df
    except Exception as e:
        logger.error("Error Raised at full cleaning process: %s", e, exc_info=True)


def get_created_at(filepath: str) -> str:
    """
    Extracting file creation date
    Args:
        filepath (str): filepath

    Returns:
        str: creation time in strings
    """
    try:
        created_timestamp = os.path.getctime(filepath)
        created_date = datetime.fromtimestamp(created_timestamp)
        return created_date.strftime("%Y-%M-%d")
    except Exception as e:
        logger.error(f"Error Raised: {e}!", exc_info=True)


def transform_data(df: pd.DataFrame, source=None) -> pd.DataFrame:
    """
    Custom function to transform any scraped and cleaned ai_tools dataset.
    Args:
        df (pd.DataFrame): Clean ai_tools dataset

    Returns:
        pd.DataFrame: Transformed ai_tools dataset
    """
    try:
        # created_day = get_created_at(scraped_data_source)
        if "source" in df.columns:
            if df["source"] is not None:
                pass
            else:
                df["source"] = source
        else:
            df["source"] = source

        if "created_at" in df.columns:
            if df['created_at'] is not None:
                pass
            else:
                df["created_at"] = datetime.now().strftime("%Y-%m-%d")
        else:
            df["created_at"] = datetime.now().strftime("%Y-%m-%d")

        df["updated_at"] = datetime.now().strftime("%Y-%m-%d")

        if "trending" not in df.columns:
            df["trending"] = 0
            # df["trending"] = df["trending"].notna().astype(bool)
        else:
            df["trending"] = df["trending"].apply(
                lambda x: 0 if x == "Low" else 1
            )
        df["trending"] = 0

        trans_df = df.rename(columns={"url": "homepage_url", "tags": "category"})

        trans_df["created_at"] = pd.to_datetime(
            trans_df["created_at"], format="%Y-%m-%d", errors="coerce"
        )
        trans_df["updated_at"] = pd.to_datetime(
            trans_df["updated_at"], format="%Y-%m-%d", errors="coerce"
        )
        trans_df = trans_df.drop_duplicates(subset=['name'], keep='last')

        logger.info("Data successfully transformed!")
        return trans_df
    except Exception as e:
        logger.error("Error Raised at transformation: %s", e, exc_info=True)


def merging_dfs(new_df, existing_df) -> pd.DataFrame:
    """
    Merging DFs to extract unique ai_tools
    Returns:
        pd.DataFrame: Merged DF with unique Ai tools
    """
    try:
        merged_df = pd.merge(new_df, existing_df, how="outer")
        merged_df.drop_duplicates(subset=[
            "name", "homepage_url"
        ], inplace=True)
        merged_df = merged_df.reset_index(drop=True)
        logger.info("Existing DB Data and Scraped Data successfully merged!")
        return merged_df
    except Exception as e:
        logger.error("Error merging DFs: %s", e, exc_info=True)


def fetch_db_records():
    session, engine = connect_db()

    with engine.connect() as conn:
        db_df = pd.read_sql("SELECT * from agents", con=conn)
        db_df = db_df.drop(columns='id')
        conn.commit()
    return db_df


def dump_raw_data_to_s3(file_path: str):
    try:
        s3.upload_file(file_path, bucket_name, f"{os.path.basename(file_path)}")
        logger.info(f"Successfully upload to s3://{bucket_name}/{os.path.basename(file_path)}")
        os.remove(file_path)
        print(f"Successfully upload to s3://{bucket_name}/{os.path.basename(file_path)}")
    except Exception as e:
        logger.error(f"Uploading failed: {e}")
        print(f"Uploading failed: {e}")


def fetch_latest_csv_from_s3(download_dir='downloads'):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        contents = response.get('Contents', [])

        # Filter for CSV files and sort by last modified time
        csv_files = [obj for obj in contents if obj['Key'].endswith('.csv')]
        if not csv_files:
            logger.info("❌ No CSV files found.")
            return None

        latest_file = max(csv_files, key=lambda x: x['LastModified'])
        latest_key = latest_file['Key']
        filename = os.path.basename(latest_key)
        local_path = os.path.join(download_dir, filename)

        os.makedirs(download_dir, exist_ok=True)
        s3.download_file(bucket_name, latest_key, local_path)

        logger.info(f"✅ Downloaded latest CSV: {latest_key} → {local_path}")
        print(f"✅ Downloaded latest CSV: {latest_key} → {local_path}")
        return local_path

    except Exception as e:
        logger.error(f"❌ Failed to fetch from S3: {e}")
        print(f"❌ Failed to fetch from S3: {e}")
        return None
