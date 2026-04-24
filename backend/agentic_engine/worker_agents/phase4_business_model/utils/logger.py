import os
import logging
from datetime import datetime
from ..config import settings


os.makedirs(settings.LOG_DIR, exist_ok=True)


def get_logger(name: str = "phase4"):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_file = os.path.join(
        settings.LOG_DIR,
        f"{datetime.now().strftime('%Y%m%d')}.log"
    )

    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger