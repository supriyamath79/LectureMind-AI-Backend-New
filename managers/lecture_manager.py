from database.database import get_connection


def add_lecture(
    title,
    video_path,
    transcript_path,
    ocr_path,
    merged_path,
    embedding_path,
    faiss_path,
):
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
            faiss_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            video_path,
            transcript_path,
            ocr_path,
            merged_path,
            embedding_path,
            faiss_path,
        ),
    )

    conn.commit()
    lecture_id = cursor.lastrowid
    conn.close()

    return lecture_id

def get_lecture(lecture_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM lectures WHERE id = ?",
        (lecture_id,)
    )

    lecture = cursor.fetchone()

    conn.close()

    return lecture
def get_all_lectures():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            created_at
        FROM lectures
        ORDER BY created_at DESC
    """)

    lectures = cursor.fetchall()

    conn.close()

    return lectures


def delete_lecture(lecture_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM lectures WHERE id = ?",
        (lecture_id,)
    )

    conn.commit()
    conn.close()