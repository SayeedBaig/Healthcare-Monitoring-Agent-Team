# show_users.py
import sqlite3
conn = sqlite3.connect("health_data.db")
cur = conn.cursor()
rows = list(cur.execute("SELECT id, name, email, role FROM users"))
if not rows:
    print("No users found.")
else:
    for r in rows:
        print(r)
conn.close()
