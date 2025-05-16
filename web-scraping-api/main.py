"""
FAST API Functions
"""
from fastapi import FastAPI
from scraper.scraper import cities_scraper
from scraper.google_sheet import export_to_sheets

app = FastAPI()
SHEETNAME = "FastApi Weather Scraping"


@app.get("/")
def home(wel_text: str):
    """
    Home Function to review the app functionality
    and welcome the user to the apu

    Returns:
        _type_: _description_
    """
    wel_text = 'You are welcome to State Weather Information API.'
    return {'Open Message: ': wel_text}


@app.get("/weather/{state}")
def fetch_weather(state: str):
    """
    This function scrapes the weather data and
    pushes it to the google sheet.

    Args:
        state (str): States to be scraped.

    Returns:
        weather_data: Scraped weather data info.
    """
    weather_data = cities_scraper(state)

    export_to_sheets(sheetname=SHEETNAME, data=weather_data)
    return weather_data
