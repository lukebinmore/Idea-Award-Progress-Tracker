import sqlite3
from datetime import datetime
from IAPT.core.config import DATABASE_PATH


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
    connection = get_connection()

    connection.execute(
        """
        UPDATE students
        SET active = 0
        WHERE class_name = ?
        """,
        (class_name,),
    )

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
    connection.close()


def set_student_disabled(student_id, state):
    connection = get_connection()

    connection.execute(
        """
        UPDATE students
        SET manual_disable = ?
        WHERE student_id = ?
        """,
        (state, student_id),
    )

    connection.commit()
    connection.close()


def upsert_results(results):
    connection = get_connection()

    current_date = datetime.now()
    current_week = current_date.isocalendar().week
    current_year = current_date.isocalendar().year

    status = connection.execute(
        """
        SELECT last_week, last_year
        FROM import_status
        WHERE name = ?
        """,
        ("results",),
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
    connection.close()


def upsert_schedule(homeworks):
    connection = get_connection()

    connection.execute("""
        DELETE FROM schedule
        """)

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
    connection.close()


if __name__ == "__main__":
    initialise_database()
