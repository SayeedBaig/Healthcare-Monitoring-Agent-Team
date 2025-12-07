import streamlit as st
import bcrypt
from scripts.db_operations import get_user_by_email
from ui.registration import show_registration

def validate_user(email, password):
    user = get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return user
    return None

def show_login():
    st.title("🔐 Login to Health Agent")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if not email or not password:
            st.warning("Please enter both email and password.")
            return

        user = validate_user(email, password)
        if user:
            st.session_state["authenticated"] = True
            st.session_state["user_name"] = user["name"]
            st.session_state["user_role"] = user["role"]
            st.session_state["user_id"] = user["id"]
            st.success(f"Welcome, {user['name']}!")
            st.rerun()
        else:
            st.error("❌ Invalid email or password. Please try again.")
