from IAPT.gui.components import Page


class LatestPage(Page):
    page_title = "Latest Homework"
    nav_btn_name = "latest_btn"

    def __init__(self, **kwargs):
        super().__init__(name="latest_page", **kwargs)

    def drawPage(self):
        super().drawPage()

        self.page_header.setText(self.page_title)
