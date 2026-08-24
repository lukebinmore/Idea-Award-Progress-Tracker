from IAPT.core.database import read_students, read_points, read_badges, read_homeworks
from IAPT.core.calculations import (
    calculate_badge_homeworks,
    calculate_homework_quantities,
    calculate_points_homeworks,
    calculate_award_status,
)


def get_students(student_ids=None):
    students = read_students(student_ids)
    students = read_points(students)
    students = read_badges(students)
    homeworks = read_homeworks()

    students = calculate_badge_homeworks(students, homeworks)
    students = calculate_points_homeworks(students, homeworks)
    students = calculate_homework_quantities(students)
    students = calculate_award_status(students)

    return students
