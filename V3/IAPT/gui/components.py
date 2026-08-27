from IAPT.core.logs import NotificationHandler
import logging
from PySide6.QtCore import Qt, Signal, QSize, QEvent, QTimer
from PySide6.QtGui import QColor, QPainterPath, QRegion, QPen
from PySide6.QtWidgets import (
    QStyledItemDelegate,
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
    QCompleter,
    QProgressBar,
)
from IAPT.gui.icons.icons import *
from IAPT.gui.styles.stylesheet import COLOURS, RADIUS
from IAPT.gui.quotes import QUOTES
import random


class CenterItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class RightAlignedItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter


class TableDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if index.row() == self.parent().hovered_row:
            painter.save()
            painter.fillRect(option.rect, QColor(255, 255, 255, 20))
            painter.restore()

        painter.save()
        painter.setPen(QPen(QColor(COLOURS["border_secondary"]), 2))
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        painter.restore()


class Component:
    @staticmethod
    def setup(widget, **kwargs):
        layout = kwargs.pop("layout", None)
        name = kwargs.pop("name", None)
        variant = kwargs.pop("variant", None)
        stretch = kwargs.pop("stretch", 0)
        enabled = kwargs.pop("enabled", True)
        height = kwargs.pop("height", None)
        width = kwargs.pop("width", None)

        widget.setObjectName(name) if name else None
        widget.setProperty("variant", variant) if variant else None
        widget.setEnabled(enabled)
        widget.setFixedHeight(height) if height else None
        widget.setFixedWidth(width) if width else None
        layout.addWidget(widget, stretch) if layout else None

        widget.kwargs = kwargs


class Box(QWidget):
    def __init__(self, vertical=False, align="top", overflow=True, spacing=0, margins=(0, 0, 0, 0), **kwargs):
        super().__init__(kwargs.pop("parent", None))
        Component.setup(self, **kwargs)

        self.overflow = overflow
        self.radius = int(RADIUS["standard"][:-2])

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.layout = QVBoxLayout(self) if vertical else QHBoxLayout(self)
        self.setMargins(*margins)
        self.setSpacing(spacing)

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

    def updateMask(self):
        if self.overflow:
            self.clearMask()
            return

        path = QPainterPath()
        path.addRoundedRect(self.rect(), self.radius, self.radius)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.overflow:
            self.updateMask()


class CollapsibleBox(Box):
    def __init__(self, content=None, text=None, icon=None, icon_size=None, button_vert=True, collapsed=False, **kwargs):
        super().__init__(**kwargs)

        self.collapsed = collapsed
        self.collapsed_button = Button(
            layout=self,
            text=text,
            icon=icon,
            icon_size=icon_size,
            name=kwargs.get("name", "") + "_collapsed_btn",
        )

        if button_vert:
            self.collapsed_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        else:
            self.collapsed_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.content = content
        self.addWidget(content)
        self.setCollapsed(self.collapsed)

        self.collapsed_button.installEventFilter(self)
        self.window().installEventFilter(self)
        self.installEventFilter(self)

    def setCollapsed(self, collapsed):
        if collapsed:
            self.content.hide()
            self.collapsed_button.show()
        else:
            self.content.show()
            self.collapsed_button.hide()

    def checkWidth(self, width):
        if width < 700:
            self.collapsed = True
            self.setCollapsed(True)
        else:
            self.collapsed = False
            self.setCollapsed(False)

    def eventFilter(self, watched, event):
        if self.collapsed:
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

    def __init__(self, page_area=None, **kwargs):
        super().__init__(vertical=True, spacing=5, **kwargs)

        self.page_area = page_area

        Label(text=self.page_title, layout=self, name="page_title")


class Button(QPushButton):
    def __init__(self, text="", icon=None, icon_size=None, **kwargs):
        super().__init__(text)
        Component.setup(self, **kwargs)

        self.setIcon(icon) if icon else None
        self.setIconSize(QSize(*icon_size)) if icon_size else None


