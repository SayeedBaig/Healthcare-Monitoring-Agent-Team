# ui/dashboard_ui.py
import streamlit as st
from scripts.db_operations import get_user_by_id, fetch_patients_of_doctor

def show_dashboard(current_user):
    st.markdown('<h1 class="main-title">📊 Health Command Dashboard</h1>', unsafe_allow_html=True)
    
    role = current_user["role"].lower()
    user_id = current_user["id"]
    name = current_user["name"]
    
    # Hero Welcome Banner
    st.markdown(f"""
    <div class="health-card" style="background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(13, 148, 136, 0.1) 100%) !important;">
        <h2 style="margin:0; color:#3b82f6;">Welcome back, {name}!</h2>
        <p style="margin: 8px 0 0 0; font-size:1.1rem; color:#64748b;">Your personalized healthcare monitor command center. Role: <strong style="text-transform: capitalize; color:#0d9488;">{role}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Subsections by role
    if role == "doctor":
        # ID Card & Patients summary
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div class="health-card" style="text-align: center;">
                <div class="metric-label">Staff Identity</div>
                <div class="metric-value" style="font-size:2.5rem !important; margin: 10px 0;">👨‍⚕️</div>
                <div style="font-weight:600; font-size:1.1rem;">Doctor ID: {user_id}</div>
                <div style="font-size:0.85rem; color:#64748b; margin-top:4px;">Licensed Medical Practitioner</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="health-card" style="height: 100%;">
                <h4 style="margin:0 0 12px 0; color:#0d9488;">📋 Practice Scope</h4>
                <p style="margin:0 0 8px 0; font-size:0.95rem; color:#64748b;">• Manage prescription schedules and check drug conflicts.</p>
                <p style="margin:0 0 8px 0; font-size:0.95rem; color:#64748b;">• Track active patient fitness statistics and vitals logs.</p>
                <p style="margin:0; font-size:0.95rem; color:#64748b;">• Analyze patient lab reports and review machine learning disease risk predictions.</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("👨‍⚕️ Assigned Active Patients")
        patients = fetch_patients_of_doctor(user_id)
        if patients:
            cols = st.columns(min(3, len(patients)))
            for idx, p in enumerate(patients):
                col_idx = idx % 3
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="health-card">
                        <div style="font-weight:700; font-size:1.2rem; color:#2563eb;">{p['name']}</div>
                        <div style="font-size:0.9rem; color:#64748b; margin-top:4px;">📧 {p['email']}</div>
                        <div style="font-size:0.9rem; color:#64748b; margin-top:2px;">📞 {p['phone'] if p['phone'] else 'No phone listed'}</div>
                        <div style="margin-top:12px; font-weight:600; font-size:0.85rem; background: rgba(59, 130, 246, 0.1); color:#2563eb; padding: 4px 8px; border-radius: 6px; display: inline-block;">
                            Patient ID: {p['id']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("You do not have any patients linked to your profile yet.")
            
    elif role == "patient":
        # ID Card & Doctor Info
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div class="health-card" style="text-align: center;">
                <div class="metric-label">Patient Registry</div>
                <div class="metric-value" style="font-size:2.5rem !important; margin: 10px 0;">🏥</div>
                <div style="font-weight:600; font-size:1.1rem;">Patient ID: {user_id}</div>
                <div style="font-size:0.85rem; color:#64748b; margin-top:4px;">Active Health Profile</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            doctor = get_user_by_id(current_user.get("doctor_id"))
            if doctor:
                st.markdown(f"""
                <div class="health-card">
                    <h4 style="margin:0 0 12px 0; color:#2563eb;">🧑‍⚕️ Assigned Doctor</h4>
                    <div style="font-weight:700; font-size:1.2rem; color:#0f172a;">{doctor['name']}</div>
                    <div style="font-size:0.9rem; color:#64748b; margin-top:4px;">📧 {doctor['email']}</div>
                    <div style="font-size:0.9rem; color:#64748b; margin-top:2px;">📞 {doctor['phone'] if doctor['phone'] else 'No phone listed'}</div>
                    <div style="margin-top:12px; font-weight:600; font-size:0.85rem; background: rgba(13, 148, 136, 0.1); color:#0d9488; padding: 4px 8px; border-radius: 6px; display: inline-block;">
                        Doctor ID: {doctor['id']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("You are not yet linked to an attending physician.")
                
        st.markdown("---")
        st.subheader("🚀 Quick Actions & Capabilities")
        
        # Grid of Patient Actions
        act_col1, act_col2 = st.columns(2)
        with act_col1:
            st.markdown("""
            <div class="health-card">
                <h4 style="margin:0 0 8px 0; color:#3b82f6;">💊 Medication Log</h4>
                <p style="margin:0; font-size:0.9rem; color:#64748b;">Review active prescriptions, dosages, and notes issued by your doctor.</p>
            </div>
            <div class="health-card">
                <h4 style="margin:0 0 8px 0; color:#3b82f6;">🏃 Vitals & Fitness Tracker</h4>
                <p style="margin:0; font-size:0.9rem; color:#64748b;">Log step counts, calories burned, blood pressure, BMI, and sleep logs.</p>
            </div>
            """, unsafe_allow_html=True)
        with act_col2:
            st.markdown("""
            <div class="health-card">
                <h4 style="margin:0 0 8px 0; color:#3b82f6;">🧪 Lab Reports & Predictions</h4>
                <p style="margin:0; font-size:0.9rem; color:#64748b;">Record diagnostic metrics to run automated ML disease risk assessments (CKD/Diabetes).</p>
            </div>
            <div class="health-card">
                <h4 style="margin:0 0 8px 0; color:#3b82f6;">🤖 AI Assistant Chat</h4>
                <p style="margin:0; font-size:0.9rem; color:#64748b;">Instantly query the AI agent regarding medication side effects, interactions, or health questions.</p>
            </div>
            """, unsafe_allow_html=True)
            
    elif role == "caregiver":
        # ID Card & Patient Info
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div class="health-card" style="text-align: center;">
                <div class="metric-label">Care Network</div>
                <div class="metric-value" style="font-size:2.5rem !important; margin: 10px 0;">🧑‍🤝‍🧑</div>
                <div style="font-weight:600; font-size:1.1rem;">Caregiver ID: {user_id}</div>
                <div style="font-size:0.85rem; color:#64748b; margin-top:4px;">Primary Guardian Agent</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            patient = get_user_by_id(current_user.get("patient_id"))
            if patient:
                st.markdown(f"""
                <div class="health-card">
                    <h4 style="margin:0 0 12px 0; color:#2563eb;">🧑‍🤝‍🧑 Assigned Ward (Patient)</h4>
                    <div style="font-weight:700; font-size:1.2rem; color:#0f172a;">{patient['name']}</div>
                    <div style="font-size:0.9rem; color:#64748b; margin-top:4px;">📧 {patient['email']}</div>
                    <div style="font-size:0.9rem; color:#64748b; margin-top:2px;">📞 {patient['phone'] if patient['phone'] else 'No phone listed'}</div>
                    <div style="margin-top:12px; font-weight:600; font-size:0.85rem; background: rgba(59, 130, 246, 0.1); color:#2563eb; padding: 4px 8px; border-radius: 6px; display: inline-block;">
                        Patient ID: {patient['id']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("No patient is currently linked to your caregiver registry.")
                
        st.markdown("---")
        st.subheader("💡 Attendant Duties")
        st.markdown("""
        <div class="health-card">
            <p style="margin:0 0 8px 0; font-size:0.95rem; color:#64748b;">• **Medication Tracker**: Verify that your ward takes their medications according to the schedule.</p>
            <p style="margin:0 0 8px 0; font-size:0.95rem; color:#64748b;">• **Nutrition Insights**: Access OpenFoodFacts sample records for healthy food selections.</p>
            <p style="margin:0; font-size:0.95rem; color:#64748b;">• **Health Tips**: Display clean wellness notifications to maintain healthy routines.</p>
        </div>
        """, unsafe_allow_html=True)
