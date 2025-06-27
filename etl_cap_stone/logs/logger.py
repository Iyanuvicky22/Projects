import logging


def cap_stone_logger():

    logging.basicConfig(
        filename='../logs/etl_capstone_bikesharing.log',
        filemode='a',
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M",
    )

    return logging.getLogger(__name__)
