# app.py
import streamlit as st
from scripts.db_operations import (
    create_tables,
    add_medication,
    update_medication,
    delete_medication,
    fetch_medications,
    add_fitness_data,
    update_latest_fitness,
    fetch_fitness,
    get_user_by_email,
    get_user_by_id,
    fetch_patients_of_doctor
)
from ui import login_page
from ui.registration import show_registration



# UI imports (you already had these)
from backend.logs_handler import display_logs
from scripts.api_utils import get_nutrition_data
from agents.health_chatbot import process_health_query

# initialize session defaults
defaults = {
    "show_login": True,
    "authenticated": False,
    "user_role": None,
    "user_id": None,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

st.set_page_config(page_title="Healthcare Monitoring Agent", layout="wide")
st.title("🏥 Healthcare Monitoring AI Agent")

# Ensure tables exist (no destructive actions here)
create_tables()

# --- Login / Register navigation if user not authenticated ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    
    # Render login or registration form based on session state
    if st.session_state.get("show_login", True):
        login_page.show_login()
    else:
        show_registration()
    col1, col2 = st.columns([1,1])
    with col2:
        if st.button("Register", key="top_nav_register"):
            st.session_state["show_login"] = False    

    st.stop()  # stop the rest of the app until authenticated


# --- User is authenticated, now show main menu ---
role = st.session_state["user_role"]
user_id = st.session_state.get("user_id", None)
if not user_id:
    st.error("No user_id in session. Please login again.")
    st.stop()

# --- Build sidebar menu based on role ---
if role.lower() == "doctor":
    menu = ["Dashboard", "Patient Health Analytics", "Medication Tracker", "Health Workflow", "Goals", "CSV Upload", "Nutrition / Symptoms"]
elif role.lower() == "patient":
    menu = ["Dashboard", "Medication Tracker", "Fitness Data", "AI Assistant", "Health Workflow", "Goals", "CSV Upload", "Nutrition / Symptoms"]
elif role.lower() == "caregiver":
    menu = ["Dashboard", "Medication Tracker", "Nutrition Insights", "Health Tips"]
else:
    menu = ["Dashboard", "Medication Tracker", "Fitness Data", "Health Workflow", "Goals", "CSV Upload", "Nutrition / Symptoms"]

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", menu)


# ----- Dashboard -----
if page == "Dashboard":
    st.header("Welcome")

    current_user = get_user_by_id(user_id)
    st.write(f"Hello {current_user['name']} — Role: {current_user['role']}")

    # Show Doctor ID only for doctors
    if current_user["role"] == "doctor" or current_user["role"]== "patient":
        st.info(f"🆔 Your ID: **{current_user['id']}**")

# ----- Medication Tracker -----
if page == "Medication Tracker":
    st.header("💊 Medication Tracker")

    # Doctor: select which patient to manage
    target_user_id = user_id
    if role.lower() == "doctor":
        # list patients for this doctor
        patients = fetch_patients_of_doctor(user_id)
        patient_options = {f"{p['name']} ({p['email']})": p['id'] for p in patients}
        if patient_options:
            sel = st.selectbox("Select patient", ["-- choose patient --"] + list(patient_options.keys()))
            if sel != "-- choose patient --":
                target_user_id = patient_options[sel]
        else:
            st.info("You have no assigned patients.")
            target_user_id = None
    elif role.lower() == "caregiver":
        # caregiver: view medications for their patient
        current = get_user_by_id(user_id)
        if current and current.get("patient_id"):
            target_user_id = current["patient_id"]
        else:
            st.info("No patient assigned to your caregiver account.")
            target_user_id = None
    else:
        # patient: operate on their own meds (view only)
        target_user_id = user_id

    st.markdown("---")
    if target_user_id:
        # Show existing meds
        meds = fetch_medications(user_id=target_user_id, requester_id=user_id, requester_role=role)
        if meds:
            st.subheader("📋 Saved Medications")
            # Display as table + for doctors allow edit/delete
            for med in meds:
                med_name, schedule, notes, med_id, created_by = med
                cols = st.columns([4,3,2])
                with cols[0]:
                    st.write(f"**{med_name}**")
                    st.write(notes)
                with cols[1]:
                    st.write(schedule)
                with cols[2]:
                    # Doctor editing controls
                    if role.lower() == "doctor" and (target_user_id != user_id or True):
                        if st.button(f"Edit#{med_id}", key=f"edit_{med_id}"):
                            # simple inline edit modal-like
                            new_name = st.text_input("Medicine Name", value=med_name, key=f"name_{med_id}")
                            new_schedule = st.text_input("Schedule", value=schedule, key=f"sch_{med_id}")
                            new_notes = st.text_area("Notes", value=notes, key=f"notes_{med_id}")
                            if st.button("Save changes", key=f"save_{med_id}"):
                                update_medication(med_id, new_name, new_schedule, new_notes, edited_by=user_id)
                                st.success("Medication updated.")
                                st.rerun()
                        if st.button(f"Delete#{med_id}", key=f"del_{med_id}"):
                            delete_medication(med_id)
                            st.success("Deleted.")
                            st.rerun()
                    else:
                        st.write("")

        else:
            st.info("No medications found for this user.")

        # Add medication: only doctors can add meds for patients
        if role.lower() == "doctor":
            st.subheader("Add / Prescribe Medication")
            med_name = st.text_input("Medicine Name", key="new_med_name")
            schedule = st.text_input("Schedule (e.g., Morning & Night)", key="new_med_schedule")
            notes = st.text_area("Notes", key="new_med_notes")
            if st.button("Save Medication"):
                if med_name and schedule:
                    add_medication(target_user_id, med_name, schedule, created_by=user_id, notes=notes)
                    st.success("✅ Medication added successfully!")
                    st.rerun()
                else:
                    st.warning("Please provide med name and schedule.")
        else:
            st.info("Only doctors can add or edit medications.")

    else:
        st.info("Select a target patient to view medications.")

# ----- Fitness Data -----
elif page == "Fitness Data":
    st.header("🏃 Fitness Data")

    # Determine target (whose fitness we are viewing/editing)
    target_user_id = user_id
    if role.lower() == "doctor":
        # doctor selects a patient to view
        patients = fetch_patients_of_doctor(user_id)
        patient_options = {f"{p['name']} ({p['email']})": p['id'] for p in patients}
        if patient_options:
            sel = st.selectbox("Select patient", ["-- choose patient --"] + list(patient_options.keys()))
            if sel != "-- choose patient --":
                target_user_id = patient_options[sel]
            else:
                st.stop()
        else:
            st.info("You have no assigned patients.")
            st.stop()
    elif role.lower() == "caregiver":
        current = get_user_by_id(user_id)
        if current and current.get("patient_id"):
            target_user_id = current["patient_id"]
        else:
            st.info("No patient assigned.")
            st.stop()
    else:
        target_user_id = user_id

    fitness = fetch_fitness(user_id=target_user_id)
    if role.lower() == "patient" and target_user_id == user_id:
        # patient can edit / add
        st.subheader("Enter / Update Your Fitness Data")
        bmi = st.number_input("Enter your BMI", min_value=0.0, value=float(fitness["bmi"]))
        steps = st.number_input("Steps", min_value=0, step=100, value=int(fitness["steps"]))
        sleep = st.number_input("Sleep Duration (hours)", min_value=0.0, value=float(fitness["sleep"]))
        calories = st.number_input("Calories Burned", min_value=0, step=10, value=int(fitness["calories"]))
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, step=1, value=int(fitness["heart_rate"]))
        exercise = st.number_input("Total Hours of Exercise (this week)", min_value=0.0, value=float(fitness["exercise"]))
        bp = st.number_input("Enter your Systolic Blood Pressure", min_value=0, value=int(fitness["bp"]))
        date = st.date_input("Date")
        if st.button("Save Fitness Data"):
            update_latest_fitness(user_id, float(bmi), int(steps), float(sleep), int(calories), int(heart_rate), float(exercise), int(bp), str(date))
            st.success("✅ Fitness data saved.")
            st.rerun()
    else:
        # viewer (doctor or caregiver) sees metrics read-only
        st.subheader("📊 Latest Fitness Record (read-only)")
        st.metric("BMI", fitness["bmi"])
        st.metric("Steps", fitness["steps"])
        st.metric("Sleep (hours)", fitness["sleep"])
        st.metric("Calories", fitness["calories"])
        st.metric("Heart Rate", f"{fitness['heart_rate']} bpm")
        st.metric("Hours of Exercise this week", fitness["exercise"])
        st.metric("Systolic Blood Pressure", fitness["bp"])
        st.write(f"Record date: {fitness.get('date','')}")

