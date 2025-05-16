"""
Setting up logging for IMDB ETL Pipeline

Author: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
Github: https://github.com/Iyanuvicky22
"""
import logging


def etl_logger():
    """
    ETL Pipeline Logger
    Info to gain
    - Time of log
    - Level of log
    - Log message
    """

    logging.basicConfig(
        filename='imdb_etl_pipeline.log',
        filemode='a',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s -  %(message)s',
        datefmt="%Y-%m-%d %H:%M",
    )

    return logging.getLogger(__name__)
