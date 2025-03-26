"""
FastAPI Application Module

Name: Arowosegbe Victor\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""
import json
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from processor import load_data as ld
from processor import clean as cl
from processor import aggregate as ag

app = FastAPI()

RAW_PANDAS_DF = None
RAW_POLARS_DF = None


@app.get("/home")
def home():
    """
    Home Function
    """
    return """Welcome to: Data processing packages comparison (pandas vs polars) API project"""


def data_loading():
    """
    API call to load datasets.
    """
    global RAW_PANDAS_DF, RAW_POLARS_DF
    if RAW_PANDAS_DF is None:
        pd_df = ld.read_pandas()
        RAW_PANDAS_DF = pd_df
    if RAW_POLARS_DF is None:
        pl_df = ld.read_polars()
        RAW_POLARS_DF = pl_df


@app.get("/Data Processing")
async def processing():
    """
    API call to process the data sets.
    """

    try:
        data_loading()
        pd_na_free = cl.pd_na_handler(RAW_PANDAS_DF)
        cl.viz_data(pd_na_free)
        pd_df_clean = cl.handle_outlier_pandas(pd_na_free, col="Quantity",
                                               method="cap")
        pd_df_clean = cl.handle_outlier_pandas(
            pd_na_free, col="Price", method="cap"
        )
        pd_df_trans = cl.transform_df(pd_df_clean)
        cl.viz_data(pd_df_trans)
        clean_pandas_df = pd_df_trans

        pandas_aggregate = ag.aggregate_pandas(clean_pandas_df)

        json_pandas = pandas_aggregate.to_json()

        # Polars
        pl_na_free = cl.pl_na_handler(RAW_POLARS_DF)
        cl.viz_data(pl_na_free)
        pl_df_clean = cl.handle_outlier_polars(
            pl_na_free, col="Quantity", method="drop"
        )
        pl_df_clean = cl.handle_outlier_polars(
            pl_na_free, col="Price", method="drop"
        )
        pl_df_trans = cl.transform_df(pl_df_clean)
        cl.viz_data(pl_df_trans)
        clean_polars_df = pl_df_trans

        polars_aggregate = ag.aggregate_polars(clean_polars_df)

        json_polars = polars_aggregate.write_json()

        return {
            "message": "Data Processing Results",
            "success": True,
            "data": {
                "pandas": json.loads(json_pandas),
                "polars": json.loads(json_polars),
            },
        }
    except Exception as e:
        print(f"Error Returned: {e}")
        return {
            "message": "Data Processing Results",
            "success": False,
            "next step": f"Resolve error {e}",
        }


@app.get("/Time Comparison")
async def time_compare():
    """
    This function show the time comparison
    between pandas and polars.
    """
    data_loading()

    # Loading time comparison
    time_comp = ld.compare_time(ld.read_pandas, ld.read_polars)
    
    return {
        "message": "Time Comparison Results",
        "status": "Success",
        "data": time_comp
    }


@app.get("/download-json")
def download_json():
    """
    Download the processed data as a JSON file
    """
    try:
        data_loading()
        pl_na_free = cl.pl_na_handler(RAW_POLARS_DF)
        pl_df_clean = cl.handle_outlier_polars(
            pl_na_free, col="Quantity", method="drop"
        )
        pl_df_clean = cl.handle_outlier_polars(
            pl_na_free, col="Price", method="drop"
        )
        pl_df_trans = cl.transform_df(pl_df_clean)
        clean_polars_df = pl_df_trans
        file_path = "polars_data.json"
        clean_polars_df.write_json(file_path)

        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
    except Exception as e:
        return f"Error while downloading file: {e}"

    return FileResponse(
        file_path, media_type="application/json", filename="polars_data.json"
    )


@app.get("/download-parquet")
def download_parquet():
    """
    Download the processed data as a Parquet file
    """
    try:
        data_loading()
        pd_na_free = cl.pd_na_handler(RAW_PANDAS_DF)
        pd_df_clean = cl.handle_outlier_pandas(pd_na_free, col="Quantity",
                                               method="cap")
        pd_df_clean = cl.handle_outlier_pandas(
            pd_na_free, col="Price", method="cap"
        )
        pd_df_trans = cl.transform_df(pd_df_clean)
        pd_df_trans["Description"] = pd_df_trans["Description"].astype(str)
        clean_pandas_df = pd_df_trans
        file_path = "pandas_data.parquet"
        clean_pandas_df.to_parquet(file_path, engine="pyarrow",
                                   compression="snappy")

        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
    except Exception as e:
        return f"Error while downloading file: {e}"
    return FileResponse(
        file_path, media_type="application/octet-stream",
        filename="pandas_data.parquet"
    )
