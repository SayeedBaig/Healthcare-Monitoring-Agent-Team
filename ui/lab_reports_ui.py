import streamlit as st
from scripts.db_operations import get_user_by_id, fetch_patients_of_doctor


# TODO: replace these two stubs with real DB functions once the table is ready
def fetch_lab_report(user_id):
    """Fetch the latest lab report for a user. Returns a dict with default values."""
    return {
        "age_years":             1,    # min_value=1
        "sex":                   "Male",
        "serum_creatinine_mgdl": 0.0,
        "bun_mgdl":              0.0,
        "uacr_mg_g":             0.0,
        "hemoglobin_gdl":        0.0,
        "potassium_meql":        0.0,
        "phosphate_mgdl":        0.0,
        "calcium_mgdl":          0.0,
        "systolic_bp":           50,   # min_value=50
        "diastolic_bp":          30,   # min_value=30
        "hba1c_pct":             0.0,
        "ckd_stage":             1,
    }


def save_lab_report(user_id, data: dict):
    """Persist lab report values for a user."""
    pass  # TODO: implement DB write


def show_lab_reports_ui(role: str, user_id: int):
    st.header("🧪 Lab Reports & Disease Prediction")

    # ------------------------------------------------------------------
    # Resolve target patient
    # ------------------------------------------------------------------
    target_user_id = user_id

    if role == "doctor":
        patients = fetch_patients_of_doctor(user_id)
        patient_options = {f"{p['name']} ({p['email']})": p["id"] for p in patients}
        if patient_options:
            sel = st.selectbox(
                "Select patient",
                ["-- choose patient --"] + list(patient_options.keys())
            )
            if sel != "-- choose patient --":
                target_user_id = patient_options[sel]
            else:
                st.stop()
        else:
            st.info("You have no assigned patients.")
            st.stop()

    elif role == "caregiver":
        current = get_user_by_id(user_id)
        if current and current.get("patient_id"):
            target_user_id = current["patient_id"]
        else:
            st.info("No patient assigned.")
            st.stop()

    else:
        target_user_id = user_id

    # ------------------------------------------------------------------
    # Fetch existing values
    # ------------------------------------------------------------------
    lab = fetch_lab_report(user_id=target_user_id)

    # ------------------------------------------------------------------
    # Patient — editable form
    # ------------------------------------------------------------------
    if role == "patient" and target_user_id == user_id:
        st.subheader("Enter / Update Your Lab Report Values")

        age = st.number_input(
            "Age (years)",
            min_value=1, max_value=120, step=1,
            value=int(lab["age_years"])
        )
        sex = st.selectbox(
            "Sex",
            options=["Male", "Female"],
            index=0 if lab["sex"] == "Male" else 1
        )
        serum_creatinine = st.number_input(
            "Serum Creatinine (mg/dL)",
            min_value=0.0, max_value=30.0, step=0.1, format="%.2f",
            value=float(lab["serum_creatinine_mgdl"])
        )
        bun = st.number_input(
            "BUN — Blood Urea Nitrogen (mg/dL)",
            min_value=0.0, max_value=200.0, step=0.5, format="%.1f",
            value=float(lab["bun_mgdl"])
        )
        uacr = st.number_input(
            "UACR — Urine Albumin-to-Creatinine Ratio (mg/g)",
            min_value=0.0, max_value=10000.0, step=1.0, format="%.1f",
            value=float(lab["uacr_mg_g"])
        )
        hemoglobin = st.number_input(
            "Hemoglobin (g/dL)",
            min_value=0.0, max_value=25.0, step=0.1, format="%.1f",
            value=float(lab["hemoglobin_gdl"])
        )
        potassium = st.number_input(
            "Potassium (mEq/L)",
            min_value=0.0, max_value=10.0, step=0.1, format="%.1f",
            value=float(lab["potassium_meql"])
        )
        phosphate = st.number_input(
            "Phosphate (mg/dL)",
            min_value=0.0, max_value=20.0, step=0.1, format="%.1f",
            value=float(lab["phosphate_mgdl"])
        )
        calcium = st.number_input(
            "Calcium (mg/dL)",
            min_value=0.0, max_value=20.0, step=0.1, format="%.1f",
            value=float(lab["calcium_mgdl"])
        )
        systolic_bp = st.number_input(
            "Systolic Blood Pressure (mmHg)",
            min_value=50, max_value=250, step=1,
            value=int(lab["systolic_bp"])
        )
        diastolic_bp = st.number_input(
            "Diastolic Blood Pressure (mmHg)",
            min_value=30, max_value=150, step=1,
            value=int(lab["diastolic_bp"])
        )
        hba1c = st.number_input(
            "HbA1c (%)",
            min_value=0.0, max_value=20.0, step=0.1, format="%.1f",
            value=float(lab["hba1c_pct"])
        )
        ckd_stage = st.selectbox(
            "CKD Stage",
            options=[1, 2, 3, 4, 5],
            index=int(lab["ckd_stage"]) - 1
        )

        if st.button("Save Lab Report"):
            data = {
                "age_years":             age,
                "sex":                   sex,
                "serum_creatinine_mgdl": serum_creatinine,
                "bun_mgdl":              bun,
                "uacr_mg_g":             uacr,
                "hemoglobin_gdl":        hemoglobin,
                "potassium_meql":        potassium,
                "phosphate_mgdl":        phosphate,
                "calcium_mgdl":          calcium,
                "systolic_bp":           systolic_bp,
                "diastolic_bp":          diastolic_bp,
                "hba1c_pct":             hba1c,
                "ckd_stage":             ckd_stage,
            }
            save_lab_report(user_id, data)
            st.success("✅ Lab report saved.")
            st.rerun()

    # ------------------------------------------------------------------
    # Doctor / Caregiver — read-only view
    # ------------------------------------------------------------------
    else:
        st.subheader("📊 Latest Lab Report (read-only)")

        st.metric("Age", f"{lab['age_years']} years")
        st.metric("Sex", lab["sex"])
        st.metric("Serum Creatinine", f"{lab['serum_creatinine_mgdl']} mg/dL")
        st.metric("BUN", f"{lab['bun_mgdl']} mg/dL")
        st.metric("UACR", f"{lab['uacr_mg_g']} mg/g")
        st.metric("Hemoglobin", f"{lab['hemoglobin_gdl']} g/dL")
        st.metric("Potassium", f"{lab['potassium_meql']} mEq/L")
        st.metric("Phosphate", f"{lab['phosphate_mgdl']} mg/dL")
        st.metric("Calcium", f"{lab['calcium_mgdl']} mg/dL")
        st.metric("Systolic BP", f"{lab['systolic_bp']} mmHg")
        st.metric("Diastolic BP", f"{lab['diastolic_bp']} mmHg")
        st.metric("HbA1c", f"{lab['hba1c_pct']} %")
        st.metric("CKD Stage", lab["ckd_stage"])

    # ------------------------------------------------------------------
    # Prediction cards — visible to both roles
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🤖 Disease Prediction Results")
    st.info("Predictions will appear here once the lab values are saved and the models are connected.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🫘 Chronic Kidney Disease", "—", help="Model not connected yet")
    with col2:
        st.metric("🩸 Diabetes", "—", help="Model not connected yet")
    with col3:
        st.metric("❤️ Heart Disease", "—", help="Model not connected yet")
    with col4:
        st.metric("🦋 Thyroid Disorder", "—", help="Model not connected yet")