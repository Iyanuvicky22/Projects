"""
Testing the Web scraping module.
"""
import time
import pytest
from scraper.scraper import cities_scraper


@pytest.mark.parametrize("location", ["lagos"])
def test_cities_scrapper(location):
    """
    Test the web scraping function.
    """
    result = cities_scraper(location)

    expected_keys = {
        'Location', 'Current Date',
        'Pressure', 'Humidity', 'Dew Point',
                    }
    assert isinstance(result, dict), "Expected result to be a dictionary"
    assert expected_keys.issubset(result.keys()), \
        f"Missing keys: {expected_keys - result.keys()}"


def test_invalid_location():
    """
    Testing to ensure proper handling of invalid location.
    """
    result = cities_scraper("invalid_location")
    assert result is None or "error" in result, \
        "Function should handle invalid locations"


def test_get_weather_non_empty():
    """
    Testing to ensure the scraper's response is not null.
    """
    result = cities_scraper("lagos")

    for key, value in result.items():
        assert value, f"{key} should not be empty"


def test_response_time():
    """
    Testing Scraping response time
    """
    start_time = time.time()
    cities_scraper('lagos')
    end_time = time.time()
    assert end_time - start_time < 5, "Function is taking too long to respond"
