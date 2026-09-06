from IAPT.gui.components import Page, Label, ProgressBar, Button
from IAPT.core.data import get_homeworks


class HomeworkPage(Page):
    page_title = "Homework"

    def __init__(self, id, **kwargs):
        super().__init__(name="student_page", **kwargs)
        self.homework_id = id

    def drawPage(self):
        super().drawPage()

        homework = get_homeworks(self.homework_id)[0]
        self.page_header.setText(f"{homework.badge_name} - {homework.due_date}")
