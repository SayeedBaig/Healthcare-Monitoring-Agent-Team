import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts import db_operations
import json

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
    
def get_analytics():
    data = db_operations.fetch_fitness()
    if isinstance(data, dict):
        data = [data]
    insights = {
        "average_steps": cal_avg_steps(data),
        "calories_vs_target": analyse_calories(data),
        "heart_rate_status": classify_heart_rate(data)
    }
    return insights

if __name__ == "__main__":
    print(json.dumps(get_analytics(), indent=4))