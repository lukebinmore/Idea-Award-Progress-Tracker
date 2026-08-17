from pathlib import Path
from openpyxl import load_workbook
from IAPT.core.config import load_config


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


def import_students(file_path):
    config = load_config()["student_import"]

    data = read_excel_data(file_path, config.values())

    students = []
    for student in data:
        students.append(
            {
                "student_id": student[config["student_id"]],
                "first_name": student[config["first_name"]],
                "last_name": student[config["last_name"]],
            }
        )

    return students


import_students("C:\\Users\\lukeb\\Downloads\\students.xlsx")
