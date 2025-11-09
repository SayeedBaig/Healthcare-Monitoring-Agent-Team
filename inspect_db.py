# inspect_db.py
import sqlite3
conn = sqlite3.connect("health_data.db")
cur = conn.cursor()

print("Tables:")
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(" -", row[0])

print("\nRow counts:")
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    name = row[0]
    cnt = cur.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f" - {name}: {cnt} rows")

print("\nUsers schema:")
sch = cur.execute("SELECT sql FROM sqlite_master WHERE name='users'").fetchone()
print(sch[0] if sch else "No users table found")

conn.close()
