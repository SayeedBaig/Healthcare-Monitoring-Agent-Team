# tests/analytics_test.py (FINAL FIX: MOCKING DB OPERATIONS WITHIN CHATBOT TEST)

import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# CRITICAL: Ensure the project root is on the path for imports to work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the functions we need to test
from agents.analytics_agent import get_analytics, cal_avg_steps, analyse_calories, classify_heart_rate
from agents.health_chatbot import process_health_query, CHATBOT_CACHE


# --- 1. MOCK DATA FIXTURE ---

MOCK_DB_FITNESS_DATA = [
    {'date': '2025-10-20', 'steps': 8000, 'calories': 2100, 'heart_rate': 70},
    {'date': '2025-10-21', 'steps': 6000, 'calories': 1900, 'heart_rate': 65},
    {'date': '2025-10-22', 'steps': 10000, 'calories': 2500, 'heart_rate': 75},
]


# --- 2. TESTS FOR ANALYTICS AGENT (Week 3, Day 1 Logic) - These all pass ---

def test_cal_avg_steps_with_data():
    """Validates the average steps calculation."""
    avg = cal_avg_steps(MOCK_DB_FITNESS_DATA)
    assert avg == 8000.0

def test_analyse_calories_above_target():
    """Validates calorie analysis when average is above 2000 target."""
    status = analyse_calories(MOCK_DB_FITNESS_DATA, target=2000)
    assert status == "Above target"

def test_classify_heart_rate_normal():
    """Validates heart rate classification (should be Normal)."""
    status = classify_heart_rate(MOCK_DB_FITNESS_DATA)
    assert status == "Normal"

@patch('agents.analytics_agent.db_operations')
def test_get_analytics_structure(mock_db_ops):
    """Validates the main get_analytics function by mocking the DB call."""
    mock_db_ops.fetch_fitness.return_value = MOCK_DB_FITNESS_DATA
    insights = get_analytics()
    assert isinstance(insights, dict)
    assert insights['average_steps'] == 8000.0
    assert insights['heart_rate_status'] == "Normal"


# --- 3. TESTS FOR CHATBOT CORE (Week 2/3 Integration) ---

# Clear cache before running each chatbot test
@pytest.fixture(autouse=True)
def clear_cache():
    CHATBOT_CACHE.clear()
    yield
    CHATBOT_CACHE.clear()

# 🌟 FIX APPLIED HERE: Mock the dependency chain explicitly 🌟
@patch('agents.health_chatbot.get_medication_info_from_db') # Mock 1: Mock medication lookup
@patch('agents.analytics_agent.db_operations') # Mock 2: Mock the database call that get_analytics needs
def test_chatbot_insight_query(mock_db_ops, mock_meds):
    """
    Tests the Week 3 insight generation query flow.
    We are mocking db_operations.fetch_fitness so get_analytics runs correctly, 
    allowing us to test the formatting logic in health_chatbot.py.
    """
    # 1. Provide the necessary data to the mocked DB function
    mock_db_ops.fetch_fitness.return_value = [
        {'date': '2025-10-20', 'steps': 9000, 'calories': 2000, 'heart_rate': 70}
    ]
    
    query = "Give me a health review"
    response = process_health_query(query)

    # Check if the analytics agent was called (by checking if the DB operation was called)
    mock_db_ops.fetch_fitness.assert_called_once()
    
    # ASSERTION FIX: Check for the exact formatted string '9000' (from 9000.0f format)
    # The actual output from the failure was 'Your average daily steps: **0**.', 
    # but the mocked data ensures the calculation returns 9000.0.
    assert "9000" in response 
    assert "Heart rate status" in response


@patch('agents.health_chatbot.get_medication_info_from_db')
def test_chatbot_medication_query(mock_meds_db):
    """Tests the Week 2 medication lookup query flow."""
    mock_meds_db.return_value = "✅ Found: Paracetamol schedule: Morning"
    
    query = "When do I take Paracetamol?"
    response = process_health_query(query)
    
    # Check if the medication lookup function was called
    mock_meds_db.assert_called_once()
    assert "Paracetamol" in response

def test_chatbot_caching():
    """Tests the Week 2 caching mechanism."""
    query = "Give me a tip"
    
    # First call: Should be a MISS
    response1 = process_health_query(query)
    assert "(Cached Response)" not in response1
    
    # Second call: Should be a HIT
    response2 = process_health_query(query)
    assert "(Cached Response)" in response2
    
    # Check that the cache actually stores the data
    assert query.lower() in CHATBOT_CACHE