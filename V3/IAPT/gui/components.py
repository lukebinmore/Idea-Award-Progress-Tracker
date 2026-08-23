from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QLineEdit,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
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
    def __init__(self, vertical=False, align="top", **kwargs):
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


class CollapsibleBox(Box):
    def __init__(self, icon=None, icon_size=None, **kwargs):
        name = kwargs.get("name", "default")
        layout = kwargs.get("layout")
        super().__init__(**kwargs)

        self.width_collapsed = False
        self.collapsed_button = Button(layout=layout, icon=icon, icon_size=icon_size, name=name + "_collapsed_btn")
        self.collapsed_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.collapsed_button.installEventFilter(self)
        self.window().installEventFilter(self)
        self.installEventFilter(self)

    def setCollapsed(self, collapsed):
        if collapsed:
            self.hide()
            self.collapsed_button.show()
        else:
            self.show()
            self.collapsed_button.hide()

    def checkWidth(self, width):
        if width < 700:
            self.width_collapsed = True
            self.setCollapsed(True)
        else:
            self.width_collapsed = False
            self.setCollapsed(False)

    def eventFilter(self, watched, event):
        if self.width_collapsed:
            if watched == self.collapsed_button:
                if event.type() == QEvent.Enter:
                    self.setCollapsed(False)

            elif event.type() == QEvent.Leave:
                if watched == self or watched == self.window():
                    self.setCollapsed(True)
        return super().eventFilter(watched, event)


class Page(Box):
    page_title = "untitled_page"
    nav_btn_name = "untitled_btn"

    def __init__(self, name="untitled_page"):
        super().__init__(vertical=True, align="top", name=name)

        Label(text=self.page_title, layout=self, variant="page_title")


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


class Table(QTableWidget):

    def __init__(self, columns, expandable=True, **kwargs):
        variant = kwargs.get("variant", None)
        super().__init__()
        Component.setup(self, **kwargs)

        self.row_objects = {}
        self.expandable = expandable

        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels([name for name, attribute in columns])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setProperty("variant", variant) if variant else None

        self.cellClicked.connect(self._cellClicked) if self.expandable else None

    def sizeColumns(self):
        available_width = self.viewport().width()

        final_widths = []
        for column in range(self.columnCount()):
            widest = 0
            minimum = self.horizontalHeader().sectionSizeHint(column) + 10
            for row in range(self.rowCount()):
                item = self.item(row, column)
                if item:
                    width = self.fontMetrics().horizontalAdvance(item.text()) + 10
                    widest = max(widest, width)
            final_widths.append(max(minimum, widest))

        if sum(final_widths) <= available_width:
            extra_width = (available_width - sum(final_widths)) / len(final_widths)
            final_widths = [width + extra_width for width in final_widths]

        for column, width in enumerate(final_widths):
            self.setColumnWidth(column, width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.sizeColumns()

    def registerRow(self, row, student_row):
        self.row_objects[row] = student_row

    def _cellClicked(self, row, column):
        if row in self.row_objects:
            self.row_objects[row].toggleOverview()


class TableRow:
    def __init__(self, table, columns, data):
        self.table = table

        self.summary_row = table.rowCount()
        table.insertRow(self.summary_row)
        table.registerRow(self.summary_row, self)
        for column, attribute in enumerate(columns):
            value = getattr(data, attribute)
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(self.summary_row, column, item)

        if self.table.expandable:
            self.content_row = table.rowCount()
            table.insertRow(self.content_row)
            table.setSpan(self.content_row, 0, 1, len(columns))
            self.content = QWidget()
            table.setCellWidget(self.content_row, 0, self.content)
            table.setRowHidden(self.content_row, True)

    def toggleOverview(self):
        self.table.setRowHidden(self.content_row, not self.table.isRowHidden(self.content_row))


class Header(Box):
    def __init__(self, layout):
        super().__init__(layout=layout, name="header")

        self.back_button = Button(layout=self, name="back_btn", icon=back_icon, icon_size=(30, 30), enabled=False)
        self.program_title = Label(text="Idea Award Progress Tracker", layout=self, name="program_title", stretch=1)
        self.forward_button = Button(
            layout=self, name="forward_btn", icon=forward_icon, icon_size=(30, 30), enabled=False
        )


class Footer(Box):
    def __init__(self, layout):
        super().__init__(layout=layout, name="footer")

        quote = Label(text="Fun quotes go here", layout=self, name="quote")


class Navigation(CollapsibleBox):
    pageSelected = Signal(object)

    def __init__(self, layout, pages):
        super().__init__(vertical=True, layout=layout, name="navigation", icon=navigation_icon)

        self.navigation_buttons = {}
        self.setFixedWidth(150)

        Label(text="Navigation", layout=self, name="navigation_label")

        for page in pages:
            button = Button(text=page.page_title, layout=self, name=page.nav_btn_name, variant="navigation_btn")
            button.clicked.connect(lambda checked=False, page=page: self.pageSelected.emit(page))
            self.navigation_buttons[page.nav_btn_name] = button


class Search(Box):
    def __init__(self, layout):
        super().__init__(layout=layout, name="search")

        search_label = Label(text="Search:", layout=self, name="search_label")
        self.search_box = LineEdit(layout=self, stretch=1, name="searchbox")


class Filters(CollapsibleBox):
    def __init__(self, layout):
        super().__init__(vertical=True, layout=layout, name="filters", icon=filters_icon)

        self.setFixedWidth(150)

        Label(text="Testing", layout=self, name="filters_label")


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
