# agents/health_chatbot.py (CORRECTED for your existing DB schema)

import sqlite3
import os
import sys
from backend.logs_handler import log_error


# --- Configuration & Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "health_data.db")

# ----------------------------

def setup_test_medication_data():
    """
    Utility function to ensure a 'medications' table and a test entry exists.
    NOTE: This is updated to use YOUR schema: med_name and schedule.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # We don't try to CREATE the table here, as it exists, but we ensure the test data exists.
        
        # We need to insert a test medication using YOUR actual columns: med_name and schedule.
        # Data from your DB: 'Dolo650', 'after breakfast Morning'
        # Data from your DB: 'Paracetamol 500mg', 'Morning and Night'

        # Insert a test medication if not present (using INSERT OR REPLACE on primary key)
        cursor.execute(
            "INSERT OR REPLACE INTO medications (id, user_id, med_name, schedule) VALUES (?, ?, ?, ?)",
            (10, 1, 'Paracetamol 500mg', 'Morning and Night')
        )
        conn.commit()
    except sqlite3.Error as e:
        # If the table creation/insertion fails here, something is fundamentally wrong with the DB file.
        print(f"ERROR: Database setup failed: {e}")
        # sys.exit(1) # Re-add if you want to force exit on error
    finally:
        if conn:
            conn.close()

# --- AI Agent Tool: Database Lookup (using your actual column names) ---

def get_medication_info_from_db(medication_search_term: str) -> str:
    """
    Fetches information for a specific medication from the SQLite database.
    Updated to use 'med_name' and 'schedule' columns.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Search the database for the medication using YOUR column names
        cursor.execute(
            "SELECT med_name, schedule FROM medications WHERE med_name LIKE ?", 
            (f'%{medication_search_term}%',)
        )
        result = cursor.fetchone()
        
        if result:
            med_name, schedule = result
            return (
                f"✅ **Medication Found**: I see you're tracking **{med_name}**. "
                f"Your scheduled intake is: **{schedule}**."
            )
        else:
            return f"❌ Medication Not Found: I couldn't find a medication matching '{medication_search_term}' in your personal records."
            
    except sqlite3.Error as e:
        print(f"Database Access Error: {e}")
        return "An internal database error occurred while trying to fetch medication details."
    finally:
        if conn:
            conn.close()

# --- AI Agent Logic (Simulating LLM Reasoning) ---

def process_health_query(user_query: str) -> str:
    """
    The core chatbot function. It uses simple keyword matching to trigger the tool call.
    """
    query_lower = user_query.lower()

    # 1. Medication Info Logic (e.g., "When to take Paracetamol?")
    if "paracetamol" in query_lower or "dolo" in query_lower or "dosage" in query_lower:
        # We'll use a specific term from the query to search your DB
        if "dolo" in query_lower:
            search_term = "Dolo650"
        else:
            search_term = "Paracetamol" # Covers "Paracetamol 500mg"
        
        # Calls the local database 'tool'
        return get_medication_info_from_db(search_term)
    
    # 2. Simple Health Tip Logic (using hardcoded response)
    elif "tip" in query_lower or "advice" in query_lower:
        return "🧠 **Health Tip**: Tracking your daily steps is vital for cardiovascular health. Aim for at least 7,500 steps!"

    # 3. Default/Fallback response
    else:
        return "Hello! I am your Healthcare AI Agent. I can look up your medication schedule or give you a quick health tip. Try asking about 'Paracetamol'."


# --- Day 1 Deliverable Verification ---

if __name__ == "__main__":
    print(f"--- Day 1 Deliverable: Chatbot Terminal Test ---")
    
    # 1. Ensure the necessary table and data exist
    setup_test_medication_data()
    print(f"Database path: {DB_PATH}")
    
    # 2. Test 1: Query that triggers the SQLite lookup (Paracetamol)
    test_query_1 = "When do I need to take Paracetamol?"
    print(f"\n[User]: {test_query_1}")
    response_1 = process_health_query(test_query_1)
    print(f"[Agent]: {response_1}")

    # 3. Test 2: Query that triggers a generic response
    test_query_2 = "Give me a quick health tip"
    print(f"\n[User]: {test_query_2}")
    response_2 = process_health_query(test_query_2)
    print(f"[Agent]: {response_2}")

    # 4. Test 3: Query for an unknown medication
    test_query_3 = "Check my dosage for Lisinopril"
    print(f"\n[User]: {test_query_3}")
    response_3 = process_health_query(test_query_3)
    print(f"[Agent]: {response_3}")

    # 5. Test 4: Query for a different tracked medication
    test_query_4 = "What about Dolo650?"
    print(f"\n[User]: {test_query_4}")
    response_4 = process_health_query(test_query_4)
    print(f"[Agent]: {response_4}")

    print("\n--- Day 1 Deliverable Complete ---")