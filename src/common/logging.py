import logging
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access environment variables
LOG_LEVEL = os.getenv("LOG_LEVEL", default="INFO")
APP = os.getenv("APP", default="LinesOfCodeCounter")


class ContextualLogger(logging.LoggerAdapter):
    """
    Custom logger adapter to automatically handle 'extra' data for logging.
    """

    def process(self, msg, kwargs):
        # kwargs.setdefault("extra", {})
        kwargs["extra"] = {}
        return msg, kwargs


def setup_logging(log_file: str = None):
    """
    Configures application-wide logging with enhanced format and file output support.

    Args:
            log_file (str): Optional path to a log file where logs should be written.
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    log_level = getattr(logging, LOG_LEVEL.upper())
    logging.basicConfig(level=log_level, format=log_format, handlers=[])

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)
    else:
        logging.basicConfig(
            level=log_level, format=log_format, handlers=[logging.StreamHandler()]
        )
