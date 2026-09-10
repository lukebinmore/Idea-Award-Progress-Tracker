from IAPT.core.logs import NotificationHandler
import logging
from PySide6.QtCore import Qt, Signal, QSize, QEvent, QTimer, QPoint
from PySide6.QtGui import QColor, QPainterPath, QRegion, QPen, QIntValidator
from PySide6.QtWidgets import (
    QStyledItemDelegate,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
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
    QCheckBox,
    QComboBox,
    QStyle,
    QStyleOptionComboBox,
    QStylePainter,
    QDateEdit,
    QCalendarWidget,
    QScrollArea,
    QFrame,
)
from IAPT.gui.icons.icons import *
from IAPT.gui.styles.stylesheet import COLOURS
from IAPT.gui.quotes import QUOTES
from IAPT.core.data import get_students, get_classes, get_homeworks
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
        bg_colour = kwargs.pop("bg_colour", None)
        colour = kwargs.pop("colour", None)
        stretch = kwargs.pop("stretch", 0)
        enabled = kwargs.pop("enabled", True)
        height = kwargs.pop("height", None)
        width = kwargs.pop("width", None)
        position = kwargs.pop("position", None)

        widget.setObjectName(name) if name else None
        widget.setProperty("variant", variant) if variant else None
        widget.setProperty("bg_colour", bg_colour) if bg_colour else None
        widget.setProperty("colour", colour) if colour else None
        widget.setEnabled(enabled)
        widget.setFixedHeight(height) if height else None
        widget.setFixedWidth(width) if width else None

        if layout:
            if position != None:
                layout.addWidget(widget, row=position[0], column=position[1])
            else:
                layout.addWidget(widget, stretch)

        widget.kwargs = kwargs


class Box(QWidget):
    def __init__(
        self,
        vertical=False,
        grid=False,
        position=None,
        align="top",
        overflow=True,
        spacing=0,
        margins=(0, 0, 0, 0),
        scrollable=False,
        **kwargs,
    ):
        super().__init__(kwargs.pop("parent", None))

        if scrollable:
            self.scroll_area = QScrollArea()
            Component.setup(self.scroll_area, position=position, **kwargs)
            self.scroll_area.setWidget(self)
            self.scroll_area.setWidgetResizable(True)

            if grid:
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            elif vertical:
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            else:
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            self.scroll_area.setFrameShape(QFrame.NoFrame)
            self.kwargs = kwargs
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        else:
            Component.setup(self, position=position, **kwargs)

        self.overflow = overflow
        self.radius = 20

        self.setAttribute(Qt.WA_StyledBackground, True)
        if grid:
            self.layout = QGridLayout(self)
        elif vertical:
            self.layout = QVBoxLayout(self)
        else:
            self.layout = QHBoxLayout(self)
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

    def addWidget(self, widget, stretch=0, row=None, column=None):
        if row != None and column != None:
            self.layout.addWidget(widget, row, column)
        else:
            self.layout.addWidget(widget, stretch)

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def setMargins(self, left, top, right, bottom):
        self.layout.setContentsMargins(left, top, right, bottom)

    def setSpacing(self, spacing):
        self.layout.setSpacing(spacing)

    def updateMask(self):
        if self.overflow == True:
            self.clearMask()
            return

        margins = self.layout.contentsMargins()
        rect = self.rect().adjusted(
            margins.left(),
            margins.top(),
            -margins.right(),
            -margins.bottom(),
        )

        top_left, top_right, bottom_right, bottom_left = self.overflow

        path = QPainterPath()
        path.moveTo(rect.left() + top_left, rect.top())

        path.lineTo(rect.right() - top_right, rect.top())
        if top_right:
            path.arcTo(
                rect.right() - 2 * top_right,
                rect.top(),
                2 * top_right,
                2 * top_right,
                90,
                -90,
            )

        path.lineTo(rect.right(), rect.bottom() - bottom_right)
        if bottom_right:
            path.arcTo(
                rect.right() - 2 * bottom_right,
                rect.bottom() - 2 * bottom_right,
                2 * bottom_right,
                2 * bottom_right,
                0,
                -90,
            )

        path.lineTo(rect.left() + bottom_left, rect.bottom())
        if bottom_left:
            path.arcTo(
                rect.left(),
                rect.bottom() - 2 * bottom_left,
                2 * bottom_left,
                2 * bottom_left,
                270,
                -90,
            )

        path.lineTo(rect.left(), rect.top() + top_left)
        if top_left:
            path.arcTo(
                rect.left(),
                rect.top(),
                2 * top_left,
                2 * top_left,
                180,
                -90,
            )

        path.closeSubpath()
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overflow != True:
            self.updateMask()