class Label(QLabel):
    def __init__(self, text="", align="center", wrap=True, **kwargs):
        super().__init__(text)
        Component.setup(self, **kwargs)

        self.setWordWrap(wrap)

        if align == "center":
            self.setAlignment(Qt.AlignCenter)
        elif align == "right":
            self.setAlignment(Qt.AlignRight)
        else:
            self.setAlignment(Qt.AlignLeft)

        self.adjustSize()


class LineEdit(QLineEdit):
    def __init__(self, read_only=False, suggestions=None, case_sensitive=False, align="center", **kwargs):
        super().__init__()
        Component.setup(self, **kwargs)

        self.setReadOnly(read_only)

        completer = QCompleter(suggestions)
        completer.setCaseSensitivity(Qt.CaseSensitive if case_sensitive else Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setFilterMode(Qt.MatchContains)
        self.setCompleter(completer)

        if align == "center":
            self.setAlignment(Qt.AlignCenter)
            completer.popup().setItemDelegate(CenterItemDelegate(completer.popup()))
        elif align == "right":
            self.setAlignment(Qt.AlignRight)
            completer.popup().setItemDelegate(RightAlignedItemDelegate(completer.popup()))
        else:
            self.setAlignment(Qt.AlignLeft)


class ProgressBar(QProgressBar):
    def __init__(self, range=(0, 1), start_value=0, show_text=False, **kwargs):
        super().__init__()
        Component().setup(self, **kwargs)

        self.setRange(*range)
        self.setValue(start_value)
        self.setTextVisible(show_text)


class Table(QTableWidget):
    def __init__(self, columns, expandable=True, **kwargs):
        super().__init__()
        Component.setup(self, **kwargs)

        self.row_objects = {}
        self.hovered_row = -1

        self.viewport().setMouseTracking(True)
        self.viewport().installEventFilter(self)

        self.expandable = expandable
        self.setItemDelegate(TableDelegate(self))

        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels([name for name, attribute in columns])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.cellClicked.connect(self._cellClicked) if self.expandable else None

    def eventFilter(self, watched, event):
        if watched is self.viewport() and event.type() == QEvent.MouseMove:
            index = self.indexAt(event.position().toPoint())
            self.hovered_row = index.row()
            self.viewport().update()

        elif event.type() == QEvent.Leave:
            self.hovered_row = -1
            self.viewport().update()

        return super().eventFilter(watched, event)

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
        self.clearSelection()


class TableRow:
    def __init__(self, table, columns, data, row_colour=None):
        self.table = table

        self.summary_row = table.rowCount()
        table.insertRow(self.summary_row)
        table.registerRow(self.summary_row, self)
        for column, attribute in enumerate(columns):
            value = getattr(data, attribute)
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor(row_colour)) if row_colour else None
            table.setItem(self.summary_row, column, item)

        if self.table.expandable:
            self.content_row = table.rowCount()
            table.insertRow(self.content_row)
            table.setSpan(self.content_row, 0, 1, len(columns))
            self.content = Box(vertocal=True, height=100, margins=(20, 0, 20, 20))
            table.setCellWidget(self.content_row, 0, self.content)
            table.setRowHidden(self.content_row, True)
            self.table.resizeRowToContents(self.content_row)

    def toggleOverview(self):
        self.table.setRowHidden(self.content_row, not self.table.isRowHidden(self.content_row))


class ExpandingButton(Box):
    def __init__(self, start_hidden=True, vertical=True, **kwargs):
        super().__init__(vertical=True, **kwargs)

        self.button = Button(layout=self, **self.kwargs)
        self.content = Box(vertical=vertical, layout=self, name=kwargs.get("name", "") + "_content")
        self.content.setHidden(start_hidden)

        self.button.clicked.connect(self.toggleContent)

    def toggleContent(self):
        self.content.setHidden(not self.content.isHidden())


class Header(Box):
    def __init__(self, layout):
        super().__init__(layout=layout, name="header", margins=(10, 5, 10, 5))

        self.back_button = Button(layout=self, name="back_btn", icon=back_icon, icon_size=(30, 30), enabled=False)
        self.program_title = Label(text="Idea Award Progress Tracker", layout=self, name="program_title", stretch=1)
        self.forward_button = Button(
            layout=self, name="forward_btn", icon=forward_icon, icon_size=(30, 30), enabled=False
        )


