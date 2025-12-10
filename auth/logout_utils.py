import streamlit as st

def logout():
    """
    Clears all auth-related session state and reloads the app.
    Works for patient / doctor / caregiver.
    """
    keys_to_clear = [
        "authenticated",
        "user_name",
        "user_role",
        "user_id",
        "show_login",
    ]

    # Clear known keys
    for key in keys_to_clear:
        if key in st.session_state:
            st.session_state.pop(key)

    # Clear dynamic user_* keys
    for key in list(st.session_state.keys()):
        if key.startswith("user_"):
            st.session_state.pop(key, None)

    # After clearing → go back to login screen
    st.session_state["show_login"] = True

    # Use the correct rerun function (Streamlit 1.27+)
    st.rerun()
