from IAPT.core.startup import startup
from IAPT.gui.gui import start_gui
from IAPT.core.imports import import_students, import_results, import_schedule
from IAPT.core.database import read_students
import logging

logger = logging.getLogger(__name__)


def run():
    startup()

    try:
        logger.info("Application started")
        # test_imports()
        start_gui()
    except Exception:
        logger.critical("Application encountered an unexpected error")
        raise


def test_imports():
    import_students("C:\\Users\\lukeb\\Downloads\\students.xlsx", "9X-It1")
    import_results("C:\\Users\\lukeb\\Downloads\\test.xlsx")
    import_schedule("C:\\Users\\lukeb\\Downloads\\homework.xlsx")
