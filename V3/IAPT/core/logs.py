from IAPT.core.config import load_config, LOGS_DIR
from datetime import datetime
import logging

SUCCESS = 45
ERROR_DETAIL = 35
logging.addLevelName(SUCCESS, "SUCCESS")
logging.addLevelName(ERROR_DETAIL, "ERROR_DETAIL")


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)


def error_detail(self, message, *args, **kwargs):
    if self.isEnabledFor(ERROR_DETAIL):
        self._log(ERROR_DETAIL, message, args, **kwargs)


logging.Logger.success = success
logging.Logger.error_detail = error_detail
logger = logging.getLogger(__name__)


class LogFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)

        standard_fields = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__)
        standard_fields.update({"message", "asctime"})

        extras = []

        for key, value in record.__dict__.items():
            if key not in standard_fields:
                display_name = key.replace("_", " ").title()
                extras.append((display_name, value))

        if extras:
            for key, value in extras:
                message += f"\n    - {key}: {value}"

        return message


def initialise_logging():
    config = load_config("settings")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    log_file = LOGS_DIR / f"{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, config["log_level"]))
    root_logger.addHandler(file_handler)

    formatter = LogFormatter("[%(asctime)s] %(levelname)s [%(name)s]: %(message)s", datefmt="%H:%M:%S")
    file_handler.setFormatter(formatter)
