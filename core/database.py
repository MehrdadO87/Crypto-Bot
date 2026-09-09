import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
bot_db = BASE_DIR / "database.db"

def create_tables():
    conn = sqlite3.connect(bot_db, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            user_name TEXT,
            user_fname TEXT,
            user_lname TEXT,
            user_phone_number TEXT)""")

    conn.commit()
    conn.close()