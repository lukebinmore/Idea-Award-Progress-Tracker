from IAPT.gui.components import Page, TableRow, Table
from IAPT.core.data import get_students


class StudentsPage(Page):
    page_title = "Students"
    nav_btn_name = "students_btn"

    def __init__(self):
        super().__init__(name="students_page")

        columns = [
            ("ID", "id"),
            ("First Name", "firstname"),
            ("Last Name", "lastname"),
            ("Class", "classname"),
            ("Outstanding", "outstanding"),
            ("Late", "late"),
        ]

        self.student_table = Table(columns, layout=self, stretch=1, name="students_table", variant="list")

        students = get_students()

        for student in students:
            TableRow(self.student_table, [attribute for name, attribute in columns], student)

        self.student_table.sizeColumns()
