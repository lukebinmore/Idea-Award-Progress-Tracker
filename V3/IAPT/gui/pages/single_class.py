from IAPT.gui.components import Page


class ClassPage(Page):
    page_title = "Class"

    def __init__(self, **kwargs):
        super().__init__(name="class_page", **kwargs)

    def drawPage(self):
        super().drawPage()

        self.page_header.setText(self.page_title)
