"""
ui/lab_reports_ui.py
---------------------
- Patient : grouped form (Diabetes fields | CKD fields), save, then predictions
- Doctor  : read-only metrics + predictions
- Shared  : columns stored together, split at predict time
"""
 
import os
import numpy as np
import streamlit as st
import xgboost as xgb
 
from scripts.db_operations import get_user_by_id, fetch_patients_of_doctor
from scripts.db_lab_operations import fetch_lab_report, save_lab_report
 
MODEL_DIR = os.path.join(os.path.dirname(__file__),  "models")
 
 
# ── Model loading ────────────────────────────────────────────────────────────
 
@st.cache_resource
def load_models():
    ckd = xgb.XGBClassifier()
    ckd.load_model(os.path.join(MODEL_DIR, "ckd_xgboost_model.json"))
 
    diab = xgb.XGBClassifier()
    diab.load_model(os.path.join(MODEL_DIR, "diabetes_xgboost_model.json"))
 
    return ckd, diab
 
 
# ── Prediction helpers ───────────────────────────────────────────────────────
 
def predict_diabetes(model, lab: dict):
    """
    Feature order (14):
    Age, Gender, BMI, SBP, DBP, FPG, FFPG, Chol, Tri, HDL, LDL, ALT, BUN, CCR
    """
    X = np.array([[
        lab["age"],    lab["gender"], lab["bmi"],
        lab["sbp"],    lab["dbp"],
        lab["fpg"],    lab["ffpg"],
        lab["chol"],   lab["tri"],    lab["hdl"],  lab["ldl"],
        lab["alt"],    lab["bun"],    lab["ccr"],
    ]], dtype=float)
    prob = float(model.predict_proba(X)[0][1]) * 100
    return ("Positive 🔴" if prob >= 50 else "Negative 🟢"), round(prob, 1)
 
 
def predict_ckd(model, lab: dict):
    """
    Feature order (12):
    age_years, sex, serum_creatinine, bun, uacr,
    hemoglobin, potassium, phosphate, calcium,
    systolic_bp, diastolic_bp, hba1c
    """
    X = np.array([[
        lab["age"],              lab["sex"],
        lab["serum_creatinine"], lab["bun"],   lab["uacr"],
        lab["hemoglobin"],       lab["potassium"],
        lab["phosphate"],        lab["calcium"],
        lab["sbp"],              lab["dbp"],
        lab["hba1c"],
    ]], dtype=float)
    pred_class = int(model.predict(X)[0])
    probs = model.predict_proba(X)[0]

    confidence = round(float(np.max(probs)) * 100, 1)

    return f"Stage {pred_class}", confidence
 
 
# ── Prediction results block (shown to both roles) ───────────────────────────
 
def _show_predictions(lab: dict):
    st.markdown("---")
    st.subheader("🤖 Disease Prediction Results")
 
    # Only run if at least some values have been filled in
    has_data = any(lab[k] not in (0, 0.0, "") for k in ["bmi", "fpg", "serum_creatinine", "hba1c"])
    if not has_data:
        st.info("Predictions will appear here once lab values are saved.")
        return
 
    try:
        ckd_model, diab_model = load_models()
    except Exception as e:
        st.error(f"Could not load models from '{MODEL_DIR}': {e}")
        return
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown("#### 🫘 Chronic Kidney Disease")
        try:
            label, prob = predict_ckd(ckd_model, lab)
            st.metric("Result", label)
            st.progress(int(prob), text=f"Probability: {prob}%")
        except Exception as e:
            st.error(f"CKD prediction error: {e}")
 
    with col2:
        st.markdown("#### 🩸 Diabetes")
        try:
            label, prob = predict_diabetes(diab_model, lab)
            st.metric("Result", label)
            st.progress(int(prob), text=f"Probability: {prob}%")
        except Exception as e:
            st.error(f"Diabetes prediction error: {e}")
 
    st.caption("⚕️ AI-assisted predictions — not a substitute for clinical diagnosis.")
 
 
# ── Main UI ──────────────────────────────────────────────────────────────────
 
