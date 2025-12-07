# ui/goals_ui.py
import streamlit as st
from scripts.db_operations import add_fitness_data

GOALS_KEY = "health_goals"  # stored in session_state

def init_goals():
    if GOALS_KEY not in st.session_state:
        st.session_state[GOALS_KEY] = {"steps_goal": 5000, "calories_goal": 2000}

def show_goals_ui():
    st.header("🎯 Set Health Goals")
    init_goals()
    g = st.session_state[GOALS_KEY]
    g["steps_goal"] = st.number_input("Daily steps goal", min_value=100, value=g["steps_goal"])
    g["calories_goal"] = st.number_input("Daily calories goal", min_value=100, value=g["calories_goal"])
    if st.button("Save Goals"):
        st.success("Goals saved.")
    # show progress using last fitness record
    user_id = st.session_state.get("user_id", 1)
    from scripts.db_operations import fetch_fitness
    fitness = fetch_fitness(user_id=user_id)
    steps = fitness.get("steps", 0)
    calories = fitness.get("calories", 0)
    st.subheader("Today's progress")
    st.write(f"Steps: {steps} / {g['steps_goal']}")
    st.progress(min(100, int(steps / max(1, g['steps_goal']) * 100)))
    st.write(f"Calories: {calories} / {g['calories_goal']}")
