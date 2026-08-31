from IAPT.gui.components import Page, TableRow, Table, Label, Box
from IAPT.core.data import get_students
from IAPT.gui.styles.stylesheet import COLOURS
from IAPT.gui.filters import drawFilters, applySort, setDefaultSort, applyFilters
from PySide6.QtGui import QColor


class StudentsPage(Page):
    page_title = "Students"
    nav_btn_name = "students_btn"
    filters = True

    def __init__(self, **kwargs):
        super().__init__(name="students_page", **kwargs)

        self.columns = [
            ("ID", "id"),
            ("First Name", "firstname"),
            ("Last Name", "lastname"),
            ("Class", "classname"),
            ("Outstanding", "outstanding"),
            ("Late", "late"),
        ]

        self.filter_list = [
            "classname",
            "outstanding",
            "non_outstanding",
            "late",
            "non_late",
            "no_awards",
            "bronze_awarded",
            "silver_awarded",
            "no_account",
        ]

    def drawPage(self):
        super().drawPage()

        students = get_students()
        self.state = setDefaultSort(self.state, self.columns[2])
        self.controls = drawFilters(self.columns, self.filter_list, self.filters, self.state, self.drawPage)
        students = applyFilters(students, self.state)
        students = applySort(students, self.state)

        self.page_header.setText(f"{self.page_title} - {len(students)} Results")

        if students:
            self.student_table = Table(self.columns, layout=self.content, stretch=1, name="students_table")
            for student in students:
                row_colour = self.getRowColour(student)
                row = TableRow(self.student_table, [attribute for name, attribute in self.columns], student, row_colour)

                if student.outstanding > 0 and not row_colour:
                    self.student_table.item(row.summary_row, 4).setForeground(QColor(COLOURS["outstanding"]))

                if student.late > 0 and not row_colour:
                    self.student_table.item(row.summary_row, 5).setForeground(QColor(COLOURS["late"]))

            self.student_table.sizeColumns()
        else:
            Label(text="No Data Found", layout=self.content)

    def getRowColour(self, student):
        row_colour = COLOURS["bronze"] if student.bronze_awarded else None
        row_colour = COLOURS["silver"] if student.silver_awarded else row_colour
        row_colour = COLOURS["missing"] if not student.account_found else row_colour
        return row_colour
