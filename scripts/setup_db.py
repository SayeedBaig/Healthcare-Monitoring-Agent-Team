import sqlite3

DB_NAME = "health_data.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Create tables
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

# Insert mock user
c.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (1, "Test User"))

# Insert mock medications
medications = [
    (1, "Paracetamol 500mg", "Morning & Night"),
    (1, "Vitamin D3", "Once a day"),
    (1, "Amoxicillin 250mg", "Morning")
]
c.executemany("INSERT INTO medications (user_id, med_name, schedule) VALUES (?, ?, ?)", medications)

# Insert mock fitness data
fitness = (1, 8421, 320, 78, "2025-10-16")
c.execute("INSERT INTO fitness_data (user_id, steps, calories, heart_rate, date) VALUES (?, ?, ?, ?, ?)", fitness)

conn.commit()
conn.close()

print("✅ Database created and mock data inserted!")
