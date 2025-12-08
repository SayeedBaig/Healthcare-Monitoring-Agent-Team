import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "medicines.db"


def get_medicine_info(name):
    if not name:
        return None

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT name, use_case, side_effects, precautions "
        "FROM medicines WHERE LOWER(name)=LOWER(?)",
        (name,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "name": row[0],
        "use_case": row[1],
        "side_effects": row[2],
        "precautions": row[3],
    }


def check_interaction(med1, med2):
    if not med1 or not med2:
        return None

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT description FROM interactions
        WHERE (LOWER(medicine1)=LOWER(?) AND LOWER(medicine2)=LOWER(?))
           OR (LOWER(medicine1)=LOWER(?) AND LOWER(medicine2)=LOWER(?))
        """,
        (med1, med2, med2, med1),
    )

    row = cur.fetchone()
    conn.close()

    if row:
        return row[0]
    return None
