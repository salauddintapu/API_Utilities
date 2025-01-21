import os
import datetime
import logging
import logging.config
from typing import Literal

now = datetime.datetime.now()
now = now.strftime('%H_%M_%S_%d_%m_%Y')

#configuration
logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "custom_formatter",
            "level": "INFO",
            "filename": f"log/{now}_response.log",
            "mode": "a"
        }
    },
    "loggers": {
        "api_logger": {
            "handlers": ["file_handler"],
            "level": "INFO",
            "propagate": False
        }
    }
}

class LOG:
    def __init__(self):
        os.makedirs('log', exist_ok=True)
        logging.config.dictConfig(logger_config)
        self.logger = logging.getLogger("api_logger")
    
    def log_msg(self, api_area: str, msg: str, msg_level: Literal['info', 'error', 'warning']):
        msg_body = {'origin_section':api_area, 'response':msg}

        if msg_level=='info':
            self.logger.info(str(msg_body))
        elif msg_level=='error':
            self.logger.error(str(msg_body))
        elif msg_level=='warning':
            self.logger.warning(str(msg_body))