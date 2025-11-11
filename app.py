import streamlit as st
from backend.auth import role_selector
from backend.logs_handler import display_logs
from scripts.db_operations import (
    create_tables,
    add_medication,
    add_fitness_data,
    fetch_medications,
    fetch_fitness
)
# New import for enhanced Day 5 plan
from scripts.api_utils import get_nutrition_data 
from agents.health_chatbot import process_health_query
defaults = {
    "show_login": True,
    "authenticated": False,
    "user_role": None,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val
from ui import login_page
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login_page.show_login()
    st.stop()

from ui import role_dashboard

role = st.session_state["user_role"]
if role.lower() ==  "doctor": menu = ["Dashboard", "Patient Health Analytics", "Medication Tracker"]
elif role.lower() == "patient": menu = ["Dashboard", "Medication Tracker", "Fitness Data", "AI Assistant"]
elif role.lower() == "caregiver": menu = ["Dashboard", "Medication Tracker", "Nutrition Insights", "Health Tips"]

# App setup
st.set_page_config(page_title="Healthcare Monitoring Agent", layout="wide")
st.title("🏥 Healthcare Monitoring AI Agent")


create_tables()

# Sidebar Navigation
st.sidebar.title("Navigation")
# UPDATED: Added "Nutrition Insights" to the navigation
page = st.sidebar.radio("Go to", menu)

# ----- Dashboard Page (Based On Role) -----
if page == "Dashboard":
    role_dashboard.show_role_dashboard(role)

# ----- PAGE 1: Medication Tracker (UNCHANGED) -----
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

# ----- PAGE 2: Fitness Data (UNCHANGED) -----
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

# ----- NEW PAGE: Nutrition Insights (Enhanced Day 5 Integration) -----
elif page == "Nutrition Insights":
    st.header("🍎 Nutrition Insights (from OpenFoodFacts API Sample)")
    st.caption("This data is loaded from the openfoodfacts_sample.json file collected on Day 4.")

    # Fetch the data using the new utility function
    nutrition_data = get_nutrition_data()

    if nutrition_data:
        st.subheader(f"Product: {nutrition_data['name']}")
        
        # Display key metrics using columns
        col_cal, col_prot, col_sug, col_fat = st.columns(4)
        
        with col_cal:
            st.metric(label="Energy (kcal/100g)", value=f"{nutrition_data['calories_100g']} kcal")
        with col_prot:
            st.metric(label="Protein (per 100g)", value=f"{nutrition_data['proteins_100g']} g")
        with col_sug:
            st.metric(label="Sugar (per 100g)", value=f"{nutrition_data['sugars_100g']} g")
        with col_fat:
            st.metric(label="Fat (per 100g)", value=f"{nutrition_data['fat_100g']} g")
            
        st.markdown("---")
        st.info("💡 **Next Step:** This page will be enhanced with interactive charts and integrated into the core LLM agent.")

    else:
        st.warning("Could not load or parse nutrition data. Ensure 'docs/api_samples/openfoodfacts_sample.json' exists.")


# ----- PAGE 4: Health Tips (UNCHANGED) -----
elif page == "Health Tips":
    st.header("💡 Health Tips")
    st.info("💧 Stay hydrated and drink at least 2-3 liters of water daily.")
    st.info("🚶 Walk for 30 minutes every day.")
    st.info("🍎 Eat balanced meals and avoid junk food.")

# ----- PAGE 5: AI Assistant -----
elif page == "AI Assistant":
    st.subheader("🤖 AI Health Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if user_input :=st.chat_input("Ask me about your medications or health..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = process_health_query(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    st.markdown("---")
    st.subheader("🪵 System Logs")
    with st.expander("View System Logs"):
        display_logs()

# ----- PAGE 6: Health Analytics -----
elif page == "Patient Health Analytics":
    st.header("📈 Health Analytics")
    from ui import charts_section
    charts_section.show_charts()

    