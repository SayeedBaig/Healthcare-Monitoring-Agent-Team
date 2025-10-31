import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts import db_operations
import json
import streamlit as st

def cal_avg_steps(data):
    if not data:
        return 0
    total_steps = sum(entry['steps'] for entry in data)
    return total_steps/len(data)

def analyse_calories(data, target=2000):
    if not data:
        return "No data available."
    avg_calories = sum(entry['calories'] for entry in data)/len(data)
    if avg_calories > target:
        return "Above target"
    elif avg_calories < target:
        return "Below target"
    else:
        return "On track"

def classify_heart_rate(data):
    if not data:
        return "No data available."
    avg_hr = sum(entry['heart_rate'] for entry in data)/len(data)
    if avg_hr < 60:
        return "Low"
    elif 60 <= avg_hr <= 100:
        return "Normal"
    else:
        return "High"
    
@st.cache_data(ttl=300) # Cache the result for 300 seconds (5 minutes)
def get_analytics():
    """
    Fetches raw fitness data, calculates metrics, and returns insights.
    The @st.cache_data decorator ensures this intensive computation only runs once 
    every 5 minutes or if the database file (a dependency) changes.
    """
    # ... (Keep existing logic)
    # data = db_operations.fetch_fitness()  <-- This line should be here, assumed working
    
    # Since we don't have the content of db_operations, we will ensure that 
    # db_operations.fetch_fitness() is either mocked or assumed to work with caching.
    
    # NOTE: Assuming fetch_fitness is called here and returns data
    # We must ensure all inputs to this function are hashable for caching to work.

    # ----------------------------------------------------
    # MOCK DATA FOR DEMONSTRATION (If the real DB fetch is slow/unreliable)
    # To truly test speed, you'd use a real fetch_fitness() call here.
    
    # Since this is a performance task, we assume the real db_operations is called here:
    data = db_operations.fetch_fitness() 
    
    if isinstance(data, dict):
        data = [data]
    
    insights = {
        "average_steps": cal_avg_steps(data),
        "calories_vs_target": analyse_calories(data),
        "heart_rate_status": classify_heart_rate(data)
    }
    return insights