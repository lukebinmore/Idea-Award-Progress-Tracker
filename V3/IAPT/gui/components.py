from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QLineEdit, QComboBox
from IAPT.gui.icons.icons import *


class Box(QWidget):
    def __init__(self, vertical=False, layout=None, name=None, stretch=0):
        super().__init__()

        self.setObjectName(name) if name else None
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.layout = QVBoxLayout(self) if vertical else QHBoxLayout(self)
        self.setMargins(0, 0, 0, 0)
        self.setSpacing(0)

        layout.addWidget(self, stretch=stretch) if layout else None

    def addWidget(self, widget, stretch=0):
        self.layout.addWidget(widget, stretch)

    def setMargins(self, left, top, right, bottom):
        self.layout.setContentsMargins(left, top, right, bottom)

    def setSpacing(self, spacing):
        self.layout.setSpacing(spacing)


class Page(Box):
    page_title = "Untitled Page"

    def __init__(self):
        super().__init__(vertical=True, name="page")


class Header(Box):
    def __init__(self, layout):
        super().__init__(vertical=False, layout=layout, name="header")

        self.back_button = QPushButton()
        self.back_button.setObjectName("back_button")
        self.back_button.setIcon(back_icon)
        self.back_button.setIconSize(QSize(30, 30))
        self.back_button.setEnabled(False)
        self.addWidget(self.back_button)

        program_title = QLabel("Idea Award Progress Tracker")
        program_title.setObjectName("program_title")
        program_title.setAlignment(Qt.AlignCenter)
        self.addWidget(program_title, stretch=1)

        self.forward_button = QPushButton()
        self.forward_button.setObjectName("forward_button")
        self.forward_button.setIcon(forward_icon)
        self.forward_button.setIconSize(QSize(30, 30))
        self.forward_button.setEnabled(False)
        self.addWidget(self.forward_button)


class Footer(Box):
    def __init__(self, layout):
        super().__init__(vertical=False, layout=layout, name="footer")

        quote = QLabel("Fun Quotes go here")
        quote.setObjectName("quote")
        quote.setAlignment(Qt.AlignCenter)
        self.addWidget(quote)


class Navigation(Box):
    def __init__(self, layout):
        super().__init__(vertical=True, layout=layout, name="navigation")

        self.setFixedWidth(150)


class Search(Box):
    def __init__(self, layout):
        super().__init__(vertical=False, layout=layout, name="search")

        self.setSpacing(0)

        search_label = QLabel("Search:")
        search_label.setObjectName("search_label")
        self.addWidget(search_label)

        self.search_box = QLineEdit()
        self.search_box.setObjectName("searchbox")
        self.addWidget(self.search_box, stretch=1)

        self.search_type = QComboBox()
        self.search_type.setObjectName("search_type")
        self.search_type.addItem("All", "all")
        self.search_type.addItem("Current Page", "current_page")
        self.addWidget(self.search_type)


class Filters(Box):
    def __init__(self, layout):
        super().__init__(vertical=True, layout=layout, name="filters")

        self.setFixedWidth(150)


class PageEntry:
    def __init__(self, page_class, state=None):
        self.page_class = page_class
        self.state = state or {}
        self.title = page_class.page_title


class PageArea(Box):
    backAvailable = Signal(bool)
    forwardAvailable = Signal(bool)

    def __init__(self, layout):
        super().__init__(vertical=True, layout=layout, name="page_area", stretch=1)

        self.history = []
        self.current_index = -1
        self.current_page = None

    def _loadPage(self):
        if self.current_page:
            self.current_page.deleteLater()

        entry = self.history[self.current_index]

        self.current_page = entry.page_class()
        self.addWidget(self.current_page, stretch=1)
        self.current_page.show()
        self.backAvailable.emit(self.current_index > 0)
        self.forwardAvailable.emit(self.current_index < len(self.history) - 1)

    def showPage(self, page_class):
        self.history = self.history[: self.current_index + 1]
        entry = PageEntry(page_class)
        self.history.append(entry)
        self.current_index += 1

        if self.current_page:
            self.current_page.deleteLater()

        self._loadPage()

    def goBack(self):
        if self.current_index <= 0:
            return
        self.current_index -= 1
        self._loadPage()

    def goForward(self):
        if self.current_index >= len(self.history) - 1:
            return
        self.current_index += 1
        self._loadPage()
