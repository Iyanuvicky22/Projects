import os
import logging
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Load environment variables
load_dotenv(override=True)


def set_configs() -> dict:
    """
    set_configs
    Sets configuration variables from env variables and updates the OS env.
    The following are retrieved from the environment:
        - HOST: The host for the application.
        - PORT: The port for the application.
    These variables are set in the OS environment and returned.
    Returns:
        dict: A dictionary containing the configuration variables.
    """

    config_vars = {
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("PORT"),
    }

    os.environ.update(config_vars)

    return config_vars


config_vars = set_configs()
