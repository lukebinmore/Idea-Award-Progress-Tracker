from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal
from IAPT.gui.components import Box, Header, Footer, Navigation, Search, Filters, PageArea, NotificationArea
from IAPT.gui.page_registry import NAV_PAGES
from IAPT.gui.pages.students import StudentsPage


class MainWindow(QMainWindow):
    widthChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IAPT")

        # Main Base
        base = Box(vertical=True, name="base")
        self.setCentralWidget(base)

        # Notification Area
        self.notifications = NotificationArea(self)

        # Header
        header = Header(layout=base)

        # Body
        body = Box(layout=base, name="body")

        # Navigation
        navigation = Navigation(layout=body, pages=NAV_PAGES)

        # Content Divider
        content = Box(vertical=True, layout=body, name="content")

        # Search
        search = Search(layout=content)

        main_content = Box(layout=content, name="main_content")

        # Main Page Content
        page_area = PageArea(layout=main_content)

        # Filters
        filters = Filters(layout=main_content)

        # Footer
        Footer(layout=base)

        header.back_button.clicked.connect(page_area.goBack)
        page_area.backAvailable.connect(header.back_button.setEnabled)
        header.forward_button.clicked.connect(page_area.goForward)
        page_area.forwardAvailable.connect(header.forward_button.setEnabled)

        navigation.pageSelected.connect(page_area.showPage)
        self.widthChanged.connect(navigation.checkWidth)

        self.widthChanged.connect(filters.checkWidth)

        page_area.showPage(StudentsPage)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.widthChanged.emit(self.width())
        self.notifications.updateGeometry()
