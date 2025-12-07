from db_operations import get_connection

def insert_mock_data():
    conn = get_connection()
    cur = conn.cursor()

    # ---- USERS ----
    # Doctor
    cur.execute("""
        INSERT INTO users (name, email, password, role, doctor_id, patient_id)
        VALUES ('Dr. John', 'drjohn@example.com', 'pass123', 'doctor', NULL, NULL)
    """)
    doctor_id = cur.lastrowid

    # Patient
    cur.execute("""
        INSERT INTO users (name, email, password, role, doctor_id, patient_id)
        VALUES ('Patient One', 'patient1@example.com', 'pass123', 'patient', ?, NULL)
    """, (doctor_id,))
    patient_id = cur.lastrowid

    # Caregiver
    cur.execute("""
        INSERT INTO users (name, email, password, role, doctor_id, patient_id)
        VALUES ('Caregiver One', 'care@example.com', 'pass123', 'caregiver', NULL, ?)
    """, (patient_id,))

    # ---- MEDICATION EXAMPLE ----
    cur.execute("""
        INSERT INTO medications (patient_id, medicine_name, schedule)
        VALUES (?, 'Paracetamol', 'Morning & Night')
    """, (patient_id,))

    # ---- FITNESS EXAMPLE ----
    cur.execute("""
        INSERT INTO fitness_data (user_id, bmi, steps, sleep, calories, heart_rate, exercise, bp, date)
        VALUES (?, 24.5, 5000, 7.5, 300, 78, 2, 120, '2024-12-01')
    """, (patient_id,))

    conn.commit()
    conn.close()

    print("Mock data inserted successfully!")
