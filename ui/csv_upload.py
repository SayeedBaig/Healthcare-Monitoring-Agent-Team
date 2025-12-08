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

            for _, row in df.iterrows():

                uid = int(row.get("user_id", st.session_state.get("user_id", 1)))
                date = str(row.get("date", "2025-01-01"))
                steps = int(row.get("steps", 0))
                calories = int(row.get("calories", 0))
                hr = int(row.get("heart_rate", 0))

                # CSV may not contain these → give safe defaults
                bmi = float(row.get("bmi", 0.0))
                sleep = float(row.get("sleep", 0.0))
                exercise = float(row.get("exercise", 0.0))
                bp = int(row.get("bp", 0))

                # MUST pass all 9 arguments in correct order
                add_fitness_data(
                    uid,
                    bmi,
                    steps,
                    sleep,
                    calories,
                    hr,
                    exercise,
                    bp,
                    date
                )

            st.success("Imported CSV to DB.")
