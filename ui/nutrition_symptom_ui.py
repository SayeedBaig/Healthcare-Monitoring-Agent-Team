# ui/nutrition_symptom_ui.py
import streamlit as st

def show_nutrition_symptom_ui():
    st.header("🍎 Nutrition / Symptoms Tool")
    st.subheader("Nutrition (optional)")
    food = st.text_input("Food item (e.g., apple, cereal)")
    qty = st.number_input("Quantity (g)", min_value=0, value=100)
    if st.button("Save Nutrition"):
        st.success("Nutrition saved (demo).")

    st.markdown("---")
    st.subheader("Symptom Entry")
    symptom = st.text_input("Symptom (e.g., headache, fever)")
    severity = st.selectbox("Severity", ["mild", "moderate", "severe"])
    if st.button("Save Symptom"):
        # for now store in session (demo); integration to DB optional later
        if "symptoms" not in st.session_state:
            st.session_state["symptoms"] = []
        st.session_state["symptoms"].append({"symptom": symptom, "severity": severity})
        st.success("Symptom recorded.")
    if st.session_state.get("symptoms"):
        st.write("Recent symptoms:")
        st.json(st.session_state["symptoms"][-5:])
