import logging

logging.basicConfig(level=logging.INFO)
root_logger = logging.getLogger()


def get_logger(module_name: str) -> logging.Logger:
    child_logger = root_logger.getChild(module_name)
    return child_logger
