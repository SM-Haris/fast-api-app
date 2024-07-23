import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    # Create a custom logger
    logger = logging.getLogger("fastapi")
    logger.setLevel(logging.INFO)
    
    # Create handlers
    handler = TimedRotatingFileHandler(
        "../logs/fastapi.log", when="midnight", interval=1, backupCount=5
    )
    handler.setLevel(logging.INFO)

    # Create formatters and add them to handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(handler)
