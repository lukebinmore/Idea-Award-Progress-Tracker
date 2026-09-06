from IAPT.gui.components import Page, Label, ProgressBar, Button, Box, LineEdit, CheckBox
from IAPT.core.data import get_students, updateStudent
from IAPT.gui.pages.homework import HomeworkPage


class StudentPage(Page):
    page_title = "Student"

    def __init__(self, id, **kwargs):
        super().__init__(name="student_page", **kwargs)
        self.student_id = id

    def drawPage(self):
        super().drawPage()

        student = get_students(self.student_id)[0]
        self.page_header.setText(f"{student.firstname} {student.lastname}")

        info = Box(layout=self.content, vertical=True, name="student_info", spacing=5, margins=(20, 0, 20, 0))
        id = Box(vertical=True, layout=info)
        Label(text="Candidate Number:", layout=id)
        LineEdit(read_only=True, text=student.id, layout=id)
        firstname_box = Box(vertical=True, layout=info)
        Label(text="First Name:", layout=firstname_box)
        firstname = LineEdit(text=student.firstname, layout=firstname_box)
        firstname.editingFinished.connect(lambda: updateStudent(student, "firstname", firstname.text()))
        lastname_box = Box(vertical=True, layout=info)
        Label(text="Last Name:", layout=lastname_box)
        lastname = LineEdit(text=student.lastname, layout=lastname_box)
        lastname.editingFinished.connect(lambda: updateStudent(student, "lastname", lastname.text()))
        classname_box = Box(vertical=True, layout=info)
        Label(text="Class:", layout=classname_box)
        classname = LineEdit(text=student.classname, layout=classname_box)
        classname.editingFinished.connect(lambda: updateStudent(student, "classname", classname.text()))
        account_box = Box(vertical=True, layout=info)
        Label(text="Account Found:", layout=account_box)
        CheckBox(read_only=True, layout=account_box, box_only=True, default=student.account_found)
        on_roll_box = Box(vertical=True, layout=info)
        Label(text="On Roll:", layout=on_roll_box)
        on_roll = CheckBox(layout=on_roll_box, box_only=True, default=student.on_roll)
        on_roll.stateChanged.connect(lambda state: updateStudent(student, "on_roll", bool(state)))
        disabled_box = Box(vertical=True, layout=info)
        Label(text="Disabled:", layout=disabled_box)
        disabled = CheckBox(layout=disabled_box, box_only=True, default=student.disabled)
        disabled.stateChanged.connect(lambda state: updateStudent(student, "disabled", bool(state)))

        award_progress = Box(layout=self.content, name="award_progress")
        bronze_award = Box(layout=award_progress, vertical=True, spacing=5)
        Label(text=f"Bronze Progress - {student.bronze_current} points", layout=bronze_award, variant="subheading")
        ProgressBar(range=(0, 250), start_value=student.bronze_current, layout=bronze_award, variant="bronze_progress")
        silver_award = Box(layout=award_progress, vertical=True, spacing=5)
        Label(text=f"Silver Progress - {student.silver_current} points", layout=silver_award, variant="subheading")
        ProgressBar(range=(0, 300), start_value=student.silver_current, layout=silver_award, variant="silver_progress")

        category_progress = Box(vertical=True, layout=self.content, name="category_progress", spacing=5)
        Label(text="Bronze Category Progress", layout=category_progress, variant="subheading")
        Label(
            text=f"{student.bronze_current - student.bronze_previous} points earned this week",
            layout=category_progress,
            name="weekly_points",
        )
        category_box = Box(grid=True, align="center", layout=category_progress, margins=(10, 0, 10, 0), spacing=10)
        citizen = Box(
            vertical=True, layout=category_box, position=(0, 0), margins=(10, 10, 10, 10), variant="subheading_citizen"
        )
        Label(text=f"Citizen\n{student.bronze_citizen_current} points", layout=citizen)
        maker = Box(
            vertical=True, layout=category_box, position=(0, 1), margins=(10, 10, 10, 10), variant="subheading_maker"
        )
        Label(text=f"Maker\n{student.bronze_maker_current} points", layout=maker)
        worker = Box(
            vertical=True, layout=category_box, position=(1, 0), margins=(10, 10, 10, 10), variant="subheading_worker"
        )
        Label(text=f"Worker\n{student.bronze_worker_current} points", layout=worker)

        entrepreneur = Box(
            vertical=True,
            layout=category_box,
            position=(1, 1),
            margins=(10, 10, 10, 10),
            variant="subheading_entrepreneur",
        )
        Label(text=f"Entrepreneur\n{student.bronze_entrepreneur_current} points", layout=entrepreneur)

        badge_list = Box(vertical=True, layout=self.content, spacing=5, name="badge_list")
        Label(text=f"Missing Homeworks - {len(student.missing_homeworks)}", layout=badge_list, variant="subheading_red")
        for badge in student.missing_homeworks:
            btn = Button(text=str(badge), layout=badge_list, variant=badge.category)
            btn.clicked.connect(
                lambda checked=False, homework_id=badge.id: self.page_area.showPage(HomeworkPage, id=homework_id)
            )

        Label(text=f"Late Homeworks - {len(student.late_homeworks)}", layout=badge_list, variant="subheading_yellow")
        for badge in student.late_homeworks:
            btn = Button(text=str(badge), layout=badge_list, variant=badge.category)
            btn.clicked.connect(
                lambda checked=False, homework_id=badge.id: self.page_area.showPage(HomeworkPage, id=homework_id)
            )

        Label(
            text=f"Completed Homeworks - {len(student.completed_homeworks)}",
            layout=badge_list,
            variant="subheading_green",
        )
        for badge in student.completed_homeworks:
            btn = Button(text=str(badge), layout=badge_list, variant=badge.category)
            btn.clicked.connect(
                lambda checked=False, homework_id=badge.id: self.page_area.showPage(HomeworkPage, id=homework_id)
            )
