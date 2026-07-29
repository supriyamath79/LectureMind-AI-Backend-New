"""SQLite connection management."""

import os
import sqlite3

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "lecturemind.db",
)


def get_connection():
    """Create a SQLite connection with row access by column name."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Create authentication tables and migrate lectures to user ownership."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        """
    )

    cursor.execute("PRAGMA table_info(lectures)")
    lecture_columns = [row["name"] for row in cursor.fetchall()]

    if "user_id" not in lecture_columns:
        cursor.execute("ALTER TABLE lectures ADD COLUMN user_id INTEGER")

    cursor.execute("SELECT COUNT(*) AS count FROM lectures WHERE user_id IS NULL")
    orphaned_lectures = cursor.fetchone()["count"]

    if orphaned_lectures:
        cursor.execute("SELECT id FROM users WHERE email = ?", ("legacy@lecturemind.local",))
        legacy_user = cursor.fetchone()

        if legacy_user is None:
            cursor.execute(
                """
                INSERT INTO users (full_name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (
                    "Legacy User",
                    "legacy@lecturemind.local",
                    "$2b$12$legacy.placeholder.hash.not.for.login",
                ),
            )
            legacy_user_id = cursor.lastrowid
        else:
            legacy_user_id = legacy_user["id"]

        cursor.execute(
            "UPDATE lectures SET user_id = ? WHERE user_id IS NULL",
            (legacy_user_id,),
        )

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_lectures_user_id ON lectures(user_id)"
    )

    conn.commit()
    conn.close()
