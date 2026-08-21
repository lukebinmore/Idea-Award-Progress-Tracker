from IAPT.gui.components import Box, Label


class StudentsPage(Box):
    page_title = "Students"
    nav_btn_name = "students_btn"

    def __init__(self):
        super().__init__(vertical=True, name="students_page", align="top")

        Label(text=self.page_title, layout=self, variant="page_title")