class CollapsibleBox(Box):
    def __init__(
        self,
        layout=None,
        text=None,
        icon=None,
        icon_size=None,
        button_vert=True,
        collapsed=False,
        **kwargs,
    ):
        super().__init__(layout=layout, **kwargs)

        self.collapsed = collapsed
        self.collapsed_button = Button(
            layout=layout, text=text, icon=icon, icon_size=icon_size, name=kwargs.get("name", "") + "_collapsed_btn"
        )

        if button_vert:
            self.collapsed_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        else:
            self.collapsed_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.setCollapsed(self.collapsed)

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
    filters = False

    def __init__(self, page_area=None, **kwargs):
        super().__init__(stretch=1, **kwargs)
        self.page_area = page_area
        self.controls = []
        self.state = {}

        self.page = Box(
            vertical=True,
            layout=self,
            name="main_content",
            overflow=(20, 20, 20, 20),
            spacing=5,
            margins=(10, 10, 10, 10),
        )
        self.page_header = Label(layout=self.page, name="page_title")

        self.content = Box(layout=self.page, vertical=True, spacing=10, scrollable=True, stretch=1)

        if self.filters:
            self.filters_container = CollapsibleBox(
                layout=self,
                name="filters",
                vertical=True,
                spacing=5,
                icon=filters_icon,
                margins=(0, 10, 0, 10),
                width=160,
                overflow=(20, 0, 0, 20),
            )
            Label(text="Filters", layout=self.filters_container, name="filters_label")
            self.filters = Box(vertical=True, spacing=5, layout=self.filters_container, scrollable=True)

    def drawPage(self):
        self.content.clear()

        if self.filters:
            self.filters.clear()

        if self.page_area:
            self.page_area.updateSearchData()


class Button(QPushButton):
    def __init__(self, text="", icon=None, icon_size=None, align="center", **kwargs):
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
    def __init__(self, text=None, read_only=False, suggestions=None, case_sensitive=False, align="center", **kwargs):
        super().__init__(text=text)
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


class NumberEdit(LineEdit):
    valueCommitted = Signal(object)

    def __init__(self, minimum=0, maximum=30, value=None, placeholder_text="", **kwargs):
        super().__init__(**kwargs)
        self.setValidator(QIntValidator(minimum, maximum, self))
        self.setPlaceholderText(placeholder_text)
        self.setText(str(value) if value is not None else "")

    def value(self):
        return int(self.text()) if self.text() else None

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.valueCommitted.emit(self.value())

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.valueCommitted.emit(self.value())


