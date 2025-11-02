
# **Week-3 Report – Medical Chatbot Project**

**Duration:** October 27 – November 3, 2025    
**Team Members:** Vaibhav, Sayeed Baig, Revanth Kumar, saddab

---

## 🧩 **1. Project Overview**

Week 3 focused on improving the chatbot’s **intelligence, reliability, and visualization** features.  
Key highlights:
- Added AI-based analytics computation  
- Integrated chatbot insights  
- Designed an interactive Streamlit dashboard  
- Implemented robust error logging  
- Performed unit testing and final deployment  

---

## ⚙️ **2. Architecture Diagram**

+--------------------------------------------------------------+
|                        Streamlit UI                          |
|--------------------------------------------------------------|
|  - Chat Interface                                             |
|  - Health Analytics Charts                                    |
|  - Log Viewer (Error Display)                                 |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
|                     AI Agent Layer                           |
|--------------------------------------------------------------|
|  Files: health_chatbot.py, analytics_agent.py                 |
|  - Processes user queries                                     |
|  - Generates health insights (steps, calories, heart rate)    |
|  - Communicates with database and logging systems             |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
|                     Database Layer                            |
|--------------------------------------------------------------|
|  File: db_operations.py                                       |
|  - Stores user fitness and medication data                    |
|  - Provides data to analytics agent                           |
+-------------------------------+------------------------------+
                                |
                                v
+--------------------------------------------------------------+
|                 Logging & Error Handling Layer                |
|--------------------------------------------------------------|
|  File: backend/logs_handler.py                                |
|  - Captures runtime and chatbot errors                        |
|  - Displays logs on Streamlit in real-time                    |
+--------------------------------------------------------------+

---

## 📆 **3. Week-3 Daily Progress Summary**

| **Day** | **Date** | **Activity** | **Lead** | **Key Outcomes** |
|----------|-----------|---------------|-----------|------------------|
| Day 1 | Oct 27 | AI Analytics Agent Setup | Revanth | Created `analytics_agent.py` to compute health insights |
| Day 2 | Oct 27 | Chatbot Insight Integration | Sayeed | Enhanced chatbot with health-aware responses |
| Day 3 | Oct 28 | Visualization & UI Integration | Revanth | Added interactive charts using Plotly |
| Day 4 | Oct 30 | Error Handling & Logging | Vaibhav | Implemented `logs_handler.py` and real-time log viewer |
| Day 5 | Oct 31 | Testing & Validation | Sayeed | Created `pytest` suite with 7 passing tests |
| Day 6 | Nov 1 | Git Merge & Deployment | Sayeed | Resolved conflicts and deployed optimized version |
| Day 7 | Nov 3 | Documentation & Review | Vaibhav | Completed final docs and Capabl check-in prep |

---

## 🧠 **4. Key Accomplishments**

- AI Agent integrated with analytics and database  
- Streamlit dashboard added for visual feedback  
- Robust logging and graceful error handling  
- Automated testing with full pass rate  
- GitHub synchronization with optimized caching  

---

## 🧪 **5. Demo Link**

🔗 **Project Repository / Demo:**  
[https://github.com/SayeedBaig/Healthcare-Monitoring-Agent-Team]

---

## 🚀 **6. Final Outcome**

By the end of Week 3, the Medical Chatbot evolved into a **fully functional AI Health Assistant** capable of:  
- Computing and analyzing user health data  
- Responding with contextual, data-driven insights  
- Displaying interactive visual analytics  
- Logging and handling errors transparently  
- Passing all validation and performance checks  
