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

            if record.error.error_data:
                for key, value in record.error.error_data.items():
                    message += f"\n    - {key}: {value}"

        return message


class NotificationHandler(logging.Handler):
    def __init__(self, notification_area):
        super().__init__()
        self.notification_area = notification_area

    def emit(self, record):
        self.notification_area.addNotification(record)


def initialise_logging():
    config = load_config("settings")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    log_file = LOGS_DIR / f"{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, config["log_level"]))
    root_logger.addHandler(file_handler)

    logs = sorted(LOGS_DIR.glob("*.log"), key=lambda path: path.stat().st_mtime)
    if len(logs) > 30:
        for log in logs[:-30]:
            log.unlink()

    formatter = LogFormatter("[%(asctime)s] %(levelname)s [%(name)s]: %(message)s", datefmt="%H:%M:%S")
    file_handler.setFormatter(formatter)
