# **Weather Scraper API**

## **Overview**
The **Weather Scraper API** is a FastAPI-based web service that scrapes weather data from [Time and Date](https://www.timeanddate.com/weather/nigeria/), extracts relevant weather details for three selected Nigerian states, cleans the data (using regex if needed), and writes it to a Google Sheet. The API is designed for real-time weather monitoring and can be tested via FastAPI's interactive documentation (/docs).


## **Features**
- **FastAPI Endpoint**: Provides a GET endpoint to fetch weather data, process it, and update Google Sheets.
- **Web Scraping**: Extracts weather information from Time and Date’s website.
- **Data Cleaning**: Uses regex and other techniques to clean scraped data.
- **Google Sheets Integration**: Uses `gspread` to authenticate and update a Google Sheet.
- **Dependency Management**: Uses Poetry for package management.
- **Virtual Environment**: Uses `venv` for environment isolation.
- **API Documentation**: Provides an interactive Swagger UI at `/docs`.


## **Project Structure**
```
weather_api/
    ├── .gitignore
    ├── .env.example
    ├── README.md
    ├── main.py
    ├── pyproject.toml
    ├── poetry.lock
    ├── scraper/
    │   ├── __init__.py
    │   ├── scraper.py
    │   └── google_sheet.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_scraper.py
```
## **Installation & Setup**
### **1. Connect to the Repository**
```cmd
git remote add https://github.com/Data-Epic/weather_api.git

```
### **2. Install Poetry**
```cmd
pipx install poetry
```
### **3. Install Dependencies**
```cmd
poetry install
```
### **4. Activate Virtual Environment**
```cmd
poetry update
```

### **5. Run the API**
```cmd
fastapi dev main.py
```
## **Usage**
### **FastAPI Swagger UI**
Once the API is running, visit:
```
http://127.0.0.1:8000/docs
```
This provides an interactive interface to test the API endpoints.

## **Author**
**AROWOSEGBE VICTOR IYANUOLUWA**
