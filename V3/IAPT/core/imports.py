from openpyxl import load_workbook
from IAPT.core.config import load_config
from IAPT.core.database import upsert_students, upsert_results, upsert_schedule, initialise_database


def read_excel_data(file_path, headers):
    workbook = load_workbook(file_path, read_only=True, data_only=True)
    worksheet = workbook.active
    rows = list(worksheet.iter_rows(values_only=True))
    workbook.close()

    spreadsheet_headers = rows[0]
    indexes = []

    for header in headers:
        if header not in spreadsheet_headers:
            raise ValueError(f"Required Column {header} was not found in the spreadsheet.")

        indexes.append(spreadsheet_headers.index(header))

    data = []
    for row in rows[1:]:
        data.append({header: row[index] for header, index in zip(headers, indexes)})

    return data


def import_students(file_path, class_name):
    config = load_config()["student_import"]
    data = read_excel_data(file_path, config.values())

    students = []
    for student in data:
        if not student[config["student_id"]]:
            continue

        students.append(
            {
                "student_id": student[config["student_id"]],
                "first_name": student[config["first_name"]],
                "last_name": student[config["last_name"]],
            }
        )

    upsert_students(students, class_name)


def import_results(file_path):
    config = load_config()["results_import"]
    data = read_excel_data(file_path, config.values())

    results = []
    for row in data:
        if row[config["badge_list"]]:
            row[config["badge_list"]] = row[config["badge_list"]].split(",")

        results.append(
            {
                "student_id": row[config["student_id"]].split("@")[0],
                "bronze_points_total": row[config["bronze_points_total"]] or 0,
                "bronze_citizen": row[config["bronze_citizen"]] or 0,
                "bronze_worker": row[config["bronze_worker"]] or 0,
                "bronze_maker": row[config["bronze_maker"]] or 0,
                "bronze_entrepreneur": row[config["bronze_entrepreneur"]] or 0,
                "silver_points_total": row[config["silver_points_total"]] or 0,
                "badge_list": row[config["badge_list"]] or [],
            }
        )

    upsert_results(results)


def import_schedule(file_path):
    config = load_config()["schedule_import"]
    data = read_excel_data(file_path, config.values())

    homeworks = []
    for homework in data:
        homework[config["due_date"]] = homework[config["due_date"]].date()
        homeworks.append(
            {
                "badge_name": homework[config["badge_name"]] or "",
                "category": homework[config["category"]] or "",
                "points": homework[config["points"]],
                "due_date": homework[config["due_date"]],
            }
        )

    upsert_schedule(homeworks)


initialise_database()
import_students("C:\\Users\\lukeb\\Downloads\\students.xlsx", "9X-It1")
import_results("C:\\Users\\lukeb\\Downloads\\test.xlsx")
import_schedule("C:\\Users\\lukeb\\Downloads\\homework.xlsx")
