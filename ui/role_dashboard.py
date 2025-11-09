import streamlit as st
def show_role_dashboard(role):

    if role.lower() == "doctor": 
        st.header("👨‍⚕️ Doctor's Dashboard")
        st.info("Welcome Doctor! You can review patient analytics and logs here.")
    
    elif role.lower() == "patient": 
        st.header("👩Patient's Dashboard")
        st.info("Welcome Patient! Here's your health overview.")

    elif role.lower() == "caregiver": 
        st.header("🧑Caregiver's Dashboard")
        st.info("Welcome Caregiver! Here are your remainders and patient updates.")