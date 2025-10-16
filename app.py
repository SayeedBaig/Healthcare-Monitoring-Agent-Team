import streamlit as st
import json

# App title
st.set_page_config(page_title="Healthcare Monitoring Agent", layout="wide")
st.title("🏥 Healthcare Monitoring AI Agent")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Medication Tracker", "Fitness Data", "Health Tips"])

import sqlite3

DB_NAME = "health_data.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Medications
c.execute("SELECT med_name, schedule FROM medications")
med_rows = c.fetchall()
medications = [f"{row[0]} ({row[1]})" for row in med_rows] if med_rows else []

# Fitness
c.execute("SELECT steps, calories, heart_rate FROM fitness_data ORDER BY id DESC LIMIT 1")
row = c.fetchone()
fitness_data = {"steps": row[0], "calories": row[1], "heart_rate": row[2]} if row else {"steps":0,"calories":0,"heart_rate":0}

conn.close()

mock_data = {
    "medications": medications,
    "fitness": fitness_data,
    "tips": ["Stay hydrated", "Walk 30 mins daily", "Avoid junk food"]
}


# Main content
if page == "Medication Tracker":
    st.subheader("💊 Medication Tracker")
    st.write("Upcoming Medications:")
    st.table({"Medications": mock_data["medications"]})

elif page == "Fitness Data":
    st.subheader("🏃 Fitness Data")
    st.metric("Steps", mock_data["fitness"]["steps"])
    st.metric("Calories Burned", mock_data["fitness"]["calories"])
    st.metric("Heart Rate", f"{mock_data['fitness']['heart_rate']} bpm")

elif page == "Health Tips":
    st.subheader("💡 Health Tips")
    for tip in mock_data["tips"]:
        st.info(tip)