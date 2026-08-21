from PySide6.QtWidgets import (
    QMainWindow,
)
from IAPT.gui.components import Box, Header, Footer, Navigation, Search, Filters, PageArea
from IAPT.gui.pages.students import StudentsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IAPT")

        # Main Base
        base = Box(vertical=True, name="base")
        self.setCentralWidget(base)

        # Header
        header = Header(base)

        # Search
        search = Search(base)

        # Body
        body = Box(layout=base, name="body")

        # Navigation
        navigation = Navigation(body)

        # Main Page Content
        page_area = PageArea(body)

        # Filters
        filters = Filters(body)

        # Footer
        Footer(base)

        # Signal Connections
        header.back_button.clicked.connect(page_area.goBack)
        page_area.backAvailable.connect(header.back_button.setEnabled)
        header.forward_button.clicked.connect(page_area.goForward)
        page_area.forwardAvailable.connect(header.forward_button.setEnabled)

        page_area.showPage(StudentsPage)
        page_area.showPage(StudentsPage)
        page_area.showPage(StudentsPage)
        page_area.showPage(StudentsPage)
        page_area.showPage(StudentsPage)
        page_area.showPage(StudentsPage)
