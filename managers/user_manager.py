"""Repository-style data access for users."""

from database.database import get_connection


def create_user(full_name, email, password_hash):
    """Create a user and return its id."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (full_name, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (full_name, email.lower(), password_hash),
    )

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return user_id


def get_user_by_email(email):
    """Fetch a user by email."""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower(),))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Fetch a user by id."""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_last_login(user_id):
    """Record the latest login timestamp."""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
        (user_id,),
    )
    conn.commit()
    conn.close()
