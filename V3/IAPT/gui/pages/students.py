from IAPT.gui.components import Page, TableRow, Table
from IAPT.core.data import get_students
from IAPT.gui.styles.stylesheet import COLOURS
from PySide6.QtGui import QColor


class StudentsPage(Page):
    page_title = "Students"
    nav_btn_name = "students_btn"

    def __init__(self, **kwargs):
        super().__init__(name="students_page", **kwargs)

        columns = [
            ("ID", "id"),
            ("First Name", "firstname"),
            ("Last Name", "lastname"),
            ("Class", "classname"),
            ("Outstanding", "outstanding"),
            ("Late", "late"),
        ]

        self.student_table = Table(columns, layout=self, stretch=1, name="students_table")

        students = get_students()

        for student in students:
            row_colour = (
                COLOURS["silver"] if student.silver_awarded else COLOURS["bronze"] if student.bronze_awarded else None
            )
            row = TableRow(self.student_table, [attribute for name, attribute in columns], student, row_colour)

            if student.outstanding > 0 and not row_colour:
                self.student_table.item(row.summary_row, 4).setForeground(QColor(COLOURS["outstanding"]))

            if student.late > 0 and not row_colour:
                self.student_table.item(row.summary_row, 5).setForeground(QColor(COLOURS["late"]))

        self.student_table.sizeColumns()