class Footer(Box):
    def __init__(self, layout):
        super().__init__(layout=layout, name="footer")

        quote = random.choice(QUOTES)

        Label(text=quote, layout=self, name="quote")


class Navigation(CollapsibleBox):
    pageSelected = Signal(object)

    def __init__(self, layout, pages):
        self.content = Box(vertical=True, width=150, spacing=5, margins=(0, 10, 0, 10))
        super().__init__(layout=layout, content=self.content, name="navigation", icon=navigation_icon)

        self.navigation_buttons = {}

        Label(text="Navigation", layout=self.content, name="navigation_label")

        for page in pages:
            button = Button(text=page.page_title, layout=self.content, name=page.nav_btn_name)
            button.clicked.connect(lambda checked=False, page=page: self.pageSelected.emit(page))
            self.navigation_buttons[page.nav_btn_name] = button


class Search(Box):
    def __init__(self, layout):
        super().__init__(layout=layout, name="search", margins=(10, 0, 0, 0))

        search_label = Label(text="Search:", layout=self, name="search_label")
        self.search_box = LineEdit(layout=self, stretch=1, name="searchbox", align="left")


class Filters(CollapsibleBox):
    def __init__(self, layout):
        self.content = Box(vertical=True, width=150, margins=(0, 10, 0, 10))
        super().__init__(layout=layout, content=self.content, name="filters", icon=filters_icon)

        Label(text="Testing", layout=self.content, name="filters_label")


class PageEntry:
    def __init__(self, page_class, state=None):
        self.page_class = page_class
        self.state = state or {}
        self.title = page_class.page_title


class PageArea(Box):
    backAvailable = Signal(bool)
    forwardAvailable = Signal(bool)

    def __init__(self, layout):
        super().__init__(
            vertical=True, layout=layout, overflow=False, name="page_area", stretch=1, margins=(10, 10, 10, 10)
        )

        self.history = []
        self.current_index = -1
        self.current_page = None

    def _loadPage(self):
        if self.current_page:
            self.current_page.deleteLater()

        entry = self.history[self.current_index]

        self.current_page = entry.page_class(page_area=self)
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

    def refreshPage(self):
        self._loadPage()


class NotificationArea(Box):
    def __init__(self, parent):
        super().__init__(parent=parent, vertical=True, name="notifications", width=250, align="right")

        self.raise_()

        margin = 10
        self.move(self.parent().width() - self.width() - margin, margin)

        self.notification_handler = NotificationHandler(self)
        self.notification_handler.setLevel(logging.WARNING)
        logging.getLogger().addHandler(self.notification_handler)

    def addNotification(self, record):
        Notification(self, record)

    def event(self, event):
        if event.type() == QEvent.LayoutRequest:
            self.adjustPos()
        return super().event(event)

    def adjustPos(self):
        self.adjustSize()
        margin = 10
        self.move(self.parent().width() - self.width() - margin, margin)


class Notification(Box):
    def __init__(self, layout, record):
        super().__init__(layout=layout, vertical=True, spacing=5, margins=(5, 5, 5, 5))

        title = record.getMessage()
        level = record.levelname

        self.setProperty("variant", level)

        header = Box(layout=self, variant="notification_header")
        title = Label(layout=header, text=title, stretch=1, align="left")
        close_btn = Button(layout=header, icon=close_icon, icon_size=(20, 20))
        close_btn.clicked.connect(self.deleteLater)

        if level == "SUCCESS":
            self.startTimer(3000)
        else:
            if record.error:
                content = Box(vertical=True, layout=self, spacing=7, margins=(0, 0, 0, 5))
                Label(text=record.error.message, layout=content)
                if record.error.error_data:
                    for key, value in record.error.error_data.items():
                        key = key.replace("_", " ").title()
                        Label(text=f"{key}: {value}", layout=content)

    def startTimer(self, duration):
        self.progress = ProgressBar(layout=self, range=(0, duration), start_value=duration, height=3)

        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start()

    def updateTimer(self):
        value = self.progress.value() - 50
        self.progress.setValue(value)

        if value <= 0:
            self.timer.stop()
            self.deleteLater()
