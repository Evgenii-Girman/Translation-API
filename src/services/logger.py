import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger

LOG_DIR = "./logs"

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

class PrintLogger:
    """
    Redirects print statements to the logger.
    """
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        # Avoid logging empty lines
        if message.strip():
            self.logger.info(message.strip())

    def flush(self):
        # Required for compatibility with sys.stdout
        pass


def get_logger(name: str):
    """
    Configures and returns a logger with rotation and a simplified console format.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers
    if logger.hasHandlers():
        return logger

    # File handler with rotation
    log_file = os.path.join(LOG_DIR, f"{name}.log")
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7
    )
    file_handler.setLevel(logging.INFO)

    # File log formatter (JSON for structured logs)
    log_format = "%(asctime)s %(name)s %(levelname)s %(message)s"
    json_formatter = jsonlogger.JsonFormatter(log_format)
    file_handler.setFormatter(json_formatter)

    # Console handler with a simplified format
    console_handler = logging.StreamHandler(sys.stdout)  # Use sys.stdout for print redirection
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "INFO:     %(message)s"  # Matches FastAPI's default format
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Redirect print to this logger
    sys.stdout = PrintLogger(logger)

    return logger

