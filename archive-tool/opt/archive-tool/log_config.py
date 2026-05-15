import pathlib
import json
import logging
import logging.config


def setup_logger():
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    config_file = BASE_DIR / "log.json"
    with open(config_file) as file:
        file_content = json.load(file)
    logging.config.dictConfig(file_content)
    logger = logging.getLogger("archive_logger")
    return logger