def show_lab_reports_ui(role: str, user_id: int):
    st.header("🧪 Lab Reports & Disease Prediction")
 
    # ── Resolve target patient ───────────────────────────────────────────────
    target_user_id = user_id
 
    if role == "doctor":
        patients = fetch_patients_of_doctor(user_id)
        options = {f"{p['name']} ({p['email']})": p["id"] for p in patients}
        if not options:
            st.info("You have no assigned patients.")
            st.stop()
        sel = st.selectbox("Select patient", ["-- choose --"] + list(options.keys()))
        if sel == "-- choose --":
            st.stop()
        target_user_id = options[sel]
 
    elif role == "caregiver":
        current = get_user_by_id(user_id)
        if current and current.get("patient_id"):
            target_user_id = current["patient_id"]
        else:
            st.info("No patient assigned.")
            st.stop()
 
    # ── Fetch latest saved values ────────────────────────────────────────────
    lab = fetch_lab_report(user_id=target_user_id)
 
    # ════════════════════════════════════════════════════════════════════════
    # PATIENT — editable form
    # ════════════════════════════════════════════════════════════════════════
    if role == "patient" and target_user_id == user_id:
        st.subheader("Enter / Update Your Lab Values")
 
        # ── Section 1 : Diabetes fields ──────────────────────────────────────
        st.markdown("#### 🩸 Diabetes Panel")
        st.caption("Age, SBP, DBP and BUN are also used for CKD — enter them here.")
 
        r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns(5)
        with r1c1:
            age = st.number_input("Age (yrs)", min_value=0, max_value=120, step=1,
                                  value=int(lab["age"]))
        with r1c2:
            gender_sel = st.selectbox("Gender", ["Male", "Female"],
                                      index=0 if lab["gender"] == 1 else 1)
            gender = 1 if gender_sel == "Male" else 2
        with r1c3:
            bmi = st.number_input("BMI", min_value=0.0, max_value=70.0,
                                  step=0.1, format="%.1f", value=float(lab["bmi"]))
        with r1c4:
            sbp = st.number_input("SBP (mmHg)", min_value=0, max_value=250, step=1,
                                  value=int(lab["sbp"]))
        with r1c5:
            dbp = st.number_input("DBP (mmHg)", min_value=0, max_value=150, step=1,
                                  value=int(lab["dbp"]))
 
        r2c1, r2c2, r2c3, r2c4, r2c5 = st.columns(5)
        with r2c1:
            fpg = st.number_input("FPG (mmol/L)", min_value=0.0, max_value=50.0,
                                  step=0.1, format="%.2f", value=float(lab["fpg"]),
                                  help="Fasting Plasma Glucose")
        with r2c2:
            ffpg = st.number_input("FFPG (mmol/L)", min_value=0.0, max_value=50.0,
                                   step=0.1, format="%.2f", value=float(lab["ffpg"]))
        with r2c3:
            chol = st.number_input("Chol (mmol/L)", min_value=0.0, max_value=20.0,
                                   step=0.1, format="%.2f", value=float(lab["chol"]),
                                   help="Total Cholesterol")
        with r2c4:
            tri = st.number_input("Tri (mmol/L)", min_value=0.0, max_value=20.0,
                                  step=0.1, format="%.2f", value=float(lab["tri"]),
                                  help="Triglycerides")
        with r2c5:
            hdl = st.number_input("HDL (mmol/L)", min_value=0.0, max_value=10.0,
                                  step=0.1, format="%.2f", value=float(lab["hdl"]))
 
        r3c1, r3c2, r3c3, r3c4, r3c5 = st.columns(5)
        with r3c1:
            ldl = st.number_input("LDL (mmol/L)", min_value=0.0, max_value=10.0,
                                  step=0.1, format="%.2f", value=float(lab["ldl"]))
        with r3c2:
            alt = st.number_input("ALT (U/L)", min_value=0.0, max_value=500.0,
                                  step=0.5, format="%.1f", value=float(lab["alt"]),
                                  help="Alanine Aminotransferase")
        with r3c3:
            bun = st.number_input("BUN (mmol/L)", min_value=0.0, max_value=50.0,
                                  step=0.1, format="%.2f", value=float(lab["bun"]),
                                  help="Blood Urea Nitrogen — also used for CKD")
        with r3c4:
            ccr = st.number_input("CCR (mL/min)", min_value=0.0, max_value=200.0,
                                  step=0.5, format="%.1f", value=float(lab["ccr"]),
                                  help="Creatinine Clearance Rate")
 
        st.markdown("---")
 
        # ── Section 2 : CKD-only fields ──────────────────────────────────────
        st.markdown("#### 🫘 CKD Panel")
 
        r4c1, r4c2, r4c3, r4c4, r4c5, r4c6 = st.columns(6)
        with r4c1:
            sex_sel = st.selectbox("Sex", ["Male", "Female"],
                                   index=0 if lab["sex"] == 1 else 1,
                                   help="As recorded in CKD dataset")
            sex = 1 if sex_sel == "Male" else 2
        with r4c2:
            serum_creatinine = st.number_input("Serum Creatinine (mg/dL)",
                                               min_value=0.0, max_value=30.0,
                                               step=0.1, format="%.2f",
                                               value=float(lab["serum_creatinine"]))
        with r4c3:
            uacr = st.number_input("UACR (mg/g)", min_value=0.0, max_value=10000.0,
                                   step=1.0, format="%.1f", value=float(lab["uacr"]),
                                   help="Urine Albumin-to-Creatinine Ratio")
        with r4c4:
            hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=0.0,
                                         max_value=25.0, step=0.1, format="%.1f",
                                         value=float(lab["hemoglobin"]))
        with r4c5:
            potassium = st.number_input("Potassium (mEq/L)", min_value=0.0,
                                        max_value=10.0, step=0.1, format="%.1f",
                                        value=float(lab["potassium"]))
        with r4c6:
            phosphate = st.number_input("Phosphate (mg/dL)", min_value=0.0,
                                        max_value=20.0, step=0.1, format="%.1f",
                                        value=float(lab["phosphate"]))
 
        r5c1, r5c2 = st.columns([1, 5])
        with r5c1:
            calcium = st.number_input("Calcium (mg/dL)", min_value=0.0,
                                      max_value=20.0, step=0.1, format="%.1f",
                                      value=float(lab["calcium"]))
        with r5c2:
            hba1c = st.number_input("HbA1c (%)", min_value=0.0, max_value=20.0,
                                    step=0.1, format="%.1f", value=float(lab["hba1c"]))
 
        st.markdown("")
        if st.button("💾 Save Lab Report", type="primary", use_container_width=True):
            save_lab_report(target_user_id, {
                # shared
                "age": age, "sbp": sbp, "dbp": dbp, "bun": bun,
                # diabetes-only
                "gender": gender, "bmi": bmi,
                "fpg": fpg, "ffpg": ffpg,
                "chol": chol, "tri": tri, "hdl": hdl, "ldl": ldl,
                "alt": alt, "ccr": ccr,
                # ckd-only
                "sex": sex,
                "serum_creatinine": serum_creatinine,
                "uacr": uacr, "hemoglobin": hemoglobin,
                "potassium": potassium, "phosphate": phosphate,
                "calcium": calcium, "hba1c": hba1c,
            })
            st.success("✅ Lab report saved.")
            st.rerun()
 
    # ════════════════════════════════════════════════════════════════════════
    # DOCTOR / CAREGIVER — read-only
    # ════════════════════════════════════════════════════════════════════════
    else:
        st.subheader("📊 Latest Lab Report (read-only)")
        if lab["date"]:
            st.caption(f"📅 Last updated: {lab['date']}")
 
        st.markdown("#### 🩸 Diabetes Panel")
        dc1, dc2, dc3, dc4, dc5, dc6, dc7 = st.columns(7)
        dc1.metric("Age",    f"{lab['age']} yrs")
        dc2.metric("Gender", "Male" if lab["gender"] == 1 else "Female")
        dc3.metric("BMI",    lab["bmi"])
        dc4.metric("SBP",    f"{lab['sbp']} mmHg")
        dc5.metric("DBP",    f"{lab['dbp']} mmHg")
        dc6.metric("BUN",    f"{lab['bun']} mmol/L")
        dc7.metric("CCR",    f"{lab['ccr']} mL/min")
 
        dc8, dc9, dc10, dc11, dc12, dc13, dc14 = st.columns(7)
        dc8.metric("FPG",   f"{lab['fpg']}")
        dc9.metric("FFPG",  f"{lab['ffpg']}")
        dc10.metric("Chol", f"{lab['chol']}")
        dc11.metric("Tri",  f"{lab['tri']}")
        dc12.metric("HDL",  f"{lab['hdl']}")
        dc13.metric("LDL",  f"{lab['ldl']}")
        dc14.metric("ALT",  f"{lab['alt']} U/L")
 
        st.markdown("#### 🫘 CKD Panel")
        kc1, kc2, kc3, kc4, kc5, kc6, kc7, kc8 = st.columns(8)
        kc1.metric("Sex",         "Male" if lab["sex"] == 1 else "Female")
        kc2.metric("Creatinine",  f"{lab['serum_creatinine']} mg/dL")
        kc3.metric("UACR",        f"{lab['uacr']} mg/g")
        kc4.metric("Hemoglobin",  f"{lab['hemoglobin']} g/dL")
        kc5.metric("Potassium",   f"{lab['potassium']} mEq/L")
        kc6.metric("Phosphate",   f"{lab['phosphate']} mg/dL")
        kc7.metric("Calcium",     f"{lab['calcium']} mg/dL")
        kc8.metric("HbA1c",       f"{lab['hba1c']} %")
 
    # ── Predictions (both roles) ─────────────────────────────────────────────
    _show_predictions(lab)