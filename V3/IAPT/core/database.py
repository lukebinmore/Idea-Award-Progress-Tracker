import sqlite3
from IAPT.core.config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialise_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            class_name TEXT,
            active INTEGER NOT NULL DEFAULT 1,
            account_found INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS points (
            student_id INTEGER PRIMARY KEY,
            bronze_previous INTEGER NOT NULL DEFAULT 0,
            bronze_current INTEGER NOT NULL DEFAULT 0,
            bronze_citizen INTEGER NOT NULL DEFAULT 0,
            bronze_worker INTEGER NOT NULL DEFAULT 0,
            bronze_maker INTEGER NOT NULL DEFAULT 0,
            bronze_entrepreneur INTEGER NOT NULL DEFAULT 0,
            bronze_other INTEGER NOT NULL DEFAULT 0,
            silver_previous INTEGER NOT NULL DEFAULT 0,
            silver_current INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS badge_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            badge_name TEXT NOT NULL,
            completed_date DATE NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            badge_name TEXT,
            points INTEGER NOT NULL,
            category TEXT,
            due_date DATE NOT NULL
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialise_database()
