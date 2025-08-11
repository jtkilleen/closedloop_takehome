"""
Medical knowledge tools for symptom analysis and condition lookup.
"""

from typing import Any, Dict, List

from ..data.mock_medical_data import (
    CONDITION_INFO,
    SYMPTOM_QUESTIONS,
    get_conditions_for_symptoms,
    is_red_flag_symptom,
)


def lookup_medical_conditions(symptoms: List[str]) -> Dict[str, Any]:
    """
    Look up possible medical conditions based on reported symptoms.

    Args:
        symptoms: List of symptom names

    Returns:
        Dictionary containing possible conditions and their information
    """
    if not symptoms:
        return {"status": "error", "message": "No symptoms provided for lookup"}

    # Normalize symptoms to lowercase
    normalized_symptoms = [s.lower().strip() for s in symptoms]

    # Get possible conditions
    possible_conditions = get_conditions_for_symptoms(normalized_symptoms)

    # Check for red flag symptoms
    red_flags = [s for s in normalized_symptoms if is_red_flag_symptom(s)]

    # Build condition details
    condition_details = {}
    for condition in possible_conditions:
        if condition in CONDITION_INFO:
            condition_details[condition] = CONDITION_INFO[condition]

    return {
        "status": "success",
        "symptoms_analyzed": normalized_symptoms,
        "possible_conditions": list(possible_conditions),
        "condition_details": condition_details,
        "red_flag_symptoms": red_flags,
        "requires_immediate_attention": len(red_flags) > 0,
    }


def get_symptom_clarification_questions(symptom: str) -> Dict[str, Any]:
    """
    Get clarification questions for a specific symptom.

    Args:
        symptom: The symptom to get questions for

    Returns:
        Dictionary containing clarification questions
    """
    normalized_symptom = symptom.lower().strip()

    questions = SYMPTOM_QUESTIONS.get(
        normalized_symptom,
        [
            "When did this symptom start?",
            "How severe is it on a scale of 1-10?",
            "What makes it better or worse?",
        ],
    )

    return {
        "status": "success",
        "symptom": symptom,
        "clarification_questions": questions,
    }


def analyze_symptom_pattern(symptoms_with_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze patterns in reported symptoms to help with diagnosis.

    Args:
        symptoms_with_details: Dictionary of symptoms and their details

    Returns:
        Dictionary containing pattern analysis
    """
    if not symptoms_with_details:
        return {"status": "error", "message": "No symptom details provided"}

    symptoms = list(symptoms_with_details.keys())
    severity_scores = []
    duration_info = []

    # Extract severity and duration information
    for symptom, details in symptoms_with_details.items():
        if isinstance(details, dict):
            if "severity" in details:
                try:
                    severity_scores.append(int(details["severity"]))
                except (ValueError, TypeError):
                    pass
            if "duration" in details:
                duration_info.append(details["duration"])

    # Calculate average severity
    avg_severity = sum(severity_scores) / len(severity_scores) if severity_scores else 0

    # Determine urgency based on patterns
    urgency = "routine"
    if avg_severity >= 8:
        urgency = "urgent"
    elif avg_severity >= 6:
        urgency = "moderate"

    # Check for concerning combinations
    concerning_combinations = []
    if "chest_pain" in symptoms and "shortness_of_breath" in symptoms:
        concerning_combinations.append("chest_pain_with_breathing_difficulty")
        urgency = "emergency"

    if "severe_headache" in symptoms and "fever" in symptoms:
        concerning_combinations.append("headache_with_fever")
        urgency = "urgent"

    return {
        "status": "success",
        "analyzed_symptoms": symptoms,
        "average_severity": avg_severity,
        "urgency_level": urgency,
        "concerning_combinations": concerning_combinations,
        "pattern_summary": (
            f"Patient reports {len(symptoms)} symptoms with average severity "
            f"{avg_severity:.1f}"
        ),
    }
