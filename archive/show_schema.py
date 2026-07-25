import sqlite3

conn = sqlite3.connect("health_data.db")
cursor = conn.cursor()

cursor.execute("SELECT sql FROM sqlite_master WHERE name='users'")
schema = cursor.fetchone()

print("\nUsers table schema:\n")
print(schema[0] if schema else "❌ No users table found")

conn.close()
