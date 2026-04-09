"""
scripts/db_lab_operations.py
-----------------------------
fetch_lab_report  — mirrors fetch_fitness()
save_lab_report   — mirrors update_latest_fitness()
"""
 
from typing import Any, Dict
from scripts.db_operations import get_connection
 
 
# All keys + safe defaults (zero / first-option)
_DEFAULTS: Dict[str, Any] = {
    # shared
    "age":              0,
    "sbp":              0,
    "dbp":              0,
    "bun":              0.0,
    # diabetes-only
    "gender":           1,
    "bmi":              0.0,
    "fpg":              0.0,
    "ffpg":             0.0,
    "chol":             0.0,
    "tri":              0.0,
    "hdl":              0.0,
    "ldl":              0.0,
    "alt":              0.0,
    "ccr":              0.0,
    # ckd-only
    "sex":              1,
    "serum_creatinine": 0.0,
    "uacr":             0.0,
    "hemoglobin":       0.0,
    "potassium":        0.0,
    "phosphate":        0.0,
    "calcium":          0.0,
    "hba1c":            0.0,
    # meta
    "date":             "",
}
 
_COLUMNS = [
    "age", "sbp", "dbp", "bun",
    "gender", "bmi", "fpg", "ffpg", "chol", "tri", "hdl", "ldl", "alt", "ccr",
    "sex", "serum_creatinine", "uacr", "hemoglobin",
    "potassium", "phosphate", "calcium", "hba1c",
    "date",
]
 
 
def fetch_lab_report(user_id: int) -> Dict[str, Any]:
    """
    Return the latest lab report row as a dict.
    Falls back to _DEFAULTS for any NULL / missing values.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT {', '.join(_COLUMNS)}
        FROM lab_reports
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
 
    if not row:
        return dict(_DEFAULTS)
 
    return {
        k: (row[i] if row[i] is not None else _DEFAULTS[k])
        for i, k in enumerate(_COLUMNS)
    }
 
 
def save_lab_report(user_id: int, data: Dict[str, Any]) -> None:
    """
    Update the existing row if one exists, otherwise insert.
    Mirrors update_latest_fitness — one live row per patient.
    """
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute(
        "SELECT id FROM lab_reports WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,)
    )
    existing = cur.fetchone()
 
    # Build ordered values from data, falling back to defaults
    vals = tuple(data.get(k, _DEFAULTS[k]) for k in _COLUMNS if k != "date")
 
    if existing:
        set_clause = ", ".join(
            f"{k}=?" for k in _COLUMNS if k != "date"
        )
        cur.execute(
            f"UPDATE lab_reports SET {set_clause}, date=DATE('now') WHERE id=?",
            vals + (existing[0],)
        )
    else:
        col_names = ", ".join(k for k in _COLUMNS if k != "date")
        placeholders = ", ".join("?" for _ in _COLUMNS if _ != "date")
        cur.execute(
            f"""INSERT INTO lab_reports (user_id, {col_names}, date)
                VALUES (?, {placeholders}, DATE('now'))""",
            (user_id,) + vals
        )
 
    conn.commit()
    conn.close()