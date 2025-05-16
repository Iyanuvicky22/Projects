"""
Goal: Load cleaned and transformed IMDB data into a
      database named imdb_db

Author: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
Github: https://github.com/Iyanuvicky22
"""

import os
import logging
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.exc import SQLAlchemyError
from logger.logger import etl_logger

logger = etl_logger()
load_dotenv(dotenv_path=".env")

DB_URL = os.getenv("DB_URL")


class Base(DeclarativeBase):
    pass


def connect_db():
    """
    Setting up database connection.
    """
    try:
        engine = create_engine(DB_URL, echo=False)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        # session = Session()
        logging.info("Database successfully connected to.")
        return Session, engine
    except SQLAlchemyError as e:
        logging.error("Connection Error: %s", e)
        return None, None


class Movies(Base):
    """
    Movies Table definition class
    Args:
        Base (Class): Table declarative class
    """

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), unique=True)
    description: Mapped[str]
    release_year: Mapped[str] = mapped_column(String(4))
    movie_type: Mapped[str] = mapped_column(String(40))

    movies_id: Mapped["Details"] = relationship(back_populates="detail")


class Details(Base):
    """
    Details of movies in the database
    Args:
        Base (Class): Table declarative class
    """

    __tablename__ = "details"

    id: Mapped[int] = mapped_column(primary_key=True)
    details_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    director: Mapped[str] = mapped_column(String(100))
    duration: Mapped[float] = mapped_column(DECIMAL(5, 2))
    ratings: Mapped[float] = mapped_column(DECIMAL(2, 1))
    votes: Mapped[int]

    detail: Mapped["Movies"] = relationship(back_populates="movies_id")


class Sales(Base):
    """
    Sales info of movies
    Args:
        Base (Class): Table declarative class
    """

    __tablename__ = "gross_sales"
    id: Mapped[int] = mapped_column(primary_key=True)
    sales: Mapped[float] = mapped_column(DECIMAL(20, 2))


def load_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Loading IMDb Data into the imdb_db

    """
    Session, engine = connect_db()
    try:
        with Session.begin() as session:
            for _, row in data.iterrows():
                movie = session.query(Movies).filter_by(title=row["title"]).first()
                if not movie:
                    movie = Movies(
                        title=row["title"],
                        description=row["description"],
                        release_year=row["release_year"],
                        movie_type=row["type"],
                    )
                    session.add(movie)

                details = Details(
                    details_id=movie.id,
                    director=row["director"],
                    duration=row["runtime"],
                    ratings=row["rating"],
                    votes=row["votes_count"],
                )
                session.add(details)

                sales = Sales(sales=row["total_sales"])
                session.add(sales)
            session.commit()
        logging.info("Transformed data successfully loaded in database schema!")
    except SQLAlchemyError as e:
        logging.error("Exception error %s", e)
