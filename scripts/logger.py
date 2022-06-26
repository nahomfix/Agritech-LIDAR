import logging
from pathlib import Path


class Logger:
    def __init__(self, filename: str, level=logging.INFO):
        """Initilize logger class with file name to be written and default log level.

        Parameters
        ---
            filename: str
                any string name for the file without its extension
            level: logging.{level}, default=logging.INFO
                logging type. It's optional, defaults to logging.INFO
        """

        # Gets or creates a logger
        logger = logging.getLogger(__name__)

        # set log level
        logger.setLevel(level)

        # define file handler and set formatter
        root_dir = Path().cwd().parent
        logs_dir = root_dir / "logs"

        if not logs_dir.exists():
            logs_dir.mkdir()

        file_handler = logging.FileHandler(root_dir / f"logs/{filename}.log")
        formatter = logging.Formatter(
            "[%(asctime)s] : %(levelname)s : {%(filename)s : %(lineno)d} - %(message)s",
            "%m-%d-%Y %H:%M:%S",
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        self.logger = logger

    def get_app_logger(self) -> logging.Logger:
        """Return the logger object.

        Returns
        ---
            logging.Logger: logger object
        """
        return self.logger
