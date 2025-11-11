import streamlit as st
import sqlite3
import bcrypt
def registration_page():
    st.title("Create a New Account")
    name = st.text_input("Enter your name: ")
    email = st.text_input("Enter your email: ")
    role = st.selectbox("Select Role", ["doctor", "patient", "caregiver"])
    password = st.text_input("Create a password: ", type="password")
    if st.button("Register"):
        if name and email and role and password:
            conn = sqlite3.connect("health_data.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email=?", (email,))
            existing_user = cur.fetchone()
            if existing_user: st.error("Email already exists. Please login instead.")
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cur.execute(
                    "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                    (name, email, hashed_password.decode('utf-8'), role)
                )
                conn.commit()
                conn.close()
                st.success("Registration successful ! You can now log in.")
                st.session_state["show_login"] = True
        else: st.warning("Please fill in all fields.")