"""
Pytest configuration and shared fixtures for medical diagnostic agent tests.
"""

import pytest
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture
def sample_patient_low_risk():
    """Fixture providing a low-risk patient profile."""
    return {
        "age": 28,
        "medical_history": [],
        "symptoms": ["runny_nose", "mild_cough", "fatigue"],
        "symptom_details": {
            "runny_nose": {"severity": "3", "duration": "2 days"},
            "mild_cough": {"severity": "2", "duration": "2 days"},
            "fatigue": {"severity": "4", "duration": "2 days"},
        },
    }


@pytest.fixture
def sample_patient_high_risk():
    """Fixture providing a high-risk patient profile."""
    return {
        "age": 65,
        "medical_history": ["heart_disease", "diabetes", "hypertension"],
        "symptoms": ["chest_pain", "shortness_of_breath"],
        "symptom_details": {
            "chest_pain": {"severity": "8", "duration": "30 minutes"},
            "shortness_of_breath": {"severity": "7", "duration": "30 minutes"},
        },
    }


@pytest.fixture
def sample_patient_pediatric():
    """Fixture providing a pediatric patient profile."""
    return {
        "age": 5,
        "medical_history": [],
        "symptoms": ["fever", "cough", "irritability"],
        "symptom_details": {
            "fever": {"severity": "6", "duration": "1 day"},
            "cough": {"severity": "5", "duration": "1 day"},
            "irritability": {"severity": "7", "duration": "1 day"},
        },
    }


@pytest.fixture
def sample_patient_elderly():
    """Fixture providing an elderly patient profile."""
    return {
        "age": 78,
        "medical_history": ["copd", "hypertension"],
        "symptoms": ["difficulty_breathing", "fatigue"],
        "symptom_details": {
            "difficulty_breathing": {"severity": "6", "duration": "3 days"},
            "fatigue": {"severity": "7", "duration": "1 week"},
        },
    }


@pytest.fixture
def common_symptoms():
    """Fixture providing common symptom lists for testing."""
    return {
        "cold_symptoms": ["runny_nose", "cough", "sore_throat", "fatigue"],
        "flu_symptoms": ["fever", "cough", "fatigue", "headache", "muscle_aches"],
        "emergency_symptoms": [
            "severe_chest_pain",
            "difficulty_breathing",
            "loss_of_consciousness",
        ],
        "mild_symptoms": ["slight_headache", "minor_fatigue"],
    }


@pytest.fixture
def expected_conditions():
    """Fixture providing expected condition mappings for testing."""
    return {
        "cold_symptoms": ["common_cold", "flu"],
        "chest_pain_symptoms": ["heart_attack", "angina", "anxiety"],
        "respiratory_symptoms": ["asthma", "pneumonia", "bronchitis"],
    }


class MockADKEvent:
    """Mock ADK event for testing without actual Google ADK calls."""

    def __init__(self, text_content: str, author: str = "test_agent"):
        self.content = MockContent([MockPart(text_content)])
        self.author = author


class MockContent:
    """Mock content object for ADK events."""

    def __init__(self, parts):
        self.parts = parts


class MockPart:
    """Mock part object for ADK content."""

    def __init__(self, text: str):
        self.text = text


@pytest.fixture
def mock_adk_event():
    """Fixture providing a mock ADK event."""
    return MockADKEvent("Test response from medical agent")


@pytest.fixture
def mock_consultation_responses():
    """Fixture providing mock consultation responses for different scenarios."""
    return {
        "greeting": "Hello! I'm here to help you with your medical concerns. Please note that this is not a substitute for professional medical advice.",
        "symptom_collection": "Can you tell me more about your symptoms? When did they start and how severe are they?",
        "risk_assessment": "Based on your symptoms, I recommend seeking medical attention within 24 hours.",
        "emergency": "IMMEDIATE MEDICAL ATTENTION REQUIRED. Please call 911 or go to the nearest emergency room.",
    }
