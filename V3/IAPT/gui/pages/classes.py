from IAPT.gui.components import Page, Table, Label, ProgressBar, Button, Box, LineEdit, CheckBox
from IAPT.core.data import get_classes
from IAPT.gui.pages.single_class import ClassPage
from IAPT.gui.styles.stylesheet import COLOURS
from PySide6.QtGui import QColor
from IAPT.gui.filters import drawFilters, setDefaultSort, applySort


class ClassesPage(Page):
    page_title = "Classes"
    nav_btn_name = "classes_btn"
    filters = True

    def __init__(self, **kwargs):
        super().__init__(name="classes_page", **kwargs)

        self.columns = [
            ("Class", "name"),
            ("Students", "student_count"),
            ("Outstanding", "outstanding_count"),
            ("Late", "late_count"),
            ("Completed", "completed_count"),
        ]
        self.filter_list = []

    def drawPage(self):
        super().drawPage()

        classes = get_classes()
        self.page_header.setText(f"{self.page_title} - {len(classes)} Results")

        drawFilters(self.columns, self.filter_list, self.filters, self.state, self.drawPage)
        self.state = setDefaultSort(self.state, self.columns[0])
        classes = applySort(classes, self.state)

        classes_table = Table(self.columns, ClassPage, self.page_area, layout=self.content)
        for group in classes:
            row = classes_table.addItem(group)
            if group.outstanding_count > 0:
                classes_table.item(row, 2).setForeground(QColor(COLOURS["outstanding"]))

            if group.late_count > 0:
                classes_table.item(row, 3).setForeground(QColor(COLOURS["late"]))

            if group.completed_count > 0:
                classes_table.item(row, 4).setForeground(QColor(COLOURS["completed"]))
