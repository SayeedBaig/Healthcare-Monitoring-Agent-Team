import streamlit as st
import sqlite3
import bcrypt

DB_NAME = "health_data.db"

def validate_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, password_hash, role FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        return {"name": user[0], "role": user[2]}
    return None


def show_login():
    st.title("🔐 Login to Health Agent")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_user(email, password)
        if user:
            st.session_state["authenticated"] = True
            st.session_state["user_name"] = user["name"]
            st.session_state["user_role"] = user["role"]
            st.session_state["page"] = "Dashboard"   
            st.success(f"Welcome, {user['name']}!")
            st.rerun()  
        else:
            st.error("Invalid email or password. Please try again.")
