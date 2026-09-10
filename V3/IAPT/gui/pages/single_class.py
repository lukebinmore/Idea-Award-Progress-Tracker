from IAPT.gui.components import Page, Table, Box, Label
from IAPT.core.data import get_classes, get_students
from IAPT.gui.filters import setDefaultSort, drawFilters, applyFilters, applySort
from IAPT.gui.pages.student import StudentPage
from IAPT.gui.styles.stylesheet import COLOURS
from PySide6.QtGui import QColor


class ClassPage(Page):
    page_title = "Class"
    filters = True

    def __init__(self, id, **kwargs):
        super().__init__(name="class_page", **kwargs)
        self.classname = id

        self.columns = [
            ("ID", "id"),
            ("First Name", "firstname"),
            ("Last Name", "lastname"),
            ("Class", "classname"),
            ("Outstanding", "outstanding"),
            ("Late", "late"),
        ]

        self.filter_list = [
            "outstanding",
            "late",
            "awards",
            "disabled",
            "on_roll",
            "no_account",
        ]

    def drawPage(self):
        super().drawPage()

        group = get_classes(self.classname)[0]

        students = [s for s in get_students() if s.classname == group.name]
        self.state = setDefaultSort(self.state, self.columns[2])
        drawFilters(self.columns, self.filter_list, self.filters, self.state, self.drawPage)
        students = applyFilters(students, self.state)
        students = applySort(students, self.state)

        self.page_header.setText(f"{group.name} - {len(students)} Results")

        summary_box = Box(vertical=True, layout=self.content, name="summary_box", spacing=10)
        Label(text="Class Overview", layout=summary_box, variant="subheading")
        summary = Box(layout=summary_box, margins=(10, 0, 10, 0), spacing=10)
        Label(text=f"Missing\n{group.outstanding_count}", layout=summary, variant="missing_total")
        Label(text=f"Late\n{group.late_count}", layout=summary, variant="late_total")
        Label(text=f"Completed\n{group.completed_count}", layout=summary, variant="completed_total")

        self.student_table = Table(
            self.columns, StudentPage, self.page_area, layout=self.content, stretch=1, name="students_table"
        )
        for student in students:
            row_colour = self.getRowColour(student)
            row = self.student_table.addItem(student, self.getRowColour(student))

            if student.outstanding > 0 and not row_colour:
                self.student_table.item(row, 4).setForeground(QColor(COLOURS["outstanding"]))

            if student.late > 0 and not row_colour:
                self.student_table.item(row, 5).setForeground(QColor(COLOURS["late"]))

        self.student_table.sizeColumns()

    def getRowColour(self, student):
        row_colour = COLOURS["bronze"] if student.bronze_awarded else None
        row_colour = COLOURS["silver"] if student.silver_awarded else row_colour
        row_colour = COLOURS["missing"] if not student.account_found else row_colour
        return row_colour
