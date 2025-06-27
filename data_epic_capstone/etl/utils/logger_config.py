import os
import logging
from datetime import datetime


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"{timestamp}_scrape.log")


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path,
    filemode='w',
)
logger = logging.getLogger(__name__)
