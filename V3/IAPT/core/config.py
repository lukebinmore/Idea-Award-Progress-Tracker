import sys
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def get_app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parents[2]


APP_ROOT = get_app_root()
APP_DATA = APP_ROOT / "AppData"

DATABASE_DIR = APP_DATA / "database"
CONFIG_DIR = APP_DATA / "config"
BACKUPS_DIR = APP_DATA / "backups"
LOGS_DIR = APP_DATA / "logs"

DATABASE_PATH = DATABASE_DIR / "db.db"
CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "student_import": {
        "student_id": "Candidate Number",
        "first_name": "First Name",
        "last_name": "Last Name",
    },
    "results_import": {
        "student_id": "Email",
        "bronze_points_total": "Bronze Points Total",
        "bronze_citizen": "Bronze Citizen Points",
        "bronze_worker": "Bronze Worker Points",
        "bronze_maker": "Bronze Maker Points",
        "bronze_entrepreneur": "Bronze Entrepreneur Points",
        "silver_points_total": "Silver Points Total",
        "bronze_award_date": "Bronze Award Date",
        "silver_award_date": "Silver Award Date",
        "badge_list": "Badge List",
    },
    "schedule_import": {"badge_name": "Badge Name", "category": "Category", "points": "Points", "due_date": "Due Date"},
    "settings": {"log_level": "INFO"},
}


def initialise_directories():
    directories = [
        DATABASE_DIR,
        CONFIG_DIR,
        BACKUPS_DIR,
        LOGS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def initialise_config():
    if not CONFIG_PATH.exists():
        with CONFIG_PATH.open("w", encoding="utf-8") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        return

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = json.load(file)

    changed = False

    for section, defaults in DEFAULT_CONFIG.items():
        if section not in config:
            config[section] = defaults
            changed = True
            continue

        for key, default_value in defaults.items():
            if key not in config[section]:
                config[section][key] = default_value
                changed = True

    if changed:
        with CONFIG_PATH.open("w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)


def load_config(section=None):
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            config = json.load(file)
            if section:
                return config[section]
            return config

    except FileNotFoundError:
        logger.error_detail("Config file could not be found")
        raise

    except json.JSONDecodeError:
        logger.error_detail("Config file contains invalid JSON")
        raise

    except OSError:
        logger.error_detail("Config file could not be read")
        raise

    except KeyError:
        logger.error_detail("Config section not found", extra={"section": section})
        raise
