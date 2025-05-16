#  Arowosegbe Victor Iyanuoluwa ETL Pipeline

## Overview
This is a data engineering task. It is basically an ETL project using IMDb APIs from Rapid API {[text](https://rapidapi.com/)} for extracting data, transforming with pandas and Loading to a database with SQLAlchemy.
Movies data was extracted from two IMDb APIs. 
1) [text](https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236/playground/apiendpoint_a5de12e2-d269-44fb-8af7-6eb02982ee9e)
2) [text](https://rapidapi.com/robotfa-robotfa-default/api/imdb-top-1000-movies-series/playground/apiendpoint_b9c2303e-934a-4b85-a8aa-3fed7cb08fe5)


## Features
- Extract: Fetch movie data from the IMDB APIs on Rapid API website using `Requests` library
- Transform: Clean and transform the extracted data using `Pandas` for efficient processing. Polars will follow after.
- Database integration with `SQLAlchemy` and `psycopg2`
- Configuration management using `.env` files
- Unit testing with `pytest`
   ```

## ETL Process Map
![alt text](pictures/etl-pipeline.jpg)

## Database Table Schema
This is my table schema
![alt text](<pictures/ETL project (1).jpg>)

## Project Structure
```
/etl_pipeline
│── .env                # Environment variables
│── .gitignore          # Git ignore file
│── pyproject.toml      # Project dependencies and metadata
│── poetry.lock         # Dependency lock file
│── README.md           # Project documentation
├── run_pipeline.py      # run etl pipeline logic
│── src/
│   ├── __init__.py     # Package initialization
│   ├── web_scraper.py      # Extraction logic
│   ├── data_transform.py    # Data transformation logic
│   ├── db_loader.py         # Load processed data into a database
│── tests/
│   ├── __init__.py     # Package initialization
│   ├── test_web_scraper.py # Unit tests for extraction
│   ├── test_data_transform.py # Unit tests for transformation
│   ├── test_db_loader.py    # Unit tests for loading
│── data/
│   ├── First_df.csv         # Data scraped from IMDb 1000 popular movies [text](https://rapidapi.com/robotfa-robotfa-default/api/imdb-top-1000-movies-series)
│   ├── Second_df.csv    # Data scraped from IMDb API [text](https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236)
│   ├── Joined_data         # Joined data from the two sources.
│   ├── processed_data.parquet      # Processed Data saved in parquet format.    
```
## Result


## Installation
### Prerequisites
- Python 3.13+
- Poetry package manager

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Iyanuvicky22/victor-etl-pipeline.git
   cd etl_pipeline
   ```
2. Install dependencies:
   ```sh
   poetry install
   ```

## Usage
Run the ETL pipeline with:
```sh
python run_pipeline.py
```

To run tests:
```sh
pytest
```

## Dependencies
- `pandas` (>=1.25.2,<2.0.0)
- `requests` (>=2.32.3,<3.0.0)
- `sqlalchemy` (>=2.0.39,<3.0.0)
- `psycopg2` (>=2.9.10,<3.0.0)
- `pyarrow` (>=19.0.1,<20.0.0)"
- `fastparquet` (>=2024.11.0,<2025.0.0)"

[tool.poetry.group.dev.dependencies]
- `black` = "^25.1.0"
- `dotenv` = "^0.9.9"

[tool.poetry.group.testing.dependencies]
- `pytest` = "^8.3.5"


## Author
**Arowosegbe Victor Iyanuoluwa**
