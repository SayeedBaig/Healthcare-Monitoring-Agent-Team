Day-1 Progress Report 
lead: Sayeed (me)
Objective for Day-1
Set up the complete project foundation and confirm Streamlit + Python environment runs successfully for all members.

![alt text](image.png) // hover on image.png to view work done 

Initial setup completed successfully. Environment verified and repository synced across all teammates.


Day 2 Progress Report – Streamlit UI Skeleton 
Lead: Revanth
Support: Sayeed
Objective: Design Streamlit UI skeleton with sidebar, dashboard, and placeholder sections.
 Tasks Completed

Sidebar navigation created

Dashboard, Medication, Fitness, and Health Tips placeholders added

Basic layout tested locally

App runs successfully using streamlit run app.py

Deliverable: Streamlit app runs locally with UI sections visible
Next Step (Day 3): Set up SQLite database and add medication reminder logic (Lead: Vaibhav)



 Day 3 Progress Report – Database Integration 

Lead: Vaibhav 
Support: Sayeed
 Objective

Set up SQLite database, define CRUD operations, and connect with Streamlit UI.

Completed Tasks

Added health_data.db with vitals & medication tables

Created scripts/db_operations.py with all DB functions

Integrated DB with app.py for testing

Verified data insertion & retrieval locally

 Deliverable:
Streamlit app runs with working database integration and can store test inputs.


Day-4 
lead:Sayeed Baig

Objective for Day-4
To research and test suitable public APIs for health and nutrition data integration into the Healthcare Monitoring AI Agent. The primary aim was to fetch live JSON data from at least one working API and document the implementation process.

Results / Output
Successfully fetched and stored real-world nutrition data without authentication, verifying the working API connection and saving a sample response for project reference. This data is ready for integration into the UI

Day-5
lead:Sayeed Baig

Objective for Day-5
To integrate the basic health data parsing logic, display basic fitness metrics from the SQLite database, and, in an enhanced step, integrate the API sample data from Day 4 into a new Streamlit UI section.


Proof of Progress
The Streamlit application now shows a new section, "Nutrition Insights," displaying parsed nutrition data from the OpenFoodFacts API sample, fulfilling the goal of making the Day 4 backend work visible on the UI.

Day-6 Progress Report Deployment  
Lead:Sayeed Baig 
 
 
 
Objective Set up the entire project environment and deploy a basic Streamlit app with a 
placeholder for health monitoring and medication tracking. 
Deliverable 
Met Live URL + functional demo 
 
 
Tasks & Status 
Task Description Status 
GitHub 
Preparation 
Ensured requirements.txt, app.py, and utility scripts were current 
and pushed to the main branch. Completed 
Streamlit 
Cloud Setup 
Created Streamlit Cloud account and connected the Healthcare
Monitoring-Agent-Team GitHub repository4. Completed 
Deployment Successfully deployed the basic application featuring Medication 
Tracker, Fitness Data, and Nutrition Insights5. Success 
Accessibility 
Check 
Verified public link is functional and accessible: https://healthcare
monitoring-agent-team-cjkxjrhjp5rsguhudxxckr.streamlit.app/. Verified 
 
Results / Output 
A working, publicly accessible deployed application is live on Streamlit Cloud, marking the completion of 
the foundation phase and the Quick Win milestone for Week 1. 
 
Deployed Link : https://healthcare-monitoring-agent-team-cjkxjrhjp5rsguhudxxckr.streamlit.app/


WEEK-2 

Week-2  
Day 1 Progress Report
Date: October 20, 2025 Activity: AI Chatbot Foundation Lead: Sayeed 
Objective Achieved: Implement basic question-answer logic for medication tracking using local data (SQLite)
1. Key Accomplishments (Track A: AI Reasoning)
The foundation for the AI Agent has been successfully established by creating the necessary file structure and core logic.
•	Folder Structure: Created the new required directory: agents/.
•	Core Logic File: Created agents/health_chatbot.py.
•	Agent Logic (Tool-Agnostic): Implemented the process_health_query() function to serve as the core Q&A agent logic.
•	Local Tool Integration: Successfully integrated the agent logic with the existing SQLite database (health_data.db) via the get_medication_info_from_db() function. This function acts as the local tool that the agent uses to retrieve structured medication data.
2. Deliverable Verification
•	The core deliverable was verified in the terminal environment
Input Query (Terminal)	Expected Action	Actual Output
"When do I need to take Paracetamol?"	Call DB Tool, Fetch Schedule for Paracetamol.	Successfully returned Paracetamol 500mg: Morning & Night (verified with terminal output).
"What about Dolo650?"	Call DB Tool, Fetch Schedule for Dolo650.	Successfully returned Dolo650: after breakfast Morning (verified with terminal output).
"Give me a quick health tip"	Trigger Hardcoded Tip.	Successfully returned a generic health tip.


