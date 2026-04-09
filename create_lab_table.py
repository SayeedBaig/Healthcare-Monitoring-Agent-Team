"""
create_lab_table.py
-------------------
Run this ONCE to create the lab_reports table.
 
    python create_lab_table.py
 
Never run again after that — CREATE TABLE IF NOT EXISTS makes it safe,
but it's just not needed.
"""
 
import sqlite3
 
DB_NAME = "healthcare.db"   # must match db_operations.py
 
 
def create_lab_reports_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lab_reports (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id               INTEGER NOT NULL,
 
            -- ── Shared / overlapping columns ──────────────────────
            -- Diabetes uses: Age, SBP, DBP, BUN
            -- CKD      uses: age_years, systolic_bp, diastolic_bp, bun_mgdl
            age                   INTEGER DEFAULT 0,   -- Age / age_years
            sbp                   INTEGER DEFAULT 0,   -- SBP  / systolic_bp
            dbp                   INTEGER DEFAULT 0,   -- DBP  / diastolic_bp
            bun                   REAL    DEFAULT 0.0, -- BUN  / bun_mgdl
 
            -- ── Diabetes-only columns ─────────────────────────────
            gender                INTEGER DEFAULT 1,   -- 1=Male 2=Female
            bmi                   REAL    DEFAULT 0.0,
            fpg                   REAL    DEFAULT 0.0,
            ffpg                  REAL    DEFAULT 0.0,
            chol                  REAL    DEFAULT 0.0,
            tri                   REAL    DEFAULT 0.0,
            hdl                   REAL    DEFAULT 0.0,
            ldl                   REAL    DEFAULT 0.0,
            alt                   REAL    DEFAULT 0.0,
            ccr                   REAL    DEFAULT 0.0,
 
            -- ── CKD-only columns ──────────────────────────────────
            sex                   INTEGER DEFAULT 1,   -- 1=Male 2=Female
            serum_creatinine      REAL    DEFAULT 0.0, -- mg/dL
            uacr                  REAL    DEFAULT 0.0, -- mg/g
            hemoglobin            REAL    DEFAULT 0.0, -- g/dL
            potassium             REAL    DEFAULT 0.0, -- mEq/L
            phosphate             REAL    DEFAULT 0.0, -- mg/dL
            calcium               REAL    DEFAULT 0.0, -- mg/dL
            hba1c                 REAL    DEFAULT 0.0, -- %
 
            date                  TEXT    DEFAULT '',
 
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅  lab_reports table created (or already exists) in '{DB_NAME}'")
 
 
if __name__ == "__main__":
    create_lab_reports_table()