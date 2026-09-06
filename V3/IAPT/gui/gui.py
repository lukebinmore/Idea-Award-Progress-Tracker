import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFileSystemWatcher
from IAPT.gui.main_window import MainWindow
from IAPT.gui.styles.stylesheet import build_stylesheet, load_style_config
from IAPT.core.config import PACKAGE_ROOT
import logging

logger = logging.getLogger(__name__)


def reload_stylesheet(app, stylesheet_path, config_path):
    with stylesheet_path.open("r", encoding="utf-8") as file:
        stylesheet = file.read()
    app.setStyleSheet(build_stylesheet(stylesheet, load_style_config(config_path)))


def start_gui():
    logger.info("Starting GUI")
    app = QApplication(sys.argv)

    stylesheet_path = PACKAGE_ROOT / "gui" / "styles" / "style.qss"
    config_path = PACKAGE_ROOT / "gui" / "styles" / "stylesheet.json"
    reload_stylesheet(app, stylesheet_path, config_path)
    app.style_watcher = QFileSystemWatcher()
    app.style_watcher.addPaths([str(stylesheet_path), str(config_path)])
    app.style_watcher.fileChanged.connect(lambda: reload_stylesheet(app, stylesheet_path, config_path))

    window = MainWindow()
    window.setWindowTitle("IAPT")
    window.resize(1000, 600)
    window.show()

    logger.info("GUI Started")

    sys.exit(app.exec())
