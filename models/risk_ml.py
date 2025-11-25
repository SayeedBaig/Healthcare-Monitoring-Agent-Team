import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# ---------------------------------------
# 1. Load dataset
# ---------------------------------------
df = pd.read_csv("health_data.csv")  # your dataset

# Features and target
X = df[["BMI", "Daily_Steps", "Calories_Intake", "Hours_of_Sleep", "Heart_Rate", "Systolic_BP", "Exercise_Hours_per_Week"]]
y = df["Risk_Level"]

# ---------------------------------------
# 2. Encode labels (Low, Medium, High)
# ---------------------------------------
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)  # Low=0, Medium=1, High=2

# ---------------------------------------
# 3. Train-test split
# ---------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# ---------------------------------------
# 4. Scale numeric features
# ---------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------
# 5. Train model
# ---------------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42
)

model.fit(X_train_scaled, y_train)

# ---------------------------------------
# 6. Evaluate
# ---------------------------------------
accuracy = model.score(X_test_scaled, y_test)
print("Model Accuracy:", accuracy)

# ---------------------------------------
# 7. Save model & encoder & scaler
# ---------------------------------------
joblib.dump(model, "risk_model.pkl")
joblib.dump(encoder, "risk_label_encoder.pkl")
joblib.dump(scaler, "risk_scaler.pkl")

print("Model saved successfully!")
