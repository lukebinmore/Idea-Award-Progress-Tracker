from IAPT.core.config import initialise_directories, initialise_config
from IAPT.core.database import initialise_database
from IAPT.core.logs import initialise_logging
import logging

logger = logging.getLogger(__name__)


def startup():
    print("Starting Application...")

    try:
        print("Initialising Directories...", end="")
        initialise_directories()
        print("Done!")

        print("Initialising Config...", end="")
        initialise_config()
        print("Done!")

        print("Initialising Logging...", end="")
        initialise_logging()
        print("Done!")

        print("initialising Database...", end="")
        initialise_database()
        print("Done!")

        logger.info("Initialisation Complete")
    except Exception:
        print("Failed to initialise application!")
        raise
