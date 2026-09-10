from IAPT.gui.components import Page, Box, Label, Table, Button
from IAPT.core.data import get_latest_homeworks, get_students
from IAPT.gui.pages.homework import HomeworkPage
from IAPT.gui.pages.student import StudentPage
from IAPT.gui.filters import drawFilters, setDefaultSort, applySort, applyFilters


class LatestPage(Page):
    page_title = "Latest Homework"
    nav_btn_name = "latest_btn"
    filters = True

    def __init__(self, **kwargs):
        super().__init__(name="latest_page", **kwargs)

        self.columns = [("ID", "id"), ("First Name", "firstname"), ("Last Name", "lastname"), ("Class", "classname")]

        self.filter_list = ["classname_selector"]

    def drawPage(self):
        super().drawPage()

        self.page_header.setText(self.page_title)
        latest_hws = get_latest_homeworks()
        students = get_students()
        self.state = setDefaultSort(self.state, self.columns[2])
        drawFilters(self.columns, self.filter_list, self.filters, self.state, self.drawPage)
        students = applySort(students, self.state)
        students = applyFilters(students, self.state)

        if not latest_hws:
            Label(text="No Homework Data Found", layout=self.content)
            return

        if not students:
            Label(text="No Student Data Found", layout=self.content)
            return

        missing_students = [o for o in students if any(h in o.missing_homeworks for h in latest_hws)]
        missing_students = [o for o in missing_students if not o.bronze_awarded or not o.silver_awarded]
        late_students = [o for o in students if all(h in o.late_homeworks for h in latest_hws)]
        late_students = [o for o in late_students if not o.bronze_awarded or not o.silver_awarded]
        completed_students = [o for o in students if all(h in o.completed_homeworks for h in latest_hws)]
        completed_students = [o for o in completed_students if not o.bronze_awarded or not o.silver_awarded]
        awarded_students = [o for o in students if o.bronze_awarded or o.silver_awarded]

        homework_list = Box(vertical=True, layout=self.content, spacing=5)
        Label(text="Homeworks", layout=homework_list, variant="subheading")
        for homework in latest_hws:
            btn = Button(text=str(homework), layout=homework_list, variant=homework.category)
            btn.clicked.connect(lambda checked=False, id=homework.id: self.page_area.showPage(HomeworkPage, id=id))

        if len(missing_students) > 0:
            missing_box = Box(vertical=True, layout=self.content, name="missing_homeworks")
            Label(text=f"Missing - {len(missing_students)} Results", layout=missing_box, variant="subheading_red")
            missing_table = Table(self.columns, StudentPage, self.page_area, layout=missing_box, fit_height=True)
            for student in missing_students:
                missing_table.addItem(student)

        if len(late_students) > 0:
            late_box = Box(vertical=True, layout=self.content, name="late_homeworks")
            Label(text=f"Late - {len(late_students)} Results", layout=late_box, variant="subheading_yellow")
            late_table = Table(self.columns, StudentPage, self.page_area, layout=late_box, fit_height=True)
            for student in late_students:
                late_table.addItem(student)

        if len(completed_students) > 0:
            completed_box = Box(vertical=True, layout=self.content, name="completed_homeworks")
            Label(
                text=f"Completed - {len(completed_students)} Results", layout=completed_box, variant="subheading_green"
            )
            completed_table = Table(self.columns, StudentPage, self.page_area, layout=completed_box, fit_height=True)
            for student in completed_students:
                completed_table.addItem(student)

        if len(awarded_students) > 0:
            awarded_box = Box(vertical=True, layout=self.content, name="awarded_homeworks")
            Label(text=f"Award Earned - {len(awarded_students)} Results", layout=awarded_box, variant="subheading")
            awarded_table = Table(self.columns, StudentPage, self.page_area, layout=awarded_box, fit_height=True)
            for student in awarded_students:
                awarded_table.addItem(student)
