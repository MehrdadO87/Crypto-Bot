import sqlite3
import os
import sqlite3
from core.database import bot_db



def connect_to_db():
    conn = sqlite3.connect(bot_db, timeout=10)
    cursor = conn.cursor()
    return conn, cursor


def insert_user(user_id, user_name, user_fname, user_lname):
    conn = sqlite3.connect(bot_db, timeout=10)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users(user_id, user_name, user_fname, user_lname) VALUES(?,?,?,?)", (user_id, user_name, user_fname, user_lname))
        conn.commit()
    finally:
        conn.close()

def update_phone(user_id, user_phone_number):
    conn = sqlite3.connect(bot_db, timeout=10)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET user_phone_number = ? WHERE user_id = ?",(user_phone_number, user_id))
        conn.commit()
    finally:
        conn.close()


def get_user(user_id):
    conn, cursor = connect_to_db()
    try:
        cursor.execute("SELECT user_id, user_name, user_fname, user_lname, user_phone_number FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        return user
    finally:
        conn.close()
        

def get_user_phone(user_id):
    conn, cursor = connect_to_db()
    try:
        cursor.execute("SELECT user_phone_number FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.commit()
        return result[0] if result else None
    finally:
        conn.close()

def delete_user(user_id):
    conn = sqlite3.connect(bot_db)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()