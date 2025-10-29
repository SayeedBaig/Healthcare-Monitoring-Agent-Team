import logging
import streamlit as st

logging.basicConfig(filename='system_logs.log', level=logging.INFO)

def log_error(message):
    logging.error(message)

def display_logs():
    with st.expander("View System Logs"):
        with open('system_logs.log', 'r') as f:
            st.text(f.read())
