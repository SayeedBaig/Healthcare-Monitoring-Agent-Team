import sqlite3
from pathlib import Path

print("➡ create_medicine_db.py starting...")

# Project root: .../Healthcare-Monitoring-Agent-Team
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "medicines.db"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"

print("BASE_DIR :", BASE_DIR)
print("DB_PATH  :", DB_PATH)
print("SCHEMA   :", SCHEMA_PATH)


def init_db():
    print("➡ init_db() called")

    # 1) connect / create DB file
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print("✔ Connected to DB")

    # 2) run schema.sql to create tables
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        sql = f.read()
        print("✔ Loaded schema.sql")
        cur.executescript(sql)
        print("✔ Executed schema.sql")

    # 3) insert sample medicines
    medicines = [
        ("Paracetamol", "Fever, mild pain",
         "Nausea, rash (rare liver damage in overdose)",
         "Avoid overdose, caution in liver disease"),
        ("Ibuprofen", "Pain, inflammation",
         "Stomach pain, acidity",
         "Avoid in kidney disease, gastric ulcer, late pregnancy"),
        ("Azithromycin", "Bacterial infections",
         "Nausea, loose motion",
         "Avoid self-medication, complete full course"),
        ("Cetirizine", "Allergy, cold",
         "Drowsiness, dry mouth",
         "Avoid driving if drowsy"),
        ("Metformin", "Type-2 diabetes",
         "Nausea, stomach upset",
         "Take with food; caution in kidney disease"),
        ("Pantoprazole", "Acidity, reflux",
         "Headache, gas",
         "Short-term use unless doctor advises"),
        ("Aspirin", "Pain, heart protection (low dose)",
         "Stomach irritation, bleeding",
         "Avoid in kids with viral fever; caution with blood thinners"),
        ("Dolo 650", "Fever, pain",
         "Same as paracetamol",
         "Do not exceed 3–4 tablets/day without doctor"),
        ("Amoxicillin", "Bacterial infections",
         "Rash, loose motion",
         "Check allergy history; complete course"),
        ("ORS", "Dehydration",
         "Usually safe",
         "Use correct powder-to-water ratio"),
    ]

    cur.executemany(
        "INSERT OR IGNORE INTO medicines (name, use_case, side_effects, precautions) "
        "VALUES (?, ?, ?, ?)",
        medicines,
    )
    print("✔ Inserted medicines")

    # 4) insert sample interactions
    interactions = [
        ("Aspirin", "Ibuprofen",
         "Both can irritate stomach and increase bleeding risk."),
        ("Aspirin", "Paracetamol",
         "Occasional combined use is usually safe; long-term combo only under doctor advice."),
        ("Metformin", "Azithromycin",
         "Generally okay, but sugars may fluctuate; monitor as advised by doctor."),
    ]

    cur.executemany(
        "INSERT INTO interactions (medicine1, medicine2, description) VALUES (?, ?, ?)",
        interactions,
    )
    print("✔ Inserted interactions")

    conn.commit()
    conn.close()
    print("✅ medicines.db created/updated at:", DB_PATH)


if __name__ == "__main__":
    init_db()
