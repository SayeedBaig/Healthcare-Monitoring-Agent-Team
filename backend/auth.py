import streamlit as st

def role_selector():
    st.sidebar.title("User Role")
    role = st.sidebar.selectbox(
        "Select Role",
        ["Patient", "Doctor", "Caregiver"]
    )

    # Display current role
    st.sidebar.success(f"Current Role: {role}")

    # Simple role permissions
    if role == "Patient":
        st.sidebar.write("You can view your own health data.")
    elif role == "Doctor":
        st.sidebar.write("You can view all patient data.")
    elif role == "Caregiver":
        st.sidebar.write("You can view limited data for assigned patients.")

    return role
