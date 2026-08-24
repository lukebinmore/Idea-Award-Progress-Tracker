from IAPT.gui.components import Page, Button


class ImportPage(Page):
    page_title = "Import Options"
    nav_btn_name = "imports_btn"

    def __init__(self):
        super().__init__(name="imports_page")

        import_results_btn = Button(text="Import Weekly Results", layout=self)
        import_schedule_btn = Button(text="Import Homework Schedule", layout=self)
        import_students_btn = Button(text="Import Students", layout=self)