class DateEdit(QDateEdit):
    def __init__(self, minimum=None, value=None, **kwargs):
        super().__init__()
        Component.setup(self, **kwargs)
        self.setCalendarPopup(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit().installEventFilter(self)
        self.calendar_popup = QCalendarWidget()
        self.calendar_popup.setWindowFlags(Qt.WindowType.Popup)
        self.calendar_popup.clicked.connect(self._selectDate)
        self.setDisplayFormat("dd/MM/yyyy")
        if minimum:
            self.setMinimumDate(minimum)
        if value:
            self.setDate(value)

    def eventFilter(self, watched, event):
        if watched is self.lineEdit() and event.type() == QEvent.Type.MouseButtonPress:
            self._openCalendar()
            return True
        return super().eventFilter(watched, event)

    def mousePressEvent(self, event):
        self._openCalendar()
        event.accept()

    def _openCalendar(self):
        self.calendar_popup.setMinimumDate(self.minimumDate())
        self.calendar_popup.setSelectedDate(self.date())
        self.calendar_popup.adjustSize()
        self.calendar_popup.move(self.mapToGlobal(QPoint(0, self.height())))
        self.calendar_popup.show()

    def _selectDate(self, value):
        self.setDate(value)
        self.calendar_popup.hide()


class CheckBox(QCheckBox):
    def __init__(
        self,
        text="",
        text_align="left",
        box_only=False,
        box_align="right",
        default=False,
        vertical=False,
        read_only=False,
        **kwargs,
    ):
        super().__init__()
        Component.setup(self, **kwargs)

        self.setChecked(default)
        self.read_only = read_only
        self.setFocusPolicy(Qt.NoFocus) if read_only else None

        if not box_only:
            layout = QVBoxLayout(self) if vertical else QHBoxLayout(self)
            Label(text=text, align=text_align, layout=layout)

            if box_align == "left":
                self.setLayoutDirection(Qt.LeftToRight)
                layout.setContentsMargins(35, 5, 10, 5)
            else:
                self.setLayoutDirection(Qt.RightToLeft)
                layout.setContentsMargins(10, 5, 35, 5)

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def mousePressEvent(self, event):
        if self.read_only:
            event.ignore()
            return

        super().mousePressEvent(event)


class ComboBox(QComboBox):
    def __init__(self, options=None, default=None, align="left", **kwargs):
        super().__init__()
        Component.setup(self, **kwargs)
        self.text_alignment = {
            "center": Qt.AlignmentFlag.AlignCenter,
            "right": Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        }.get(align, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        if align == "center":
            self.setItemDelegate(CenterItemDelegate(self))
        elif align == "right":
            self.setItemDelegate(RightAlignedItemDelegate(self))

        if options:
            if isinstance(options[0], tuple):
                for label, key in options:
                    self.addItem(label, key)
            else:
                for value in options:
                    self.addItem(value, value)

        if default:
            target = self.findData(default)
            self.setCurrentIndex(target) if target >= 0 else None

    def paintEvent(self, event):
        if self.text_alignment == Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter:
            super().paintEvent(event)
            return

        painter = QStylePainter(self)
        option = QStyleOptionComboBox()
        self.initStyleOption(option)
        text = option.currentText
        option.currentText = ""
        painter.drawComplexControl(QStyle.ComplexControl.CC_ComboBox, option)

        text_rect = self.style().subControlRect(
            QStyle.ComplexControl.CC_ComboBox,
            option,
            QStyle.SubControl.SC_ComboBoxEditField,
            self,
        )
        painter.drawItemText(text_rect, self.text_alignment, self.palette(), self.isEnabled(), text)


class ProgressBar(QProgressBar):
    def __init__(self, range=(0, 1), start_value=0, show_text=False, **kwargs):
        super().__init__()
        Component().setup(self, **kwargs)

        max = range[1]

        self.setRange(*range)
        self.setValue(start_value if max >= start_value else max)
        self.setTextVisible(show_text)


class Table(QTableWidget):
    def __init__(self, columns, click_page=None, page_area=None, id_column=0, fit_height=False, **kwargs):
        super().__init__()
        self.fit_height = fit_height
        Component.setup(self, **kwargs)

        self.hovered_row = -1
        self.columns = columns

        self.viewport().setMouseTracking(True)
        self.viewport().installEventFilter(self)

        self.setItemDelegate(TableDelegate(self))

        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels([name for name, _ in columns])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        if self.fit_height:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.setWordWrap(False)
            self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        if click_page:
            self.cellClicked.connect(
                lambda row, column: page_area.showPage(
                    click_page,
                    id=self.item(row, id_column).text(),
                )
            )

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

    def addItem(self, data, row_colour=None):
        row = self.rowCount()
        self.insertRow(row)
        for column, attribute in enumerate(self.columns):
            value = getattr(data, attribute[1])
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor(row_colour)) if row_colour else None
            self.setItem(row, column, item)

        if self.fit_height:
            row_height = self.verticalHeader().defaultSectionSize()
            self.setRowHeight(row, row_height)
            table_height = self.horizontalHeader().height() + self.frameWidth() * 2
            table_height += self.rowCount() * row_height
            self.setFixedHeight(table_height)

        return row


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
        super().__init__(
            layout=layout,
            name="navigation",
            vertical=True,
            spacing=5,
            icon=navigation_icon,
            margins=(0, 10, 0, 10),
            width=160,
            overflow=(0, 20, 20, 0),
        )

        self.navigation_buttons = {}
        Label(text="Navigation", layout=self, name="navigation_label")
        content = Box(vertical=True, spacing=5, layout=self, scrollable=True)

        for page in pages:
            button = Button(text=page.page_title, layout=content, name=page.nav_btn_name)
            button.clicked.connect(lambda checked=False, page=page: self.pageSelected.emit(page))
            self.navigation_buttons[page.nav_btn_name] = button


class Search(Box):
    resultSelected = Signal(object, object)

    def __init__(self, layout):
        super().__init__(layout=layout, name="search", margins=(10, 0, 0, 0))

        Label(text="Search:", layout=self, name="search_label")
        self.search_box = LineEdit(layout=self, stretch=1, name="searchbox", align="left")
        self.search_box.installEventFilter(self)
        self.search_box.textChanged.connect(self.updateResults)

        self.results_box = Box(parent=layout, name="search_results", overflow=(20, 20, 20, 20))
        self.results_box.hide()
        self.move()
        self.updateData()

    def move(self, width=None, height=None):
        parent = self.results_box.parentWidget()
        if not parent:
            return

        position = self.search_box.mapTo(parent, QPoint(0, self.search_box.height()))
        panel = self.results_box

        if width and height:
            panel.setFixedWidth(min(width + 20, self.search_box.width()))
            panel.setFixedHeight(min(height, (self.window().height() / 5) * 3))
        else:
            panel.setMinimumSize(0, 0)
            panel.setMaximumSize(16777215, 16777215)
            QTimer.singleShot(10, panel.adjustSize)

        panel.move(position.x(), position.y())
        panel.raise_()

    def eventFilter(self, watched, event):
        if watched is self.search_box:
            if event.type() == QEvent.FocusIn:
                self.move()
                self.results_box.show()
                self.results_box.raise_()
            elif event.type() == QEvent.FocusOut:
                self.results_box.hide()

        return super().eventFilter(watched, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.move()

    def updateData(self):
        self.students = get_students()
        self.classes = get_classes()
        self.homeworks = get_homeworks()
        self.updateResults(self.search_box.text() if hasattr(self, "search_box") else "")
        self.clearSearch()

    def updateResults(self, text):
        from IAPT.gui.pages.homework import HomeworkPage
        from IAPT.gui.pages.single_class import ClassPage
        from IAPT.gui.pages.student import StudentPage

        self.results_box.clear()
        text = text.strip().lower()
        if not text:
            Label(text="Type to search...", layout=self.results_box, variant="subheading", align="left")
            self.move()
            return

        categories = [
            (
                "Students",
                [
                    (student, str(student), StudentPage, {"id": student.id})
                    for student in self.students
                    if text in str(student).lower()
                ],
            ),
            (
                "Classes",
                [
                    (group, str(group), ClassPage, {"id": group.name})
                    for group in self.classes
                    if text in str(group).lower()
                ],
            ),
            (
                "Homeworks",
                [
                    (homework, str(homework), HomeworkPage, {"id": homework.id})
                    for homework in self.homeworks
                    if text in str(homework).lower()
                ],
            ),
        ]
        result_count = sum(len(results) for _, results in categories)
        width = 0
        height = 0

        if not result_count:
            Label(text="No results found", layout=self.results_box, variant="subheading", align="left")
        else:
            results_scroll = Box(
                layout=self.results_box, vertical=True, scrollable=True, spacing=7, margins=(0, 0, 0, 10)
            )
            for category, results in categories:
                if not results:
                    continue

                Label(text=category, layout=results_scroll, align="left")
                for _item, result_text, page, arguments in results:
                    result_button = Button(text=result_text, layout=results_scroll, align="left")
                    result_button.clicked.connect(
                        lambda checked=False, page=page, arguments=arguments: self.resultSelected.emit(page, arguments)
                    )
                    btn_width = result_button.sizeHint().width() + 10
                    width = btn_width if btn_width > width else width
            results_scroll.adjustSize()
            height = results_scroll.height()

        self.move(width=width, height=height)

    def clearSearch(self):
        self.search_box.clear()
        self.search_box.clearFocus()
        self.results_box.hide()


class PageArea(Box):
    filters = None
    backAvailable = Signal(bool)
    forwardAvailable = Signal(bool)

    def __init__(self, layout, updateSearchData):
        super().__init__(vertical=True, stretch=1, layout=layout)

        self.history = []
        self.current_index = -1
        self.current_page = None
        self.updateSearchData = updateSearchData

    def handleResize(self, width):
        if self.current_page and self.current_page.filters:
            self.current_page.filters_container.checkWidth(width)

    def loadPage(self):
        if self.current_page:
            self.current_page.hide()

        self.current_page = self.history[self.current_index]
        self.current_page.drawPage()
        self.current_page.show()
        self.backAvailable.emit(self.current_index > 0)
        self.forwardAvailable.emit(self.current_index < len(self.history) - 1)

        if self.current_page.filters:
            self.current_page.show()

        self.handleResize(self.current_page.window().width())

    def showPage(self, page_class, **kwargs):
        for page in self.history[self.current_index + 1 :]:
            page.deleteLater()

        self.history = self.history[: self.current_index + 1]
        new_page = page_class(layout=self, page_area=self, **kwargs)
        self.history.append(new_page)
        self.current_index += 1
        self.loadPage()

    def goBack(self):
        if self.current_index <= 0:
            return
        self.current_index -= 1
        self.loadPage()

    def goForward(self):
        if self.current_index >= len(self.history) - 1:
            return
        self.current_index += 1
        self.loadPage()

    def refreshPage(self):
        self.loadPage()


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

        header = Box(layout=self, variant="notification_header", height=32)
        title = Label(layout=header, text=title, stretch=1, align="left")
        close_btn = Button(layout=header, icon=close_icon, icon_size=(20, 20))
        close_btn.clicked.connect(self.deleteLater)

        if level == "SUCCESS":
            self.startTimer(3000)
        else:
            if record.error:
                content = Box(vertical=True, layout=self, spacing=7, margins=(0, 0, 0, 5))
                Label(text=record.error.message, layout=content)

                if level == "ERROR" and record.error.error_data:
                    for key, value in record.error.error_data.items():
                        key = key.replace("_", " ").title()
                        Label(text=f"{key}: {value}", layout=content)

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustSize()
        QTimer.singleShot(100, lambda: self.setFixedHeight(self.height()))

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
