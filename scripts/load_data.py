import pdal

from logger import Logger


class LoadData:
    def __init__(self) -> None:
        self.logger = Logger("load_data").get_app_logger()
