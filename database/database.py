import sqlite3
from pathlib import Path

# Database file location
DB_PATH = Path("database/lecturemind.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            video_path TEXT,
            transcript_path TEXT,
            ocr_path TEXT,
            merged_path TEXT,
            embedding_path TEXT,
            faiss_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")