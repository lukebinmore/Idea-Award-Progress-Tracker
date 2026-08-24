from datetime import date


def calculate_badge_homeworks(students, homeworks):
    badge_homeworks = [homework for homework in homeworks if homework.badge_name]

    for homework in badge_homeworks:
        if homework.due_date > date.today():
            continue

        for student in students:
            completed_badge = next((badge for badge in student.badges if badge.name == homework.badge_name), None)

            if completed_badge is None:
                student.missing_homeworks.append(homework)
            elif completed_badge.completed_date <= homework.due_date:
                student.completed_homeworks.append(homework)
                student.points_from_homeworks += homework.points
            else:
                student.late_homeworks.append(homework)
                student.points_from_homeworks += homework.points

    return students


def calculate_points_homeworks(students, homeworks):
    points_homeworks = [homework for homework in homeworks if not homework.badge_name]

    for homework in points_homeworks:
        if homework.due_date > date.today():
            continue

        for student in students:
            points_available = student.bronze_current - student.points_from_homeworks

            if points_available >= homework.points:
                student.completed_homeworks.append(homework)
                student.points_from_homeworks += homework.points
            else:
                student.missing_homeworks.append(homework)

    return students


def calculate_homework_quantities(students):
    for student in students:
        student.complete = len(student.completed_homeworks)
        student.late = len(student.late_homeworks)
        student.outstanding = len(student.missing_homeworks)

    return students


def calculate_award_status(students):
    for student in students:
        student.bronze_awarded = student.bronze_current >= 250
        student.silver_awarded = student.silver_current >= 300

    return students
