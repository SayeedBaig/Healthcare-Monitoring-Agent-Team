# agents/health_chatbot.py (FINAL PATH-FIXED VERSION)

import sqlite3
import os
import sys
import time

# 🌟 FIX START: MUST BE HERE 🌟
# Append the project root (parent directory) to sys.path so Python can find 'agents'
# This is necessary because we are executing a file *inside* the 'agents' directory.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# 🌟 FIX END 🌟

# Now that the path is set, the import below will succeed.
from agents.analytics_agent import get_analytics # Week 3, Day 2 Import


# --- Configuration & Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR) # This resolves to the project root
DB_PATH = os.path.join(PROJECT_ROOT, "health_data.db")

# 🌟 Week 2, Day 5: Mock Redis Cache Implementation 🌟
CHATBOT_CACHE = {} 
CACHE_TTL_SECONDS = 30 
MAX_CACHE_SIZE = 3 

# ----------------------------

def setup_test_medication_data():
    """Utility function to ensure a test entry exists."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO medications (id, user_id, med_name, schedule) VALUES (?, ?, ?, ?)",
            (10, 1, 'Paracetamol 500mg', 'Morning and Night')
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"ERROR: Database setup failed: {e}")
    finally:
        if conn:
            conn.close()

# --- AI Agent Tool: Database Lookup ---

def get_medication_info_from_db(medication_search_term: str) -> str:
    """Fetches information from the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
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

# --- AI Agent Logic (Core Dispatch) ---

def process_health_query(user_query: str) -> str:
    """
    The core chatbot function, with caching and insight generation.
    """
    query_lower = user_query.lower()
    
    # --- Caching: 1. Check Cache ---
    if query_lower in CHATBOT_CACHE:
        cache_entry = CHATBOT_CACHE[query_lower]
        if time.time() - cache_entry["timestamp"] < CACHE_TTL_SECONDS:
            print(f"🤖 [CONSOLE LOG] Cache HIT for: '{user_query}'")
            return f"(Cached Response) {cache_entry['response']}"
        else:
            del CHATBOT_CACHE[query_lower]
            print(f"🤖 [CONSOLE LOG] Cache MISS (Expired) for: '{user_query}'")
    else:
        print(f"🤖 [CONSOLE LOG] Cache MISS (New Query) for: '{user_query}'")


    # --- Agent Logic: 2. Insight Generation (Week 3, Day 2 Logic) ---
    response = ""

    if "health review" in query_lower or "insights" in query_lower or "how am i doing" in query_lower or "fitness" in query_lower:
        
        # Call the Analytics Agent using the correct function name
        insights = get_analytics()
        
        # Determine the status messages based on the keys returned by get_analytics()
        # NOTE: Using .get() for safety, and :.0f for steps which is float in analytics_agent.py
        steps_message = f"Your average daily steps: **{insights.get('average_steps', 0):.0f}**."
        calories_message = f"Calorie analysis: **{insights.get('calories_vs_target', 'N/A')}** vs. your 2000 target."
        hr_message = f"Heart rate status: **{insights.get('heart_rate_status', 'N/A')}**."
        
        # Generate the contextual, personalized response
        response = (
            f"Here is your latest health metrics review:\n\n"
            f"🚶 Steps: {steps_message}\n"
            f"🍽️ Calories: {calories_message}\n"
            f"❤️ Heart Rate: {hr_message}\n\n"
            f"Keep up the great work on your monitoring!"
        )
    
    # --- Agent Logic: 3. Medication Info Logic (Week 2 Logic) ---
    elif "paracetamol" in query_lower or "dolo" in query_lower or "dosage" in query_lower:
        if "dolo" in query_lower:
            search_term = "Dolo650"
        else:
            search_term = "Paracetamol"
        response = get_medication_info_from_db(search_term)
    
    # --- Agent Logic: 4. Simple Health Tip Logic (Week 2 Logic) ---
    elif "tip" in query_lower or "advice" in query_lower:
        response = "🧠 **Health Tip**: Tracking your daily steps is vital for cardiovascular health. Aim for at least 7,500 steps!"

    # --- Agent Logic: 5. Default/Fallback response ---
    else:
        response = "Hello! I am your Healthcare AI Agent. I can look up your medication schedule or give you a full **health review**. What can I help with?"


    # --- Caching: 2. Store New Response ---
    if response:
        if len(CHATBOT_CACHE) >= MAX_CACHE_SIZE:
            oldest_key = next(iter(CHATBOT_CACHE))
            del CHATBOT_CACHE[oldest_key]
            
        CHATBOT_CACHE[query_lower] = {
            "response": response,
            "timestamp": time.time()
        }

    return response

# --- Deliverable Verification ---

if __name__ == "__main__":
    
    # The try/except block below is now redundant because the fix is at the top, 
    # but we will keep it simple for final verification.

    print(f"--- Chatbot Complete Feature Test (Week 3, Day 2) ---")
    setup_test_medication_data()
    print(f"Database path: {DB_PATH}")
    
    # Test 1: Insight Generation (New Feature)
    test_query_1 = "Can you give me a health review?"
    print(f"\n[User]: {test_query_1}")
    response_1 = process_health_query(test_query_1)
    print(f"[Agent]: {response_1}")

    # Test 2: Medication Lookup (Week 2 Feature)
    test_query_2 = "What about Dolo650?"
    print(f"\n[User]: {test_query_2}")
    response_2 = process_health_query(test_query_2)
    print(f"[Agent]: {response_2}")

    # Test 3: Cache Hit Check
    print(f"\n[User]: {test_query_1} (Second run for cache check)")
    response_3 = process_health_query(test_query_1)
    print(f"[Agent]: {response_3}")

    print("\n--- Verification Complete ---")