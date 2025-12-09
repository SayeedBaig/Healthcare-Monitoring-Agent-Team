# agents/health_chatbot.py

import sqlite3
import os
import sys
import time
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

# Get API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the client
client = Groq(api_key=GROQ_API_KEY)

# Resolve database path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "health_data.db")

# Small cache (optional)
CHATBOT_CACHE = {}
CACHE_TTL = 30   # 30 seconds


# ------------------------------
# Fetch medication info from DB
# ------------------------------
def get_medication_info_from_db(search_term: str) -> str | None:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT med_name, schedule, notes
            FROM medications
            WHERE LOWER(med_name) LIKE ?
        """, (f"%{search_term.lower()}%",))

        row = cursor.fetchone()
        if not row:
            return None

        med, schedule, notes = row
        return (
            f"Medication: **{med}**\n"
            f"Schedule: **{schedule}**\n"
            f"Notes: {notes if notes else 'No notes'}"
        )

    except Exception as e:
        return f"Error reading medication data: {e}"
    finally:
        if 'conn' in locals():
            conn.close()


# ------------------------------
# Main Chatbot Handler
# ------------------------------
def process_health_query(user_query: str) -> str:
    query = user_query.lower()

    # 1. Cache
    if query in CHATBOT_CACHE:
        entry = CHATBOT_CACHE[query]
        if time.time() - entry["ts"] < CACHE_TTL:
            return "(cached) " + entry["response"]
        else:
            del CHATBOT_CACHE[query]

    # 2. If query mentions medication, check DB first
    if "medicine" in query or "medication" in query or "dose" in query or "tablet" in query:
        # Extract a keyword from user query (simple approach)
        words = user_query.split()
        for w in words:
            result = get_medication_info_from_db(w)
            if result:
                return "📘 **Your Medication Info:**\n\n" + result

    # 3. Real LLM response (Groq)
    try:
        completion = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=[
                {"role": "system", "content": (
                    "You are a friendly healthcare assistant. "
                    "You answer clearly, provide caution when needed, "
                    "and avoid giving harmful or extreme medical advice. "
                    "If users ask serious medical questions, tell them to consult a doctor."
                )},
                {"role": "user", "content": user_query}
            ],
            temperature=0.4,
            max_tokens=300
        )

        response = completion.choices[0].message.content

        # Save to cache
        CHATBOT_CACHE[query] = {"response": response, "ts": time.time()}

        return response

    except Exception as e:
        return f"AI Assistant Error: {e}"
