from fastapi import FastAPI
app = FastAPI()
@app.get("/healthdata")
def get_health_data():
    fitness_data = {
        "steps": 7500,
        "calories": 320,
        "heart_rate": 72,
        "sleep_hours": 7.5
    }
    return fitness_data