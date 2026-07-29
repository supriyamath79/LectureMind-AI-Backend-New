"""Repository-style data access for lectures."""

from database.database import get_connection


def add_lecture(
    user_id,
    title,
    video_path,
    transcript_path,
    ocr_path,
    merged_path,
    embedding_path,
    faiss_path,
):
    """Insert a processed lecture and return its database id."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO lectures
        (
            title,
            video_path,
            transcript_path,
            ocr_path,
            merged_path,
            embedding_path,
            faiss_path,
            user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            video_path,
            transcript_path,
            ocr_path,
            merged_path,
            embedding_path,
            faiss_path,
            user_id,
        ),
    )

    conn.commit()
    lecture_id = cursor.lastrowid
    conn.close()

    return lecture_id


def get_lecture(lecture_id):
    """Fetch one lecture by id."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM lectures WHERE id = ?",
        (lecture_id,),
    )

    lecture = cursor.fetchone()
    conn.close()

    return lecture


def get_lecture_for_user(lecture_id, user_id):
    """Fetch one lecture owned by a user."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM lectures WHERE id = ? AND user_id = ?",
        (lecture_id, user_id),
    )

    lecture = cursor.fetchone()
    conn.close()

    return lecture


def get_all_lectures(user_id=None):
    """Fetch lectures ordered from newest to oldest, optionally scoped by user."""

    conn = get_connection()
    cursor = conn.cursor()

    if user_id is None:
        cursor.execute(
            """
            SELECT
                id,
                title,
                created_at
            FROM lectures
            ORDER BY created_at DESC
            """
        )
    else:
        cursor.execute(
            """
            SELECT
                id,
                title,
                created_at
            FROM lectures
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )

    lectures = cursor.fetchall()
    conn.close()

    return lectures


def delete_lecture(lecture_id, user_id=None):
    """Delete one lecture by id, optionally scoped by user."""

    conn = get_connection()
    cursor = conn.cursor()

    if user_id is None:
        cursor.execute(
            "DELETE FROM lectures WHERE id = ?",
            (lecture_id,),
        )
    else:
        cursor.execute(
            "DELETE FROM lectures WHERE id = ? AND user_id = ?",
            (lecture_id, user_id),
        )

    conn.commit()
    conn.close()
