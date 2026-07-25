import sqlite3
from backend.seed_users import hash_password  # if error, we'll replace this after

conn = sqlite3.connect("health_data.db")
cur = conn.cursor()

# 1. Delete all current users (including placeholder)
cur.execute("DELETE FROM users;")

# 2. Insert fresh correct users
users = [
    ("Patient One", "patient@example.com", "patient123", "patient"),
    ("Doctor One", "doctor@example.com", "doctor123", "doctor"),
    ("Caregiver One", "caregiver@example.com", "caregiver123", "caregiver"),
]

for name, email, pwd, role in users:
    hashed = hash_password(pwd)  # bcrypt hash
    cur.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
        (name, email, hashed, role),
    )

conn.commit()
conn.close()
print("✅ Users reset & seeded")
