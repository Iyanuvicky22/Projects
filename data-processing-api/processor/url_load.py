"""
This script loads the dataset
from the specified url.

Name: Arowosegbe Victor\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""

import logging
from io import BytesIO
from zipfile import ZipFile
import requests

URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"


def extract_from_url(url: str):
    """
    Extracting excel data from URL
    """
    res = requests.get(url, timeout=20)
    if res.status_code == 200:
        with ZipFile(BytesIO(res.content)) as zip_file:
            zip_file.extractall()
            logging.info("Download Successful")
    else:
        logging.error("Failed to download file %s ", res.status_code)
    return res.status_code
