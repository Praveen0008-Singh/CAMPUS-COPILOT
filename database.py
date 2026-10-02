import sqlite3

DB_NAME = "campus_copilot.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            complaint TEXT,
            category TEXT,
            location TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def add_complaint(name, complaint, category, location, priority):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints
        (name, complaint, category, location, priority, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        complaint,
        category,
        location,
        priority,
        "Pending"
    ))

    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return ticket_id


def get_complaints():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, complaint, category,
               location, priority, status
        FROM complaints
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data