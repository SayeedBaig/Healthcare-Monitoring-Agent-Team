# ui/style_utils.py
import streamlit as st

def inject_custom_css():
    css = """
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* CSS variables for global light blue themed color system */
    :root {
        --bg-main: #f0f9ff;
        --bg-gradient: linear-gradient(135deg, #e0f2fe 0%, #f0fdfa 60%, #ffffff 100%);
        --card-bg: rgba(255, 255, 255, 0.7);
        --card-border: rgba(14, 165, 233, 0.12);
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --accent-blue: #0284c7;
        --accent-teal: #0d9488;
        --primary-gradient: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        --danger-gradient: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        --sidebar-bg: #0f172a;
        --glass-shadow: 0 8px 32px 0 rgba(15, 23, 42, 0.05);
        --hover-transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Global Font and Core Resets */
    html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stInput, .stSelectbox {
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* Main Container Styles */
    [data-testid="stAppViewContainer"] {
        background: var(--bg-gradient) !important;
        color: var(--text-primary) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Custom Header Styles */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: var(--text-primary) !important;
    }

    /* Title Highlights */
    .main-title {
        background: linear-gradient(90deg, #0369a1, #0d9488);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        margin-bottom: 2rem !important;
        letter-spacing: -0.03em !important;
        display: inline-block;
    }

    /* Modern Glassmorphic Cards */
    .health-card {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin: 16px 0px !important;
        box-shadow: var(--glass-shadow) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        transition: var(--hover-transition) !important;
    }
    .health-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 40px 0 rgba(14, 165, 233, 0.12) !important;
        border-color: rgba(14, 165, 233, 0.3) !important;
    }

    /* Premium Metrics Card Styling (Streamlit Widgets) */
    [data-testid="stMetric"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: var(--glass-shadow) !important;
        backdrop-filter: blur(8px) !important;
        transition: var(--hover-transition) !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        border-color: rgba(13, 148, 136, 0.3) !important;
        box-shadow: 0 8px 24px rgba(13, 148, 136, 0.08) !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: var(--accent-blue) !important;
        background: linear-gradient(90deg, #0369a1, #0d9488);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    /* Input Control Overrides */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox [role="button"], .stDateInput input {
        background-color: #ffffff !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(15, 23, 42, 0.15) !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        transition: var(--hover-transition) !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus, .stSelectbox [role="button"]:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.2) !important;
        outline: none !important;
    }

    /* Buttons Styling */
    div.stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: var(--hover-transition) !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.2) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.35) !important;
        background: linear-gradient(135deg, #0369a1 0%, #0f766e 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 10px rgba(2, 132, 199, 0.2) !important;
    }

    /* Destructive/Danger Buttons Override */
    div.stButton > button[key*="del"], div.stButton > button[key*="delete"] {
        background: var(--danger-gradient) !important;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.2) !important;
    }
    div.stButton > button[key*="del"]:hover, div.stButton > button[key*="delete"]:hover {
        background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%) !important;
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.35) !important;
    }

    /* Styled Sidebar with light/dark contrast safety */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"], [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        transition: var(--hover-transition) !important;
        margin-bottom: 4px !important;
        border: 1px solid transparent !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #38bdf8 !important;
        border-color: rgba(56, 189, 248, 0.15) !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] [data-checked="true"] label {
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.12) 0%, rgba(13, 148, 136, 0.04) 100%) !important;
        color: #38bdf8 !important;
        font-weight: 600 !important;
        border-color: rgba(56, 189, 248, 0.25) !important;
    }
    [data-testid="stSidebar"] button {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
    }

    /* Native Alert/Status Box Styles */
    [data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(15, 23, 42, 0.08) !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(8px) !important;
    }
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
        color: var(--text-primary) !important;
    }
    [data-testid="stAlert"]:has([aria-label="Success"]) {
        border-left: 4px solid #10b981 !important;
        background-color: #f0fdf4 !important;
    }
    [data-testid="stAlert"]:has([aria-label="Info"]) {
        border-left: 4px solid var(--accent-blue) !important;
        background-color: #f0f9ff !important;
    }
    [data-testid="stAlert"]:has([aria-label="Warning"]) {
        border-left: 4px solid #f59e0b !important;
        background-color: #fffbeb !important;
    }
    [data-testid="stAlert"]:has([aria-label="Error"]) {
        border-left: 4px solid #ef4444 !important;
        background-color: #fef2f2 !important;
    }

    /* Table & Dataframe overrides */
    .stDataFrame, [data-testid="stTable"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 10px !important;
        padding: 6px !important;
    }

    /* Elegant Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Custom Dividers */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.02) 0%, rgba(15, 23, 42, 0.1) 50%, rgba(15, 23, 42, 0.02) 100%) !important;
        margin: 24px 0 !important;
    }

    /* Native Chat Message Overrides */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(15, 23, 42, 0.08) !important;
        border-radius: 12px !important;
        padding: 14px !important;
        margin-bottom: 12px !important;
        backdrop-filter: blur(4px) !important;
    }
    [data-testid="stChatMessageUser"] {
        background-color: rgba(2, 132, 199, 0.08) !important;
        border-color: rgba(2, 132, 199, 0.18) !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
