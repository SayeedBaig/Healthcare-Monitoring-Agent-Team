import streamlit as st
from scripts.db_operations import delete_user_and_related  # NEW import


def show_account_delete_screen(current_user: dict, current_role: str):
    """
    Delete account screen. Uses db_operations.delete_user_and_related()
    so it does not depend on table / column names here.
    """
    st.subheader("⚠️ Delete My Account")

    if not current_user or not current_role:
        st.warning("You are not logged in.")
        return

    st.info(
        f"You are logged in as **{current_user.get('name', 'Unknown')}** "
        f"({current_role})."
    )

    st.markdown(
        "**This action is permanent.** "
        "All data linked to this account will be removed."
    )

    confirm_text = st.text_input("Type **DELETE** in uppercase to confirm:", max_chars=10)

    if st.button("🗑️ Yes, Delete My Account"):
        if confirm_text != "DELETE":
            st.error("Please type DELETE exactly in uppercase to confirm.")
            return

        user_id = current_user.get("id")
        if user_id is None:
            st.error("User ID missing – cannot delete safely.")
            return

        try:
            # 🔥 MAIN CALL – let db_operations handle the SQL
            delete_user_and_related(user_id)
        except Exception as e:
            st.error(f"Error while deleting account: {e}")
            return

        # Clear session state so user is logged out
        for key in list(st.session_state.keys()):
            if key in ("authenticated", "user_role", "user_id", "user_name", "show_login") or key.startswith("user_"):
                st.session_state.pop(key, None)

        st.success("Your account has been deleted successfully.")
        st.session_state["show_login"] = True
        st.rerun()
