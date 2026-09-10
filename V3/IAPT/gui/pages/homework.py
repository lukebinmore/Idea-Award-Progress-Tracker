from IAPT.gui.components import Page, Label, Box, LineEdit, NumberEdit, DateEdit, ComboBox
from IAPT.core.data import get_homeworks, updateHomework
from PySide6.QtCore import QDate
from datetime import date


class HomeworkPage(Page):
    page_title = "Homework"

    def __init__(self, id, **kwargs):
        super().__init__(name="homework_page", **kwargs)
        self.homework_id = id

    def saveHomeworkChange(self, homework, key, value):
        updateHomework(homework, key, value)
        self.drawPage()

    def drawPage(self):
        super().drawPage()

        homework = get_homeworks(self.homework_id)[0]
        self.page_header.setText(str(homework))

        info = Box(layout=self.content, vertical=True, name="homework_info", spacing=5, margins=(20, 0, 20, 0))
        badge_name_box = Box(vertical=True, layout=info)
        Label(text="Badge Name:", layout=badge_name_box)
        badge_name = LineEdit(text=homework.badge_name, layout=badge_name_box)
        badge_name.editingFinished.connect(lambda: self.saveHomeworkChange(homework, "badge_name", badge_name.text()))

        category_box = Box(vertical=True, layout=info)
        Label(text="Category:", layout=category_box)
        options = ["", "Citizen", "Maker", "Worker", "Entrepreneur"]
        category = ComboBox(options=options, default=homework.category, layout=category_box, align="center")
        category.currentIndexChanged.connect(
            lambda: self.saveHomeworkChange(homework, "category", category.currentData())
        )

        points_box = Box(vertical=True, layout=info)
        Label(text="Points", layout=points_box)
        points = NumberEdit(value=homework.points, layout=points_box)
        points.valueCommitted.connect(lambda: self.saveHomeworkChange(homework, "points", points.text()))

        due_date_box = Box(vertical=True, layout=info)
        Label(text="Account Found:", layout=due_date_box)
        today = date.today()
        september = QDate(today.year if today.month >= 9 else today.year - 1, 9, 1)
        due_date = DateEdit(minimum=september, value=homework.due_date, layout=due_date_box, align="center")
        due_date.dateChanged.connect(
            lambda value: self.saveHomeworkChange(homework, "due_date", value.toString("yyyy-MM-dd"))
        )
