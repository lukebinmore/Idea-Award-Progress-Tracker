from IAPT.gui.components import Page


class StudentsPage(Page):
    page_title = "Students"
    nav_btn_name = "students_btn"

    def __init__(self):
        super().__init__(name="students_page")
