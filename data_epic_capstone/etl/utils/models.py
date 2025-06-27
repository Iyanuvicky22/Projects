import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from utils.logger_config import logger

load_dotenv()
DB_USER = os.environ.get('DB_USER')# or os.getenv("DB_USER")
DB_PASSWORD = os.environ.get('DB_PASSWORD')# or os.getenv("DB_PASSWORD")
DB_HOST = os.environ.get('DB_HOST') #or os.getenv("DB_HOST")
DB_PORT = os.environ.get('DB_PORT')# or os.getenv("DB_PORT")
DB_NAME = os.environ.get('DB_NAME')# or os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()

expected_schema = {
    'name': str,
    'description': str,
    'homepage_url': str,
    'category': str,
    'source': str,
    'trending': int,
    'created_at': 'datetime64[ns]',
    'updated_at': 'datetime64[ns]'
}


def connect_db():
    """
    Database connector
    """
    try:
        engine = create_engine(DB_URL)
        Session = sessionmaker(bind=engine, autoflush=False)
        Base.metadata.create_all(engine)
        logger.info("Database succesfully connected to.")
        return Session, engine
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")


def enforce_schema(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    for col, dtype in schema.items():
        if col not in df.columns:
            raise ValueError(f"Missing column: '{col}'")
        df[col] = df[col].astype(dtype)
    return df[list(schema.keys())]


def upsert_agents(df: pd.DataFrame):
    df = enforce_schema(df, expected_schema)
    data = [tuple(row) for row in df.to_numpy()]
    columns = list(expected_schema.keys())

    insert_query = f"""
        INSERT INTO agents ({', '.join(columns)})
        VALUES %s
        ON CONFLICT (name)
        DO UPDATE SET
            description = EXCLUDED.description,
            homepage_url = EXCLUDED.homepage_url,
            category = EXCLUDED.category,
            source = EXCLUDED.source,
            trending = EXCLUDED.trending,
            updated_at = NOW();
    """

    conn_info = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'port': DB_PORT
    }

    try:
        with psycopg2.connect(**conn_info) as conn:
            with conn.cursor() as cursor:
                execute_values(cursor, insert_query, data)
            conn.commit()
        logger.info("Upsert completed successfully.")
    except Exception as e:
        logger.error('Data upsert failed! %s', e, exc_info=True)
        raise RuntimeError(f"Upsert failed: {e}")
