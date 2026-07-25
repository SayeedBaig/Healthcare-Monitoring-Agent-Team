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
DB_PATH = os.path.join(PROJECT_ROOT, "healthcare.db")

# Small cache (optional)
CHATBOT_CACHE = {}
CACHE_TTL = 30   # 30 seconds


# ------------------------------
# Fetch medication info from DB
# ------------------------------
def get_medication_info_from_db(search_term: str, user_id: int = None) -> str | None:
    if not user_id:
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT med_name, schedule, notes
            FROM medications
            WHERE user_id = ? AND LOWER(med_name) LIKE ?
        """, (user_id, f"%{search_term.lower()}%"))

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
def process_health_query(user_query: str, user_id: int = None) -> str:
    query = user_query.lower()

    # 1. Cache
    if query in CHATBOT_CACHE:
        entry = CHATBOT_CACHE[query]
        if time.time() - entry["ts"] < CACHE_TTL:
            return "(cached) " + entry["response"]
        else:
            del CHATBOT_CACHE[query]

    # 2. Check medications in active prescriptions first
    words = [w.strip("?,.!") for w in user_query.split()]
    if user_id:
        for w in words:
            if len(w) > 3:
                result = get_medication_info_from_db(w, user_id)
                if result:
                    return "📘 **Your Active Prescription Info:**\n\n" + result

    # 3. Fallback: check general Indian Medicine Reference info
    try:
        from agents.indian_health_db_tool import get_medicine_info
        for w in words:
            if len(w) > 3:
                gen_info = get_medicine_info(w)
                if gen_info:
                    return (
                        f"💊 **Medicine Reference Info (General):**\n\n"
                        f"**Name:** {gen_info['name']}\n"
                        f"**Use-case:** {gen_info['use_case']}\n"
                        f"**Side-effects:** {gen_info['side_effects']}\n"
                        f"**Precautions:** {gen_info['precautions']}"
                    )
    except Exception:
        pass

    # 4. Real LLM response (Groq)
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
