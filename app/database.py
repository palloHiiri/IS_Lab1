import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database.db"


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_db():
    with get_db() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.commit()


def get_user_by_username(username):
    with get_db() as connection:
        return connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()


def create_user(username, password_hash):
    with get_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )
        connection.commit()
        return cursor.lastrowid


def get_notes(user_id):
    with get_db() as connection:
        rows = connection.execute(
            "SELECT id, title, content FROM notes WHERE user_id = ?",
            (user_id,)
        ).fetchall()

        return [dict(row) for row in rows]


def create_note(user_id, title, content):
    with get_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO notes (user_id, title, content)
            VALUES (?, ?, ?)
            """,
            (user_id, title, content)
        )
        connection.commit()
        return cursor.lastrowid