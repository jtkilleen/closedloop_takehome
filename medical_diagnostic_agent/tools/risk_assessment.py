"""
Risk assessment tools for medical triage and care recommendations.
"""

from typing import Any, Dict, List, Optional

from ..data.mock_medical_data import AGE_RISK_FACTORS, CONDITION_INFO, RED_FLAG_SYMPTOMS


def assess_patient_risk(
    symptoms: List[str],
    patient_info: Dict[str, Any],
    symptom_details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Assess patient risk level based on symptoms and demographics.

    Args:
        symptoms: List of reported symptoms
        patient_info: Patient demographic information (age, medical_history, etc.)
        symptom_details: Additional details about symptoms

    Returns:
        Dictionary containing risk assessment results
    """
    if not symptoms:
        return {
            "status": "error",
            "message": "No symptoms provided for risk assessment",
        }

    # Initialize risk factors
    risk_score = 0
    risk_factors = []

    # Age-based risk assessment
    age = patient_info.get("age", 0)
    age_risk_multiplier = 1.0

    for age_group, info in AGE_RISK_FACTORS.items():
        age_min, age_max = info["age_range"]
        if age_min <= age <= age_max:
            age_risk_multiplier = info["risk_multiplier"]
            if age_risk_multiplier > 1.0:
                risk_factors.append(f"Age group ({age_group}) increases risk")
            break

    # Symptom-based risk assessment
    red_flag_count = 0
    for symptom in symptoms:
        normalized_symptom = symptom.lower().replace(" ", "_")
        if normalized_symptom in RED_FLAG_SYMPTOMS:
            red_flag_count += 1
            risk_score += 10
            risk_factors.append(f"Red flag symptom: {symptom}")

    # Medical history risk factors
    medical_history = patient_info.get("medical_history", [])
    high_risk_conditions = [
        "heart_disease",
        "diabetes",
        "hypertension",
        "copd",
        "cancer",
    ]

    for condition in medical_history:
        if condition.lower() in high_risk_conditions:
            risk_score += 3
            risk_factors.append(f"Medical history: {condition}")

    # Severity-based risk (if available)
    if symptom_details:
        for symptom, details in symptom_details.items():
            if isinstance(details, dict) and "severity" in details:
                try:
                    severity = int(details["severity"])
                    if severity >= 8:
                        risk_score += 5
                        risk_factors.append(
                            f"High severity {symptom} (severity: {severity})"
                        )
                    elif severity >= 6:
                        risk_score += 2
                        risk_factors.append(
                            f"Moderate severity {symptom} (severity: {severity})"
                        )
                except (ValueError, TypeError):
                    pass

    # Apply age multiplier
    risk_score = int(risk_score * age_risk_multiplier)

    # Determine care level
    care_level = "routine"
    if red_flag_count > 0 or risk_score >= 20:
        care_level = "emergency"
    elif risk_score >= 10:
        care_level = "urgent"
    elif risk_score >= 5:
        care_level = "moderate"

    return {
        "status": "success",
        "risk_score": risk_score,
        "care_level": care_level,
        "risk_factors": risk_factors,
        "red_flag_count": red_flag_count,
        "age_risk_multiplier": age_risk_multiplier,
        "immediate_attention_required": care_level == "emergency",
    }


def generate_care_recommendations(
    risk_assessment: Dict[str, Any], possible_conditions: List[str]
) -> Dict[str, Any]:
    """
    Generate care recommendations based on risk assessment and possible conditions.

    Args:
        risk_assessment: Results from assess_patient_risk
        possible_conditions: List of possible medical conditions

    Returns:
        Dictionary containing care recommendations
    """
    care_level = risk_assessment.get("care_level", "routine")
    immediate_attention = risk_assessment.get("immediate_attention_required", False)

    recommendations = []
    next_steps = []

    # Emergency recommendations
    if immediate_attention or care_level == "emergency":
        recommendations.extend(
            [
                "Seek immediate emergency medical attention",
                "Call 911 or go to the nearest emergency room",
                "Do not delay seeking care",
            ]
        )
        next_steps.append("Emergency care required immediately")

    # Urgent care recommendations
    elif care_level == "urgent":
        recommendations.extend(
            [
                "Seek medical attention within 24 hours",
                "Contact your primary care doctor or urgent care center",
                "Monitor symptoms closely",
            ]
        )
        next_steps.append("Schedule urgent medical appointment")

    # Moderate care recommendations
    elif care_level == "moderate":
        recommendations.extend(
            [
                "Schedule appointment with primary care doctor within 2-3 days",
                "Monitor symptoms and seek care if they worsen",
                "Consider over-the-counter treatments for symptom relief",
            ]
        )
        next_steps.append("Schedule medical appointment within few days")

    # Routine care recommendations
    else:
        recommendations.extend(
            [
                "Consider scheduling routine appointment with primary care doctor",
                "Try conservative home treatments",
                "Monitor symptoms and seek care if they persist or worsen",
            ]
        )
        next_steps.append("Consider routine medical follow-up")

    # Condition-specific recommendations
    for condition in possible_conditions:
        if condition in CONDITION_INFO:
            condition_recs = CONDITION_INFO[condition].get("recommendations", [])
            recommendations.extend(
                [f"For {condition}: {rec}" for rec in condition_recs]
            )

    # General recommendations
    general_recommendations = [
        "Stay hydrated",
        "Get adequate rest",
        "Monitor symptoms for changes",
        "Keep a symptom diary",
        "Follow up if symptoms worsen or new symptoms develop",
    ]

    return {
        "status": "success",
        "care_level": care_level,
        "immediate_attention_required": immediate_attention,
        "primary_recommendations": recommendations[:3],  # Top 3 most important
        "additional_recommendations": recommendations[3:] + general_recommendations,
        "next_steps": next_steps,
        "follow_up_timeline": _get_follow_up_timeline(care_level),
    }


def _get_follow_up_timeline(care_level: str) -> str:
    """Get appropriate follow-up timeline based on care level."""
    timelines = {
        "emergency": "Immediate",
        "urgent": "Within 24 hours",
        "moderate": "Within 2-3 days",
        "routine": "Within 1-2 weeks if symptoms persist",
    }
    return timelines.get(care_level, "As needed")
