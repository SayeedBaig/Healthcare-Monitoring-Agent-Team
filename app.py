import streamlit as st
from scripts.db_operations import (
    create_tables,
    add_medication,
    add_fitness_data,
    fetch_medications,
    fetch_fitness
)

# App setup
st.set_page_config(page_title="Healthcare Monitoring Agent", layout="wide")
st.title("🏥 Healthcare Monitoring AI Agent")


create_tables()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Medication Tracker", "Fitness Data", "Health Tips"])

# ----- PAGE 1: Medication Tracker -----
if page == "Medication Tracker":
    st.header("💊 Medication Tracker")

    st.subheader("Add New Medication")
    med_name = st.text_input("Medicine Name")
    schedule = st.text_input("Schedule (e.g., Morning & Night)")
    user_id = 1  # using mock user for now

    if st.button("Save Medication"):
        if med_name and schedule:
            add_medication(user_id, med_name, schedule)
            st.success("✅ Medication added successfully!")
        else:
            st.warning("Please fill both fields before saving.")

    st.markdown("---")
    st.subheader("📋 Saved Medications")
    meds = fetch_medications()
    if meds:
        st.table({"Medicine": [m[0] for m in meds], "Schedule": [m[1] for m in meds]})
    else:
        st.info("No medications found yet.")

# ----- PAGE 2: Fitness Data -----
elif page == "Fitness Data":
    st.header("🏃 Fitness Data Entry")

    user_id = 1
    steps = st.number_input("Steps", min_value=0, step=100)
    calories = st.number_input("Calories Burned", min_value=0, step=10)
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, step=1)
    date = st.date_input("Date")

    if st.button("Save Fitness Data"):
        add_fitness_data(user_id, steps, calories, heart_rate, str(date))
        st.success("✅ Fitness data added successfully!")

    st.markdown("---")
    st.subheader("📊 Latest Fitness Record")
    fitness = fetch_fitness()
    st.metric("Steps", fitness["steps"])
    st.metric("Calories", fitness["calories"])
    st.metric("Heart Rate", f"{fitness['heart_rate']} bpm")

# ----- PAGE 3: Health Tips -----
elif page == "Health Tips":
    st.header("💡 Health Tips")
    st.info("💧 Stay hydrated and drink at least 2–3 liters of water daily.")
    st.info("🚶 Walk for 30 minutes every day.")
    st.info("🍎 Eat balanced meals and avoid junk food.")
