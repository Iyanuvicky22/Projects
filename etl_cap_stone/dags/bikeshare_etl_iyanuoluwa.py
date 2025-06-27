from airflow.decorators import dag, task
import os
from io import BytesIO
from zipfile import ZipFile
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import logging

load_dotenv(dotenv_path=".env")

FILEPATH = os.getenv("DATA_URL")
RAW_DATAPATH = r"C:\Users\APIN PC\OneDrive\Documents\DS\DE_Inter\etl_cap_stone\data\raw\202212-capitalbikeshare-tripdata.csv"
LOCAL_PATH = "../data"
CURRENT_TIME = datetime.now().strftime("%d-%m-%Y")


default_args = {
    "owner": "Iyanuoluwa",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="bikeshare_etl_iyanuoluwa_v03",
    default_args=default_args,
    start_date=datetime(2025, 5, 9),
    schedule="0 10 * * 1",
)
def bikesharing_etl():
    """
    Bike sharing containerized ETL pipeline to identify
    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """

    @task
    def extract_from_url():
        """
        Extract data from URL
        Args:
            url (str): S3 bucket with transport data
        """
        url = FILEPATH
        output_path = "../data/raw"

        try:
            url = FILEPATH
            res = requests.get(url, timeout=20)
            if res.status_code == 200:
                with ZipFile(BytesIO(res.content)) as zip_file:
                    zip_file.extractall(path=output_path)
            return output_path
        except Exception as e:
            print(e) # include separate logging for code errors

    @task
    def transform_df():
        try:
            df = pd.read_csv(RAW_DATAPATH)
            df["started_at"] = pd.to_datetime(df["started_at"], errors="coerce")
            df["ended_at"] = pd.to_datetime(df["ended_at"], errors="coerce")
            df["trip_duration"] = (df["ended_at"] - df["started_at"]).dt.total_seconds()
            df["start_time"] = df["started_at"].dt.hour
            df["week_of_operation"] = df["started_at"].dt.isocalendar().week
            output_path = f"{LOCAL_PATH}/{CURRENT_TIME}_transformed_data.parquet"
            df.to_parquet(output_path)
            return output_path
        except Exception as e:
            print(e) # include separate logging for code errors
            return None
        

    @task
    def stream_logs(filepath: str):
        logger = logging.getLogger("bike_etl_logger")
        logger.setLevel(logging.WARNING)

        if not logger.handlers:
            file_handler = logging.FileHandler("../logs/etl_capstone_bikesharing.log")
            filemode = "w"
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            df = pd.read_parquet(filepath)

        def stream_trips(df_):
            for _, row in df_.iterrows():
                yield row

        for trip in stream_trips(df):
            duration_mins = trip["trip_duration"]
            trip_start_time = trip["start_time"]

            if duration_mins > 45:
                logger.warning(
                    f"Ride above expected threshold detected! Duration: {duration_mins:.2f} minutes, Ride_ID: {trip['ride_id']}"
                )
            if trip["member_casual"] == "casual" and trip_start_time == 0:
                logger.warning(
                    f"Midnight ride by a casual rider detected! Ride_id: {trip['ride_id']}, station: {trip['start_station_name']}, end_station: {trip['end_station_name']}"
                )

    @task
    def clean_and_load_parquet(filepath: str):
        try:
            df = pd.read_parquet(filepath)
            df = (df.dropna().reset_index()).drop(columns=["index"])
            output_partition = (
                f"{LOCAL_PATH}/{CURRENT_TIME}_clean_parquet_partitions.parquet"
            )
            output_clean = f"{LOCAL_PATH}/{CURRENT_TIME}_clean_data.parquet"
            df.to_parquet(output_partition, partition_cols="week_of_operation")
            df.to_parquet(output_clean)
            return output_clean
        except Exception as e:
            print(e) # include separate logging for code errors
            return None


    @task
    def visualize_heatmap(filepath: str):
        try:
            df = pd.read_parquet(filepath)

            fig = px.density_map(
                df,
                lat="start_lat",
                lon="start_lng",
                radius=5,
                center={"lat": df["start_lat"].mean(), "lon": df["start_lng"].mean()},
                zoom=11,
                map_style="carto-positron",
                title="Bikeshare Start Location Heatmap",
            )
            output_loc = "../pictures"
            fig.write_html(os.path.join(output_loc, "heatmap.html"))
        except Exception as e:
            print(e) # include separate logging for code errors

    file = extract_from_url()
    transform_file = transform_df()
    stream_and_log = stream_logs(transform_file)
    clean_and_load = clean_and_load_parquet(transform_file)
    vis_heatmap = visualize_heatmap(clean_and_load)

    transform_file >> stream_and_log
    transform_file >> clean_and_load
    clean_and_load >> vis_heatmap


bikesharing_etl_dag = bikesharing_etl()
