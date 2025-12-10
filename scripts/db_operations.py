
import sqlite3
from typing import Optional, List, Dict, Any

DB_NAME = "healthcare.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            doctor_id INTEGER,
            patient_id INTEGER
        )
    """)
    # Add other tables (medications, fitness, etc.)
    conn.commit()
    conn.close()

def add_user(name, email, phone, password_hash, role, doctor_id=None, patient_id=None):
    """
    Add a user. Password must already be hashed with bcrypt before passing in.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, email, phone, password_hash, role, doctor_id, patient_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, phone, password_hash, role, doctor_id, patient_id))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

def get_user_by_email(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, email, password_hash, role, doctor_id, patient_id FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "password_hash": row[3],
            "role": row[4],
            "doctor_id": row[5],
            "patient_id": row[6]
        }
    return None

def get_user_by_id(user_id: int) -> Optional[Dict[str,Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, phone, role, doctor_id, patient_id FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "phone": row[3],
        "role": row[4],
        "doctor_id": row[5],
        "patient_id": row[6]
    }

def fetch_patients_of_doctor(doctor_user_id: int) -> List[Dict[str,Any]]:
    """
    Returns list of patients assigned to the given doctor id.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, phone FROM users WHERE role = 'patient' AND doctor_id = ?", (doctor_user_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2], "phone": r[3]} for r in rows]


# -------------------- Medication functions --------------------

def add_medication(user_id: int, med_name: str, schedule: str, created_by: Optional[int]=None, notes: str=""):
    """
    Add medication record for patient user_id.
    created_by should normally be doctor's user_id.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO medications (user_id, med_name, schedule, notes, created_by)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, med_name, schedule, notes, created_by))
    conn.commit()
    conn.close()

def update_medication(med_id: int, med_name: str, schedule: str, notes: str="", edited_by: Optional[int]=None) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE medications
        SET med_name = ?, schedule = ?, notes = ?, created_by = ?
        WHERE id = ?
    """, (med_name, schedule, notes, edited_by, med_id))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed > 0

def delete_medication(med_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM medications WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()

def fetch_medications(user_id: int, requester_id: Optional[int]=None, requester_role: Optional[str]=None):
    """
    Return medication rows for a patient user_id.
    requester_id and role are optional; the calling UI can check permissions.
    Returns list of tuples (med_name, schedule, notes, id, created_by)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT med_name, schedule, notes, id, created_by FROM medications
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_user_and_related(user_id: int):
    """
    Deletes a user and related rows in a safe way.
    Only touches tables we know about in this file:
      - medications (user_id)
      - fitness_data (user_id)
      - goals (user_id)  [optional]
      - users (id)
    Any missing table/column is silently ignored.
    """
    conn = get_connection()      
    cur = conn.cursor()

    def safe_delete(sql, params):
        try:
            cur.execute(sql, params)
            conn.commit()
        except sqlite3.OperationalError:
            pass   

    # Delete medications belonging to this user
    safe_delete("DELETE FROM medications WHERE user_id = ?", (user_id,))

    # Delete fitness data
    safe_delete("DELETE FROM fitness_data WHERE user_id = ?", (user_id,))

    # Delete goals if exists
    safe_delete("DELETE FROM goals WHERE user_id = ?", (user_id,))

    # Finally delete main user record
    safe_delete("DELETE FROM users WHERE id = ?", (user_id,))

    conn.close()


# -------------------- Fitness functions --------------------

def add_fitness_data(user_id: int, bmi: float, steps: int, sleep: float, calories: int,
                     heart_rate: int, exercise: float, bp: int, date: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO fitness_data (user_id, bmi, steps, sleep, calories, heart_rate, exercise, bp, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, bmi, steps, sleep, calories, heart_rate, exercise, bp, date))
    conn.commit()
    conn.close()

def update_latest_fitness(user_id: int, bmi: float, steps: int, sleep: float, calories: int,
                          heart_rate: int, exercise: float, bp: int, date: str) -> bool:
    """
    Update the latest fitness_data record for the user. If none exists, create a new one.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM fitness_data WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    row = cur.fetchone()
    if row:
        fid = row[0]
        cur.execute("""
            UPDATE fitness_data
            SET bmi=?, steps=?, sleep=?, calories=?, heart_rate=?, exercise=?, bp=?, date=?
            WHERE id=?
        """, (bmi, steps, sleep, calories, heart_rate, exercise, bp, date, fid))
        changed = cur.rowcount
        conn.commit()
        conn.close()
        return changed > 0
    else:
        conn.commit()
        conn.close()
        add_fitness_data(user_id, bmi, steps, sleep, calories, heart_rate, exercise, bp, date)
        return True

def fetch_fitness(user_id: int) -> Dict[str, Any]:
    """
    Return the latest fitness metric for the given user_id as a dict.
    If none found, return zeros/defaults.
    Keep same return keys as app expects.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT bmi, steps, sleep, calories, heart_rate, exercise, bp, date
        FROM fitness_data
        WHERE user_id = ?
        ORDER BY id DESC LIMIT 1
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {
            "bmi": 0.0, "steps": 0, "sleep": 0.0, "calories": 0,
            "heart_rate": 0, "exercise": 0.0, "bp": 0, "date": ""
        }
    return {
        "bmi": row[0] or 0.0,
        "steps": row[1] or 0,
        "sleep": row[2] or 0.0,
        "calories": row[3] or 0,
        "heart_rate": row[4] or 0,
        "exercise": row[5] or 0.0,
        "bp": row[6] or 0,
        "date": row[7] or ""
    }
