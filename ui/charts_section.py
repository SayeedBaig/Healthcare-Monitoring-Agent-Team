def show_charts():
    import streamlit as st
    import plotly.express as px
    import pandas as pd
    data = {
        "date": ["2025-10-21", "2025-10-22", "2025-10-23", "2025-10-24", "2025-10-25"],
        "steps": [4500, 5200, 6100, 5800, 7000],
        "calories_burned": [1800, 1950, 2100, 2000, 2200],
        "calories_intake": [2000, 2050, 1900, 2100, 2150],
        "medication_compliance": [1, 0.8, 1, 0.9, 1],
    }
    df = pd.DataFrame(data)
    st.header("Health Analytics")
    fig1 = px.line(df, x="date", y="steps", title="Steps Trend Over Time")
    st.plotly_chart(fig1)
    fig2=px.bar(df, x="date", y=["calories_intake","calories_burned"], barmode="group", title="Calories Burned vs Intake")
    st.plotly_chart(fig2)
    fig3 = px.bar(df, x="date", y="medication_compliance", title="Medication Compliance", color="medication_compliance")
    st.plotly_chart(fig3)