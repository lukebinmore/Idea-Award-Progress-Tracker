from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QLineEdit
from IAPT.gui.icons.icons import *


class Component:
    @staticmethod
    def setup(widget, **kwargs):
        layout = kwargs.pop("layout", None)
        name = kwargs.pop("name", None)
        variant = kwargs.pop("variant", None)
        stretch = kwargs.pop("stretch", 0)
        enabled = kwargs.pop("enabled", True)

        if name:
            widget.setObjectName(name)

        if variant:
            widget.setProperty("variant", variant)

        widget.setEnabled(enabled)

        if layout:
            layout.addWidget(widget, stretch)


class Box(QWidget):
    def __init__(self, vertical=False, align="center", **kwargs):
        super().__init__()
        Component.setup(self, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.layout = QVBoxLayout(self) if vertical else QHBoxLayout(self)
        self.setMargins(0, 0, 0, 0)
        self.setSpacing(0)

        if align == "left":
            self.layout.setAlignment(Qt.AlignLeft)
        elif align == "right":
            self.layout.setAlignment(Qt.AlignRight)
        elif align == "top":
            self.layout.setAlignment(Qt.AlignTop)
        elif align == "bottom":
            self.layout.setAlignment(Qt.AlignBottom)
        else:
            self.layout.setAlignment(Qt.AlignCenter)

    def addWidget(self, widget, stretch=0):
        self.layout.addWidget(widget, stretch)

    def setMargins(self, left, top, right, bottom):
        self.layout.setContentsMargins(left, top, right, bottom)

    def setSpacing(self, spacing):
        self.layout.setSpacing(spacing)


class Button(QPushButton):
    def __init__(self, text="", icon=None, icon_size=None, **kwargs):
        super().__init__(text)
        Component.setup(self, **kwargs)

        self.setIcon(icon) if icon else None
        self.setIconSize(QSize(*icon_size)) if icon_size else None


class Label(QLabel):
    def __init__(self, text="", align="center", **kwargs):
        super().__init__(text)
        Component.setup(self, **kwargs)

        if align == "center":
            self.setAlignment(Qt.AlignCenter)
        elif align == "left":
            self.setAlignment(Qt.AlignLeft)
        else:
            self.setAlignment(Qt.AlignRight)


class LineEdit(QLineEdit):
    def __init__(self, **kwargs):
        super().__init__()
        Component.setup(self, **kwargs)


class Header(Box):
    def __init__(self, layout):
        super().__init__(vertical=False, layout=layout, name="header")

        self.back_button = Button(layout=self, name="back_btn", icon=back_icon, icon_size=(30, 30), enabled=False)
        self.program_title = Label(text="Idea Award Progress Tracker", layout=self, name="program_title", stretch=1)
        self.forward_button = Button(
            layout=self, name="forward_btn", icon=forward_icon, icon_size=(30, 30), enabled=False
        )


class Footer(Box):
    def __init__(self, layout):
        super().__init__(vertical=False, layout=layout, name="footer")

        quote = Label(text="Fun quotes go here", layout=self, name="quote")


class Navigation(Box):
    pageSelected = Signal(object)

    def __init__(self, layout, pages):
        super().__init__(vertical=True, layout=layout, name="navigation", align="top")

        self.navigation_buttons = {}

        self.setFixedWidth(150)

        Label(text="Navigation", layout=self, name="navigation_label")

        for page in pages:
            button = Button(text=page.page_title, layout=self, name=page.nav_btn_name, variant="navigation_btn")
            button.clicked.connect(lambda checked=False, page=page: self.pageSelected.emit(page))
            self.navigation_buttons[page.nav_btn_name] = button


class Search(Box):
    def __init__(self, layout):
        super().__init__(vertical=False, layout=layout, name="search")

        search_label = Label(text="Search:", layout=self, name="search_label")
        self.search_box = LineEdit(layout=self, stretch=1, name="searchbox")


class Filters(Box):
    def __init__(self, layout):
        super().__init__(vertical=True, layout=layout, name="filters", align="top")

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
