# agents/risk_ml.py
def predict_risk(fitness):
    """
    fitness: dict with keys 'steps', 'calories', 'heart_rate'
    Returns: {'level': 'Low'|'Medium'|'High', 'reason': str}
    """
    steps = int(fitness.get("steps", 0) or 0)
    hr = int(fitness.get("heart_rate", 0) or 0)
    calories = int(fitness.get("calories", 0) or 0)

    # simple rule-based model (safe, explainable)
    if hr >= 120 or steps < 1000:
        return {"level": "High", "reason": "Very high heart rate or very low activity"}
    if hr >= 100 or steps < 3000:
        return {"level": "Medium", "reason": "Elevated heart rate or low activity"}
    return {"level": "Low", "reason": "Normal vitals and activity"}
