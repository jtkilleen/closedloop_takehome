"""
Unit tests for risk assessment tools.
"""

import pytest
from medical_diagnostic_agent.tools.risk_assessment import (
    assess_patient_risk,
    generate_care_recommendations,
    _get_follow_up_timeline,
)


class TestAssessPatientRisk:
    """Test the patient risk assessment functionality."""

    def test_assess_low_risk_patient(self):
        """Test assessment of low-risk patient."""
        symptoms = ["runny_nose", "mild_cough"]
        patient_info = {"age": 25, "medical_history": []}

        result = assess_patient_risk(symptoms, patient_info)

        assert result["status"] == "success"
        assert result["care_level"] in ["routine", "moderate"]
        assert result["red_flag_count"] == 0
        assert not result["immediate_attention_required"]

    def test_assess_high_risk_elderly_patient(self):
        """Test assessment of elderly patient with risk factors."""
        symptoms = ["fever", "cough", "shortness_of_breath"]
        patient_info = {"age": 75, "medical_history": ["heart_disease", "diabetes"]}

        result = assess_patient_risk(symptoms, patient_info)

        assert result["status"] == "success"
        assert result["age_risk_multiplier"] > 1.0
        assert len(result["risk_factors"]) > 0
        assert any("Age group" in factor for factor in result["risk_factors"])
        assert any("Medical history" in factor for factor in result["risk_factors"])

    def test_assess_red_flag_symptoms(self):
        """Test assessment with red flag symptoms."""
        symptoms = ["severe_chest_pain", "difficulty_breathing"]
        patient_info = {"age": 45, "medical_history": []}

        result = assess_patient_risk(symptoms, patient_info)

        assert result["status"] == "success"
        assert result["care_level"] == "emergency"
        assert result["red_flag_count"] >= 2
        assert result["immediate_attention_required"]

    def test_assess_with_symptom_details(self):
        """Test assessment including symptom severity details."""
        symptoms = ["chest_pain", "headache"]
        patient_info = {"age": 50, "medical_history": []}
        symptom_details = {
            "chest_pain": {"severity": "9"},
            "headache": {"severity": "8"},
        }

        result = assess_patient_risk(symptoms, patient_info, symptom_details)

        assert result["status"] == "success"
        assert result["care_level"] in ["urgent", "emergency"]
        assert any("High severity" in factor for factor in result["risk_factors"])

    def test_assess_with_empty_symptoms(self):
        """Test assessment with no symptoms."""
        result = assess_patient_risk([], {"age": 30})

        assert result["status"] == "error"
        assert "No symptoms provided" in result["message"]

    def test_assess_pediatric_patient(self):
        """Test assessment of pediatric patient."""
        symptoms = ["fever", "cough"]
        patient_info = {"age": 5, "medical_history": []}

        result = assess_patient_risk(symptoms, patient_info)

        assert result["status"] == "success"
        assert result["age_risk_multiplier"] > 1.0
        assert any(
            "Age group (pediatric)" in factor for factor in result["risk_factors"]
        )

    def test_assess_with_high_risk_medical_history(self):
        """Test assessment with high-risk medical conditions."""
        symptoms = ["chest_pain"]
        patient_info = {
            "age": 60,
            "medical_history": ["heart_disease", "hypertension", "diabetes"],
        }

        result = assess_patient_risk(symptoms, patient_info)

        assert result["status"] == "success"
        assert result["risk_score"] > 5  # Should have elevated risk score
        assert len([f for f in result["risk_factors"] if "Medical history" in f]) == 3


class TestGenerateCareRecommendations:
    """Test the care recommendations generation functionality."""

    def test_emergency_recommendations(self):
        """Test recommendations for emergency care level."""
        risk_assessment = {
            "care_level": "emergency",
            "immediate_attention_required": True,
            "risk_score": 25,
        }
        possible_conditions = ["heart_attack"]

        result = generate_care_recommendations(risk_assessment, possible_conditions)

        assert result["status"] == "success"
        assert result["care_level"] == "emergency"
        assert result["immediate_attention_required"]
        assert any("911" in rec for rec in result["primary_recommendations"])
        assert any(
            "emergency" in rec.lower() for rec in result["primary_recommendations"]
        )

    def test_urgent_care_recommendations(self):
        """Test recommendations for urgent care level."""
        risk_assessment = {
            "care_level": "urgent",
            "immediate_attention_required": False,
            "risk_score": 15,
        }
        possible_conditions = ["pneumonia"]

        result = generate_care_recommendations(risk_assessment, possible_conditions)

        assert result["status"] == "success"
        assert result["care_level"] == "urgent"
        assert any("24 hours" in rec for rec in result["primary_recommendations"])
        assert result["follow_up_timeline"] == "Within 24 hours"

    def test_routine_care_recommendations(self):
        """Test recommendations for routine care level."""
        risk_assessment = {
            "care_level": "routine",
            "immediate_attention_required": False,
            "risk_score": 3,
        }
        possible_conditions = ["common_cold"]

        result = generate_care_recommendations(risk_assessment, possible_conditions)

        assert result["status"] == "success"
        assert result["care_level"] == "routine"
        assert not result["immediate_attention_required"]
        assert any(
            "routine" in rec.lower() or "primary care" in rec.lower()
            for rec in result["primary_recommendations"]
        )

    def test_condition_specific_recommendations(self):
        """Test that condition-specific recommendations are included."""
        risk_assessment = {
            "care_level": "routine",
            "immediate_attention_required": False,
        }
        possible_conditions = ["common_cold", "flu"]

        result = generate_care_recommendations(risk_assessment, possible_conditions)

        assert result["status"] == "success"
        # Should include some condition-specific recommendations
        all_recommendations = (
            result["primary_recommendations"] + result["additional_recommendations"]
        )
        assert any("common_cold" in rec or "flu" in rec for rec in all_recommendations)

    def test_moderate_care_recommendations(self):
        """Test recommendations for moderate care level."""
        risk_assessment = {
            "care_level": "moderate",
            "immediate_attention_required": False,
            "risk_score": 8,
        }
        possible_conditions = []

        result = generate_care_recommendations(risk_assessment, possible_conditions)

        assert result["status"] == "success"
        assert result["care_level"] == "moderate"
        assert "Within 2-3 days" in result["follow_up_timeline"]


class TestFollowUpTimeline:
    """Test the follow-up timeline helper function."""

    def test_emergency_timeline(self):
        """Test timeline for emergency care."""
        timeline = _get_follow_up_timeline("emergency")
        assert timeline == "Immediate"

    def test_urgent_timeline(self):
        """Test timeline for urgent care."""
        timeline = _get_follow_up_timeline("urgent")
        assert timeline == "Within 24 hours"

    def test_moderate_timeline(self):
        """Test timeline for moderate care."""
        timeline = _get_follow_up_timeline("moderate")
        assert timeline == "Within 2-3 days"

    def test_routine_timeline(self):
        """Test timeline for routine care."""
        timeline = _get_follow_up_timeline("routine")
        assert timeline == "Within 1-2 weeks if symptoms persist"

    def test_unknown_care_level(self):
        """Test timeline for unknown care level."""
        timeline = _get_follow_up_timeline("unknown")
        assert timeline == "As needed"
