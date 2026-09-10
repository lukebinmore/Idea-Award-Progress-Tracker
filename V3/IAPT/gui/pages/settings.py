from IAPT.gui.components import Page, Box, Label, LineEdit
from IAPT.core.config import load_config, update_config


class SettingsPage(Page):
    page_title = "Settings"
    nav_btn_name = "settings_btn"

    def __init__(self, **kwargs):
        super().__init__(name="settings_page", **kwargs)

    @staticmethod
    def setting(config, section, key, layout):
        field = LineEdit(text=config[section][key], layout=layout)
        field.editingFinished.connect(lambda: update_config(config, section, key, field.text()))
        return field

    def drawPage(self):
        super().drawPage()

        config = load_config()

        self.page_header.setText(self.page_title)

        student_box = Box(vertical=True, layout=self.content, name="student_settings", spacing=5)
        Label(text="Student Excel File Settings", layout=student_box, variant="subheading")
        student_id = Box(vertical=True, layout=student_box, margins=(20, 0, 20, 0))
        Label(text="Candidate Number Coulmn:", layout=student_id)
        self.setting(config, "student_import", "student_id", student_id)
        first_name = Box(vertical=True, layout=student_box, margins=(20, 0, 20, 0))
        Label(text="First Name Coulmn:", layout=first_name)
        self.setting(config, "student_import", "first_name", first_name)
        last_name = Box(vertical=True, layout=student_box, margins=(20, 0, 20, 0))
        Label(text="Last Name Coulmn:", layout=last_name)
        self.setting(config, "student_import", "last_name", last_name)

        results_box = Box(vertical=True, layout=self.content, name="results_settings", spacing=5)
        Label(text="Idea Results Excel File Settings", layout=results_box, variant="subheading")
        student_id = Box(vertical=True, layout=results_box, margins=(20, 0, 20, 0))
        Label(text="Email Column:", layout=student_id)
        self.setting(config, "results_import", "student_id", student_id)
        bronze_points_total = Box(vertical=True, layout=results_box, margins=(20, 0, 20, 0))
        Label(text="Total Bronze Points Column:", layout=bronze_points_total)
        self.setting(config, "results_import", "bronze_points_total", bronze_points_total)
        bronze_citizen = Box(vertical=True, layout=results_box, margins=(20, 0, 20, 0))
        Label(text="Citizen Points Column:", layout=bronze_citizen)
        self.setting(config, "results_import", "bronze_citizen", bronze_citizen)
        bronze_worker = Box(vertical=True, layout=results_box, margins=(20, 0, 20, 0))
        Label(text="Worker Points Column:", layout=bronze_worker)
        self.setting(config, "results_import", "bronze_worker", bronze_worker)
        bronze_maker = Box(vertical=True, layout=results_box, margins=(20, 0, 20, 0))
        Label(text="Maker Points Column:", layout=bronze_maker)
        self.setting(config, "results_import", "bronze_maker", bronze_maker)
        bronze_entrepreneur = Box(vertical=True, layout=results_box, margins=(20, 0, 20, 0))
        Label(text="Entrepreneur Points Column:", layout=bronze_entrepreneur)
        self.setting(config, "results_import", "bronze_entrepreneur", bronze_entrepreneur)
        silver_points_total = Box(vertical=True, layout=results_box, margins=(20, 0, 20, 0))
        Label(text="Total Silver Points Column:", layout=silver_points_total)
        self.setting(config, "results_import", "silver_points_total", silver_points_total)
        badge_list = Box(vertical=True, layout=results_box, margins=(20, 0, 20, 0))
        Label(text="Badge List Column:", layout=badge_list)
        self.setting(config, "results_import", "badge_list", badge_list)

        schedule_box = Box(vertical=True, layout=self.content, name="schedule_settings", spacing=5)
        Label(text="Homework Schedule Excel File Settings", layout=schedule_box, variant="subheading")
        badge_name = Box(vertical=True, layout=schedule_box, margins=(20, 0, 20, 0))
        Label(text="Badge Name Column:", layout=badge_name)
        self.setting(config, "schedule_import", "badge_name", badge_name)
        category = Box(vertical=True, layout=schedule_box, margins=(20, 0, 20, 0))
        Label(text="Category Column:", layout=category)
        self.setting(config, "schedule_import", "category", category)
        points = Box(vertical=True, layout=schedule_box, margins=(20, 0, 20, 0))
        Label(text="Points Column:", layout=points)
        self.setting(config, "schedule_import", "points", points)
        due_date = Box(vertical=True, layout=schedule_box, margins=(20, 0, 20, 0))
        Label(text="Due Date Column:", layout=due_date)
        self.setting(config, "schedule_import", "due_date", due_date)
