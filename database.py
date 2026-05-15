import sqlite3

conn = sqlite3.connect("tasks.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    priority TEXT NOT NULL,
    completed INTEGER DEFAULT 0
)
""")

conn.commit()

conn.close()

print("Database created successfully!")
