from IAPT.core.config import load_config, LOGS_DIR
from datetime import datetime
import logging

SUCCESS = 45
logging.addLevelName(SUCCESS, "SUCCESS")


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)


logging.Logger.success = success
logger = logging.getLogger(__name__)


class LogFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)

        if hasattr(record, "error"):
            if record.error.details:
                message += f"\n    - Details: {record.error.details}"
            else:
                message += f"\n    - Message: {record.error.message}"

        return message


class NotificationHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.WARNING or record.levelno == SUCCESS:
            print("GUI NOTIFICATION:")
            print(f"  Level: {record.levelname}")
            print(f"  Message: {record.msg}")

            if hasattr(record, "error"):
                print(f"  User message: {record.error.message}")
                print(f"  Details: {record.error.details}")
                print(f"  File: {record.error.file_path}")

            print()


def initialise_logging():
    config = load_config("settings")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    log_file = LOGS_DIR / f"{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, config["log_level"]))
    root_logger.addHandler(file_handler)

    notification_handler = NotificationHandler()
    notification_handler.setLevel(logging.WARNING)
    root_logger.addHandler(notification_handler)

    formatter = LogFormatter("[%(asctime)s] %(levelname)s [%(name)s]: %(message)s", datefmt="%H:%M:%S")
    file_handler.setFormatter(formatter)
