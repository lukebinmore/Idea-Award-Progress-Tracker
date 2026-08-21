from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from IAPT.gui.components import Page


class StudentsPage(Page):
    page_title = "Students"

    def __init__(self):
        super().__init__()

        title = QLabel("Students")
        title.setObjectName("page_title")
        title.setAlignment(Qt.AlignCenter)
        self.addWidget(title)
