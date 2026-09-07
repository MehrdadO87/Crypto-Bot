import sqlite3


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# users
cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE NOT NULL, user_name TEXT, user_fname TEXT, user_lname TEXT, user_phone_number TEXT)")




conn.commit()
conn.close()