import sys
from PySide6.QtWidgets import QApplication, QMainWindow


def start_gui():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("IAPT")
    window.resize(1200, 800)
    window.show()

    sys.exit(app.exec())
