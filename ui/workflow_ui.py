# ui/workflow_ui.py
import streamlit as st
from agents.langgraph_workflow import run_workflow

def show_workflow_ui():
    st.header("⚙️ Run Health Workflow")
    user_id = st.number_input("User ID", min_value=1, value=1)
    if st.button("Run Workflow"):
        with st.spinner("Running workflow..."):
            out = run_workflow(user_id=int(user_id))
        st.subheader("Risk")
        st.write(out["risk"])
        st.subheader("Medication Conflicts")
        st.write(out["conflicts"] or "No conflicts")
        st.subheader("Report Summary")
        st.write(out["report"]["summary"] if isinstance(out.get("report"), dict) else out.get("report"))
