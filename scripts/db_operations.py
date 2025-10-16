import sqlite3

DB_NAME = "health_data.db"

# 1️⃣ Create tables
def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            med_name TEXT,
            schedule TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS fitness_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            steps INTEGER,
            calories INTEGER,
            heart_rate INTEGER,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# 2️⃣ Add medication
def add_medication(user_id, med_name, schedule):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO medications (user_id, med_name, schedule) VALUES (?, ?, ?)",
              (user_id, med_name, schedule))
    conn.commit()
    conn.close()

# 3️⃣ Add fitness data
def add_fitness_data(user_id, steps, calories, heart_rate, date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO fitness_data (user_id, steps, calories, heart_rate, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, steps, calories, heart_rate, date))
    conn.commit()
    conn.close()

# 4️⃣ Fetch medications
def fetch_medications():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT med_name, schedule FROM medications")
    rows = c.fetchall()
    conn.close()
    return rows

# 5️⃣ Fetch fitness data
def fetch_fitness():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT steps, calories, heart_rate FROM fitness_data ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return {"steps": row[0], "calories": row[1], "heart_rate": row[2]}
    else:
        return {"steps": 0, "calories": 0, "heart_rate": 0}
