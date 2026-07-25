# finalize_migration.py
import sqlite3

DB = "health_data.db"
placeholder = "migrated_placeholder_hash"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# counts
cur.execute("SELECT COUNT(*) FROM users")
users_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM users_old")
old_count = cur.fetchone()[0]
print(f"Before: users rows = {users_count}, users_old rows = {old_count}")

# fetch rows from users_old
cur.execute("SELECT id, name FROM users_old")
rows = cur.fetchall()
inserted = 0
for r in rows:
    oid, name = r
    email = name  # use name as fallback email
    # check if a user with same email already exists
    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        print(f"Skipping {email}: already exists in users")
        continue
    # try to preserve id if possible; otherwise let SQLite assign new id
    try:
        cur.execute(
            "INSERT INTO users (id, name, email, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            (oid, name, email, placeholder, "patient")
        )
    except sqlite3.IntegrityError:
        # fallback: insert without id to avoid conflict
        cur.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name, email, placeholder, "patient")
        )
    inserted += 1
    print(f"Inserted user from old row id={oid} name={name}")

# drop users_old
if old_count > 0:
    cur.execute("DROP TABLE IF EXISTS users_old")
    print("Dropped users_old table")

conn.commit()
cur.execute("SELECT COUNT(*) FROM users")
print("After: users rows =", cur.fetchone()[0])
conn.close()
print("Done.")
