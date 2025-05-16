"""
Web scraping with requests and beautifulsoup4
"""
from typing import Any
import re
import requests
from bs4 import BeautifulSoup as Soup

URL = "https://www.timeanddate.com/weather/nigeria"


def cities_scraper(state: str) -> dict[Any]:
    """
    This function conducts the webscraping task
    using cities name.
    Key weather information are scraped and stored
    in a dictionary.

    Args:
        state (string): base url of the weather website to be scraped.

    Returns:
        dict: Dictionary of scraped weather data for a location.
    """
    res = requests.get(f'{URL}/{state}', timeout=20)
    html = Soup(res.content, 'html.parser')
    now = html.find_all('table', class_='table')

    for (index, value) in enumerate(now):
        print(index)
        row = {'Location': None, 'Current Date': None,
               'Pressure': None, 'Humidity': None, 'Dew Point': None}
        location = value.find('td').getText()
        row['Location'] = location
        date_time = value.find('td', id='wtct').getText()
        row['Current Date'] = date_time
        pressure = value.find(string=re.compile('mbar'))
        row['Pressure'] = pressure
        hum = value.find(string=re.compile('%'))
        row['Humidity'] = hum
        dew = value.find(string=re.compile('°C')).getText()
        dew = dew.replace('\xa0', '')
        row['Dew Point'] = dew
    return row
