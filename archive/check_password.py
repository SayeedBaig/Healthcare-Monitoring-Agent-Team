# check_password.py
from sqlalchemy import create_engine, text
import os
import bcrypt

DB = os.getenv("DATABASE_URL", "sqlite:///./health_data.db")
# for sqlite URL -> path
if DB.startswith("sqlite:///"):
    db_path = DB.replace("sqlite:///", "")
else:
    db_path = "./health_data.db"

import sqlite3
conn = sqlite3.connect(db_path)
cur = conn.cursor()
email = input("Email to check (exact): ").strip().lower()
pwd = input("Plain password to test: ").strip()
cur.execute("SELECT password_hash FROM users WHERE lower(email)=?", (email,))
row = cur.fetchone()
if not row:
    print("User not found.")
else:
    stored = row[0]
    ok = bcrypt.checkpw(pwd.encode("utf-8"), stored.encode("utf-8"))
    print("Password match:", ok)
conn.close()
