# scripts/setup_db.py
import sqlite3

DB_NAME = "healthcare.db"

def reset_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    print("Dropping tables (if exist)...")
    cur.execute("DROP TABLE IF EXISTS fitness_data")
    cur.execute("DROP TABLE IF EXISTS medications")
    cur.execute("DROP TABLE IF EXISTS users")

    print("Recreating tables...")
    # Recreate using same schema as db_operations.create_tables
    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT,
        role TEXT,
        doctor_id INTEGER,
        patient_id INTEGER,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    cur.execute("""
    CREATE TABLE medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        med_name TEXT,
        schedule TEXT,
        notes TEXT,
        created_by INTEGER,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    cur.execute("""
    CREATE TABLE fitness_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bmi REAL,
        steps INTEGER,
        sleep REAL,
        calories INTEGER,
        heart_rate INTEGER,
        exercise REAL,
        bp INTEGER,
        date TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    conn.commit()
    conn.close()
    print("Reset complete.")

if __name__ == "__main__":
    reset_database()
