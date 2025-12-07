import streamlit as st
import bcrypt
from scripts.db_operations import add_user

def show_registration():
    st.header("📝 Register New Account")
    
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["patient", "doctor", "caregiver"])
    
    doctor_id = None
    patient_id = None

    # Extra fields based on role
    if role == "patient":
        doctor_id_input = st.text_input("Assigned Doctor ID")

        if doctor_id_input.strip():
            if doctor_id_input.isdigit():
                doctor_id = int(doctor_id_input)
            else:
                st.warning("⚠ Please enter a valid numeric Doctor ID.")
                doctor_id = None

    elif role == "caregiver":
        patient_id_input = st.text_input("Assigned Patient ID")

        if patient_id_input.strip():
            if patient_id_input.isdigit():
                patient_id = int(patient_id_input)
            else:
                st.warning("⚠ Please enter a valid numeric Patient ID.")
                patient_id = None

    if st.button("Register", key="register_button"):
        if not name or not email or not password:
            st.warning("Please fill in all required fields.")
            return

        # Patient must provide a valid doctor_id
        if role == "patient" and doctor_id is None:
            st.error("❌ You must enter a valid Doctor ID.")
            return

        # Caregiver must provide a valid patient_id
        if role == "caregiver" and patient_id is None:
            st.error("❌ You must enter a valid Patient ID.")
            return

        # Hash password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt).decode()

        try:
            add_user(name, email, phone, password_hash, role, doctor_id, patient_id)
            st.success("✅ Registration successful! Please login now.")
        except Exception as e:
            st.error(f"Registration failed: {e}")
