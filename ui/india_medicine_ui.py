import streamlit as st
from agents.indian_health_db_tool import get_medicine_info, check_interaction


def india_medicine_page():
    st.title("Indian Medicine Info & Interactions")

    # --- Single medicine lookup ---
    st.subheader("🔍 Single Medicine Lookup")
    med_name = st.text_input("Enter medicine name (e.g., Dolo 650, Paracetamol):")

    if st.button("Search Medicine"):
        info = get_medicine_info(med_name)
        if info is None:
            st.warning("Medicine not found in local database.")
        else:
            st.markdown(f"### {info['name']}")
            st.write("**Use-case:**", info["use_case"])
            st.write("**Side-effects:**", info["side_effects"])
            st.write("**Precautions:**", info["precautions"])

    st.markdown("---")

    # --- Interaction between two medicines ---
    st.subheader("💊 Check Interaction Between Two Medicines")

    col1, col2 = st.columns(2)
    with col1:
        med1 = st.text_input("Medicine 1", key="med1")
    with col2:
        med2 = st.text_input("Medicine 2", key="med2")

    if st.button("Check Interaction"):
        if not med1 or not med2:
            st.warning("Please enter both medicine names.")
        else:
            desc = check_interaction(med1, med2)
            if desc:
                st.error(f"⚠ Interaction found: {desc}")
            else:
                st.success(
                    "No interaction found in local DB (still follow doctor’s advice)."
                )