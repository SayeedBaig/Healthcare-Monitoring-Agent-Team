import joblib
import numpy as np

model = joblib.load("risk_model.pkl")
encoder = joblib.load("risk_label_encoder.pkl")
scaler = joblib.load("risk_scaler.pkl")

def predict_risk(BMI, Daily_Steps, Calories_Intake, Hours_of_Sleep, Heart_Rate, Systolic_BP, Exercise_Hours_per_Week):
    x = np.array([[BMI, Daily_Steps, Calories_Intake, Hours_of_Sleep, Heart_Rate, Systolic_BP, Exercise_Hours_per_Week]])
    x_scaled = scaler.transform(x)
    prediction = model.predict(x_scaled)[0]
    return encoder.inverse_transform([prediction])[0]

# Example
risk = predict_risk(26.55, 12486, 2837, 7.4, 71, 102, 0.7)
print("Predicted Risk:", risk)
