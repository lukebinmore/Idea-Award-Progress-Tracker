from IAPT.gui.components import Page, Button, ExpandingButton, LineEdit, Label
from IAPT.core.imports import import_results, import_schedule, import_students
from IAPT.core.database import read_class_names
from PySide6.QtWidgets import QFileDialog
from pathlib import Path


class ImportPage(Page):
    page_title = "Import Data"
    nav_btn_name = "imports_btn"

    def __init__(self, **kwargs):
        super().__init__(name="imports_page", **kwargs)

    def drawPage(self):
        super().drawPage()

        self.page_header.setText(self.page_title)

        self.results_btn = Button(text="Import Weekly Results", layout=self.content, name="import_results_btn")
        self.results_btn.clicked.connect(self.importResults)

        self.schedule_btn = Button(text="Import Homework Schedule", layout=self.content, name="import_schedule_btn")
        self.schedule_btn.clicked.connect(self.importSchedule)

        self.students = ExpandingButton(
            text="Import Students", layout=self.content, name="import_students_btn", vertical=True
        )
        self.students.content.setMargins(0, 5, 0, 5)
        self.students.content.setSpacing(15)
        Label(text="Please enter the class name:", layout=self.students.content)
        self.students_class = LineEdit(suggestions=read_class_names(), layout=self.students.content)
        self.students_class.textChanged.connect(self.updateStudentsBtn)
        self.students_btn = Button(text="import Students", layout=self.students.content, enabled=False)
        self.students_btn.clicked.connect(self.importStudents)

    def selectExcelFile(self, file_type):
        downloads = Path.home() / "Downloads"
        file_path, _ = QFileDialog.getOpenFileName(
            self, f"Select {file_type} file", str(downloads), "Excel Files (*.xlsx *.xls)"
        )
        if not file_path:
            return None
        return file_path

    def importResults(self):
        file_path = self.selectExcelFile("results")

        if not file_path:
            return

        import_results(file_path)
        self.drawPage()

    def importSchedule(self):
        file_path = self.selectExcelFile("schedule")

        if not file_path:
            return

        import_schedule(file_path)
        self.drawPage()

    def updateStudentsBtn(self, text):
        self.students_btn.setEnabled(bool(text.strip()))

    def importStudents(self):
        file_path = self.selectExcelFile("students")

        if not file_path:
            return

        class_name = self.students_class.text().strip()
        import_students(file_path, class_name)
        self.drawPage()
