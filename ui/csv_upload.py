# ui/csv_upload.py
import streamlit as st
import pandas as pd
from scripts.db_operations import add_fitness_data

def show_csv_upload_ui():
    st.header("📤 Upload Fitness CSV")
    uploaded = st.file_uploader("Choose CSV file", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        st.write("Preview:")
        st.dataframe(df.head())
        if st.button("Import to DB"):
            # required columns: user_id, date, steps, calories, heart_rate
            for _, row in df.iterrows():
                uid = int(row.get("user_id", st.session_state.get("user_id", 1)))
                date = str(row.get("date", "2025-01-01"))
                steps = int(row.get("steps", 0))
                calories = int(row.get("calories", 0))
                hr = int(row.get("heart_rate", 0))
                add_fitness_data(uid, steps, calories, hr, date)
            st.success("Imported CSV to DB.")
