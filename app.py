import streamlit as st
import json

# App title
st.set_page_config(page_title="Healthcare Monitoring Agent", layout="wide")
st.title("🏥 Healthcare Monitoring AI Agent")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Medication Tracker", "Fitness Data", "Health Tips"])

# Mock data
mock_data = {
    "medications": ["Paracetamol 500mg", "Vitamin D3", "Amoxicillin 250mg"],
    "fitness": {"steps": 8421, "calories": 320, "heart_rate": 78},
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