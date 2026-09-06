from IAPT.gui.components import Page, Table
from IAPT.core.data import get_homeworks
from IAPT.gui.filters import setDefaultSort, applySort, drawFilters, applyFilters
from IAPT.gui.pages.homework import HomeworkPage
from IAPT.gui.styles.stylesheet import COLOURS


class SchedulePage(Page):
    page_title = "Schedule"
    nav_btn_name = "schedule_btn"
    filters = True

    def __init__(self, **kwargs):
        super().__init__(name="schedule_page", **kwargs)

        self.columns = [
            ("Homework ID", "id"),
            ("Badge Name", "badge_name"),
            ("Category", "category"),
            ("Points", "points"),
            ("Due Date", "due_date"),
        ]

        self.filter_list = ["category", "points", "due_date"]

    def drawPage(self):
        super().drawPage()

        homeworks = get_homeworks()
        self.state = setDefaultSort(self.state, self.columns[4])
        drawFilters(self.columns[1:], self.filter_list, self.filters, self.state, self.drawPage)
        homeworks = applyFilters(homeworks, self.state)
        homeworks = applySort(homeworks, self.state)

        self.page_header.setText(f"{self.page_title} - {len(homeworks)} Results")

        homeworks_table = Table(self.columns, HomeworkPage, self.page_area, layout=self.content)
        homeworks_table.hideColumn(0)
        for homework in homeworks:
            row_colour = COLOURS.get(homework.category.lower(), None)
            homeworks_table.addItem(homework, row_colour)
