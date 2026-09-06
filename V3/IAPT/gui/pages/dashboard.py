from IAPT.gui.components import Page


class DashboardPage(Page):
    page_title = "Dashboard"

    def __init__(self, **kwargs):
        super().__init__(name="dashboard_page", **kwargs)

    def drawPage(self):
        super().drawPage()

        self.page_header.setText(self.page_title)
