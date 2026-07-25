# migrate_users_table.py (safe version)
import sqlite3, os

print("🔄 Starting safe migration...")

DB = "health_data.db"
bak = DB + ".bak"
if not os.path.exists(bak):
    print(f"Creating backup {bak} ...")
    open(bak, "wb").write(open(DB, "rb").read())
else:
    print(f"Backup {bak} already exists.")

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Check users_old exists; if not, we must have just renamed earlier or table absent
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_old';")
if not cur.fetchone():
    # if users_old doesn't exist but users exists with old schema, rename now
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if not cur.fetchone():
        print("ERROR: No users table found to migrate.")
        conn.close()
        raise SystemExit(1)
    print("Renaming users -> users_old")
    cur.execute("ALTER TABLE users RENAME TO users_old;")

# Inspect columns in users_old
cur.execute("PRAGMA table_info(users_old);")
cols = [c[1] for c in cur.fetchall()]
print("users_old columns:", cols)

# Create new users table
print("Creating new users table with required columns...")
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'patient'
);
""")

# Build INSERT depending on available columns in users_old
# If users_old has only id and name, set email = name and placeholder password
placeholder = "migrated_placeholder_hash"

if "email" in cols and "password_hash" in cols:
    print("Migrating id,name,email,password_hash -> role='patient'")
    cur.execute("""
    INSERT INTO users (id, name, email, password_hash, role)
    SELECT id, name, email, password_hash, 'patient' FROM users_old;
    """)
elif "name" in cols and "id" in cols:
    print("Migrating id,name -> set email = name, password_hash = placeholder, role='patient'")
    cur.execute("""
    INSERT INTO users (id, name, email, password_hash, role)
    SELECT id, name, name, ?, 'patient' FROM users_old;
    """, (placeholder,))
else:
    # fallback: try selecting whatever exists and fill defaults
    print("Unexpected schema in users_old; copying name if present, else aborting.")
    if "name" in cols:
        cur.execute("""
        INSERT INTO users (name, email, password_hash, role)
        SELECT name, name, ?, 'patient' FROM users_old;
        """, (placeholder,))
    else:
        print("Cannot migrate: no usable columns found in users_old.")
        conn.close()
        raise SystemExit(1)

# Drop old table
print("Dropping users_old...")
cur.execute("DROP TABLE users_old;")

conn.commit()
conn.close()
print("✅ Migration finished. New users table created.")
