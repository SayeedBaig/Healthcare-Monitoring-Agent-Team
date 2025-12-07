# scripts/migrate_passwords.py
import sqlite3
import bcrypt

DB_NAME = "healthcare.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Add the new column password_hash if it doesn't exist
cur.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cur.fetchall()]
if "password_hash" not in columns:
    cur.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    print("Added column password_hash")

# Fetch existing users
cur.execute("SELECT id, password FROM users")
users = cur.fetchall()

for user_id, plain_pwd in users:
    if plain_pwd:  # only if password exists
        hashed = bcrypt.hashpw(plain_pwd.encode(), bcrypt.gensalt())
        cur.execute("UPDATE users SET password_hash=? WHERE id=?", (hashed.decode(), user_id))
        print(f"User {user_id} password hashed")

conn.commit()
conn.close()
print("Migration completed!")
