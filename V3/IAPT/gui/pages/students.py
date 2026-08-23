from IAPT.core.models import Student
from IAPT.gui.components import Page, TableRow, Table


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

        students = [
            Student(
                id="001",
                firstname="John-asd-asddasd-asdasd-asasd",
                lastname="Smith",
                classname="8A",
                outstanding=2,
                late=0,
            ),
            Student(id="002", firstname="Sarah", lastname="Jones", classname="8A", outstanding=0, late=1),
            Student(id="003", firstname="Michael", lastname="Brown", classname="8B", outstanding=4, late=2),
        ]

        for student in students:
            TableRow(self.student_table, [attribute for name, attribute in columns], student)

        self.student_table.sizeColumns()
