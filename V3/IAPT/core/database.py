import sqlite3
from datetime import datetime
from IAPT.core.config import DATABASE_PATH
from IAPT.core.models import Student, Badge, Homework
from IAPT.core.exceptions import IAPTError
import logging

logger = logging.getLogger(__name__)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialise_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            class_name TEXT,
            active INTEGER NOT NULL DEFAULT 1,
            manual_disable INTEGER NOT NULL DEFAULT 0,
            account_found INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS points (
            student_id TEXT PRIMARY KEY,
            bronze_previous INTEGER NOT NULL DEFAULT 0,
            bronze_current INTEGER NOT NULL DEFAULT 0,
            bronze_citizen_previous INTEGER NOT NULL DEFAULT 0,
            bronze_citizen_current INTEGER NOT NULL DEFAULT 0,
            bronze_worker_previous INTEGER NOT NULL DEFAULT 0,
            bronze_worker_current INTEGER NOT NULL DEFAULT 0,
            bronze_maker_previous INTEGER NOT NULL DEFAULT 0,
            bronze_maker_current INTEGER NOT NULL DEFAULT 0,
            bronze_entrepreneur_previous INTEGER NOT NULL DEFAULT 0,
            bronze_entrepreneur_current INTEGER NOT NULL DEFAULT 0,
            silver_previous INTEGER NOT NULL DEFAULT 0,
            silver_current INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS badge_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            badge_name TEXT NOT NULL,
            completed_date DATE NOT NULL,
            UNIQUE(student_id, badge_name),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            badge_name TEXT,
            category TEXT,
            points INTEGER NOT NULL,
            due_date DATE NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS import_status (
            name TEXT PRIMARY KEY,
            last_week INTEGER NOT NULL DEFAULT 0,
            last_year INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def upsert_students(students, class_name):
    connection = None

    try:
        connection = get_connection()

        connection.execute("""UPDATE students SET active = 0 WHERE class_name = ?""", (class_name,))
        connection.executemany(
            """
            INSERT INTO students (
                student_id,
                first_name,
                last_name,
                class_name,
                active
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(student_id) DO UPDATE SET
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                class_name = excluded.class_name,
                active = excluded.active
            """,
            [
                (
                    student["student_id"],
                    student["first_name"],
                    student["last_name"],
                    class_name,
                    1,
                )
                for student in students
            ],
        )

        connection.commit()
    except Exception as error:
        raise IAPTError(message="Failed to update students table in database", error=error, student_count=len(students))
    finally:
        if connection:
            connection.close()


def set_student_disabled(student_id, state):
    connection = None

    try:
        connection = get_connection()
        connection.execute("""UPDATE students SET manual_disable = ? WHERE student_id = ?""", (state, student_id))
        connection.commit()
    except Exception as error:
        raise IAPTError(
            message="Failed to update disabled status in students table in database", error=error, student_id=student_id
        )
    finally:
        if connection:
            connection.close()


def upsert_results(results):
    connection = None

    try:
        connection = get_connection()

        current_date = datetime.now()
        current_week = current_date.isocalendar().week
        current_year = current_date.isocalendar().year

        status = connection.execute(
            """SELECT last_week, last_year FROM import_status WHERE name = ?""", ("results",)
        ).fetchone()

        is_new_week = status is None or status["last_week"] != current_week or status["last_year"] != current_year

        if is_new_week:
            connection.execute("""
                UPDATE points
                SET
                    bronze_previous = bronze_current,
                    bronze_citizen_previous = bronze_citizen_current,
                    bronze_worker_previous = bronze_worker_current,
                    bronze_maker_previous = bronze_maker_current,
                    bronze_entrepreneur_previous = bronze_entrepreneur_current,
                    silver_previous = silver_current
                """)

            connection.execute(
                """
                INSERT INTO import_status (name, last_week, last_year)
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    last_week = excluded.last_week,
                    last_year = excluded.last_year
                """,
                ("results", current_week, current_year),
            )

        connection.executemany(
            """
            INSERT INTO points (
                student_id,
                bronze_current,
                bronze_citizen_current,
                bronze_worker_current,
                bronze_maker_current,
                bronze_entrepreneur_current,
                silver_current
            )
            SELECT ?, ?, ?, ?, ?, ?, ?
            WHERE EXISTS (
                SELECT 1
                FROM students
                WHERE student_id = ?
            )
            ON CONFLICT(student_id) DO UPDATE SET
                bronze_current = excluded.bronze_current,
                bronze_citizen_current = excluded.bronze_citizen_current,
                bronze_worker_current = excluded.bronze_worker_current,
                bronze_maker_current = excluded.bronze_maker_current,
                bronze_entrepreneur_current = excluded.bronze_entrepreneur_current,
                silver_current = excluded.silver_current
            """,
            [
                (
                    result["student_id"],
                    result["bronze_points_total"],
                    result["bronze_citizen"],
                    result["bronze_worker"],
                    result["bronze_maker"],
                    result["bronze_entrepreneur"],
                    result["silver_points_total"] or 0,
                    result["student_id"],
                )
                for result in results
            ],
        )

        badges = [(result["student_id"], badge) for result in results for badge in result["badge_list"]]

        connection.executemany(
            """
            INSERT INTO badge_history (
                student_id,
                badge_name,
                completed_date
            )
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, badge_name) DO NOTHING
            """,
            [(student_id, badge, current_date.date()) for student_id, badge in badges],
        )

        connection.commit()
    except Exception as error:
        raise IAPTError(message="Failed to update results table in database", error=error, results_count=len(results))
    finally:
        if connection:
            connection.close()


def upsert_schedule(homeworks):
    connection = None

    try:
        connection = get_connection()
        connection.execute("""DELETE FROM schedule""")
        connection.executemany(
            """
            INSERT INTO schedule (
                badge_name,
                category,
                points,
                due_date
            )
            VALUES (?, ?, ?, ?)
            """,
            [(row["badge_name"], row["category"], row["points"], row["due_date"]) for row in homeworks],
        )

        connection.commit()
    except Exception as error:
        raise IAPTError(
            message="Failed to update schedule table in database", error=error, homework_count=len(homeworks)
        )
    finally:
        if connection:
            connection.close()


def read_students(student_ids=None):
    connection = None

    try:
        connection = get_connection()

        if student_ids is None:
            rows = connection.execute("""SELECT * FROM students WHERE active = 1""").fetchall()
        else:
            if isinstance(student_ids, str):
                student_ids = [student_ids]

            placeholders = ",".join("?" for _ in student_ids)

            rows = connection.execute(
                f"""SELECT * FROM students WHERE active = 1 AND student_id IN ({placeholders})""", student_ids
            ).fetchall()

        return [
            Student(
                id=row["student_id"],
                firstname=row["first_name"],
                lastname=row["last_name"],
                classname=row["class_name"],
                account_found=bool(row["account_found"]),
            )
            for row in rows
        ]

    except Exception as error:
        raise IAPTError(message="Failed to read students table in database", error=error, student_ids=student_ids)

    finally:
        if connection:
            connection.close()


def read_points(students):
    connection = None

    try:
        connection = get_connection()
        student_ids = [student.id for student in students]

        if not student_ids:
            return students

        placeholders = ",".join("?" for _ in student_ids)
        rows = connection.execute(
            f"""SELECT * FROM points WHERE student_id IN ({placeholders})""", student_ids
        ).fetchall()

        points_by_student = {row["student_id"]: row for row in rows}

        for student in students:
            row = points_by_student.get(student.id)

            if row:
                student.bronze_previous = row["bronze_previous"]
                student.bronze_current = row["bronze_current"]
                student.bronze_citizen_previous = row["bronze_citizen_previous"]
                student.bronze_citizen_current = row["bronze_citizen_current"]
                student.bronze_worker_previous = row["bronze_worker_previous"]
                student.bronze_worker_current = row["bronze_worker_current"]
                student.bronze_maker_previous = row["bronze_maker_previous"]
                student.bronze_maker_current = row["bronze_maker_current"]
                student.bronze_entrepreneur_previous = row["bronze_entrepreneur_previous"]
                student.bronze_entrepreneur_current = row["bronze_entrepreneur_current"]
                student.silver_previous = row["silver_previous"]
                student.silver_current = row["silver_current"]

        return students

    except Exception as error:
        raise IAPTError(message="Failed to read points table in database", error=error, student_count=len(students))

    finally:
        if connection:
            connection.close()


def read_badges(students):
    connection = None

    try:
        connection = get_connection()
        student_ids = [student.id for student in students]
        placeholders = ",".join("?" for _ in student_ids)

        rows = connection.execute(
            f"""SELECT * FROM badge_history WHERE student_id IN ({placeholders})""", student_ids
        ).fetchall()

        students_by_id = {student.id: student for student in students}

        for row in rows:
            badge = Badge(
                name=row["badge_name"], completed_date=datetime.strptime(row["completed_date"], "%Y-%m-%d").date()
            )
            students_by_id[row["student_id"]].badges.append(badge)

        return students

    except Exception as error:
        raise IAPTError(message="Failed to read badges table in database", error=error, student_count=len(students))

    finally:
        if connection:
            connection.close()


def read_homeworks():
    connection = None

    try:
        connection = get_connection()
        rows = connection.execute("""SELECT * FROM schedule """).fetchall()

        return [
            Homework(
                badge_name=row["badge_name"],
                category=row["category"],
                points=row["points"],
                due_date=datetime.strptime(row["due_date"], "%Y-%m-%d").date(),
            )
            for row in rows
        ]

    except Exception as error:
        raise IAPTError(message="Failed to read schedule table in database", error=error)

    finally:
        if connection:
            connection.close()


def read_class_names():
    connection = None

    try:
        connection = get_connection()
        rows = connection.execute(
            """SELECT DISTINCT class_name FROM students WHERE class_name IS NOT NULL ORDER BY class_name"""
        ).fetchall()

        return [row["class_name"] for row in rows]

    except Exception as error:
        raise IAPTError(message="Failed to read students table in database", error=error)
    finally:
        if connection:
            connection.close()