# ----- Nutrition Insights -----
elif page == "Nutrition Insights":
    st.header("🍎 Nutrition Insights")
    nutrition_data = get_nutrition_data()
    if nutrition_data:
        st.subheader(f"Product: {nutrition_data.get('name','Unknown')}")
        col_cal, col_prot, col_sug, col_fat = st.columns(4)
        with col_cal:
            st.metric(label="Energy (kcal/100g)", value=f"{nutrition_data.get('calories_100g','-')} kcal")
        with col_prot:
            st.metric(label="Protein (per 100g)", value=f"{nutrition_data.get('proteins_100g','-')} g")
        with col_sug:
            st.metric(label="Sugar (per 100g)", value=f"{nutrition_data.get('sugars_100g','-')} g")
        with col_fat:
            st.metric(label="Fat (per 100g)", value=f"{nutrition_data.get('fat_100g','-')} g")
    else:
        st.warning("Could not load nutrition data.")

# ----- Health Tips -----
elif page == "Health Tips":
    st.header("💡 Health Tips")
    st.info("💧 Stay hydrated and drink at least 2-3 liters of water daily.")
    st.info("🚶 Walk for 30 minutes every day.")
    st.info("🍎 Eat balanced meals and avoid junk food.")

# ----- AI Assistant -----
elif page == "AI Assistant":
    st.subheader("🤖 AI Health Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if user_input := st.chat_input("Ask me about your medications or health..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = process_health_query(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    st.markdown("---")
    st.subheader("🪵 System Logs")
    with st.expander("View System Logs"):
        display_logs()

# ----- Patient Health Analytics -----
elif page == "Patient Health Analytics":
    st.header("📈 Health Analytics")
    from ui import charts_section
    charts_section.show_charts()

# ----- Health Workflow / Goals / CSV Upload / Nutrition / Symptoms -----
elif page == "Health Workflow":
    from ui.workflow_ui import show_workflow_ui
    show_workflow_ui()

elif page == "Goals":
    from ui.goals_ui import show_goals_ui
    show_goals_ui()

elif page == "CSV Upload":
    from ui.csv_upload import show_csv_upload_ui
    show_csv_upload_ui()

elif page == "Nutrition / Symptoms":
    from ui.nutrition_symptom_ui import show_nutrition_symptom_ui
    show_nutrition_symptom_ui()
