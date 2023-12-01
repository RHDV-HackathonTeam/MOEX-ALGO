import logging
from logging import Logger

from settings import setup_logger


class TaLibBaseException(Exception):

    error: Exception | str
    logger: Logger

    def __init__(self, err: Exception | str):
        self.logger = logging.getLogger(__name__)
        setup_logger(logger=self.logger)
        self.error = err
        logging.error(self.error)

    def __str__(self):
        return f"app.TaLib.TABase.Exception: {self.error}"
