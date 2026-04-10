import logging
import sys

from logging.handlers import RotatingFileHandler

def setup_logging():

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter(log_format))

    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=5*1024*1024,
        backupCount=2,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )

logger = logging.getLogger("app")