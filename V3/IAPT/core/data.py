from IAPT.core.database import read_students, read_points, read_badges, read_homeworks, update_student
from IAPT.core.calculations import (
    calculate_badge_homeworks,
    calculate_homework_quantities,
    calculate_points_homeworks,
    calculate_award_status,
    calculate_class_stats,
)
from IAPT.core.models import Class
from IAPT.core.exceptions import IAPTError
from IAPT.core.config import load_config
import logging

logger = logging.getLogger(__name__)


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


def get_classnames(names=None):
    students = get_students()
    classes = sorted({student.classname for student in students if student.classname}, key=str.casefold)
    if not names:
        return classes

    if isinstance(names, str):
        names = [names]

    return [o for o in classes if o in names]


def get_classes(names=None):
    students = get_students()
    classes = [Class(name=o) for o in get_classnames(names)]
    classes = calculate_class_stats(students, classes)
    return classes


def get_homeworks(homework_ids=None):
    return read_homeworks(homework_ids)


def updateStudent(student, key, value):
    try:
        if getattr(student, key) != value:
            setattr(student, key, value)
            update_student(student)
            logger.success("Student updated")
    except IAPTError as error:
        logger.error("Student update failed", extra={"error": error})


def get_categories():
    return ["Citizen", "Maker", "Worker", "Entrepreneur"]
