import logging


def get_logger():
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())
    return logger
