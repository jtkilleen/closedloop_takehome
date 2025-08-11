"""
Unit tests for medical knowledge tools.
"""

import pytest
from medical_diagnostic_agent.tools.medical_knowledge import (
    lookup_medical_conditions,
    get_symptom_clarification_questions,
    analyze_symptom_pattern,
)


class TestLookupMedicalConditions:
    """Test the medical conditions lookup functionality."""

    def test_lookup_with_common_symptoms(self):
        """Test lookup with common cold symptoms."""
        symptoms = ["fever", "cough", "sore_throat"]
        result = lookup_medical_conditions(symptoms)

        assert result["status"] == "success"
        assert "common_cold" in result["possible_conditions"]
        assert "flu" in result["possible_conditions"]
        assert result["symptoms_analyzed"] == ["fever", "cough", "sore_throat"]
        assert not result["requires_immediate_attention"]

    def test_lookup_with_red_flag_symptoms(self):
        """Test lookup with red flag symptoms."""
        symptoms = ["severe_chest_pain", "difficulty_breathing"]
        result = lookup_medical_conditions(symptoms)

        assert result["status"] == "success"
        assert result["requires_immediate_attention"]
        assert len(result["red_flag_symptoms"]) > 0

    def test_lookup_with_empty_symptoms(self):
        """Test lookup with no symptoms provided."""
        result = lookup_medical_conditions([])

        assert result["status"] == "error"
        assert "No symptoms provided" in result["message"]

    def test_lookup_with_case_insensitive_symptoms(self):
        """Test that symptom lookup is case insensitive."""
        symptoms_upper = ["FEVER", "COUGH"]
        symptoms_lower = ["fever", "cough"]

        result_upper = lookup_medical_conditions(symptoms_upper)
        result_lower = lookup_medical_conditions(symptoms_lower)

        assert (
            result_upper["possible_conditions"] == result_lower["possible_conditions"]
        )

    def test_lookup_includes_condition_details(self):
        """Test that condition details are included in results."""
        symptoms = ["fever", "cough"]
        result = lookup_medical_conditions(symptoms)

        assert "condition_details" in result
        if "common_cold" in result["possible_conditions"]:
            assert "common_cold" in result["condition_details"]
            assert "description" in result["condition_details"]["common_cold"]


class TestSymptomClarificationQuestions:
    """Test the symptom clarification questions functionality."""

    def test_get_questions_for_chest_pain(self):
        """Test getting questions for chest pain."""
        result = get_symptom_clarification_questions("chest_pain")

        assert result["status"] == "success"
        assert result["symptom"] == "chest_pain"
        assert len(result["clarification_questions"]) > 0
        assert any(
            "severe" in question.lower()
            for question in result["clarification_questions"]
        )

    def test_get_questions_for_unknown_symptom(self):
        """Test getting questions for unknown symptom."""
        result = get_symptom_clarification_questions("rare_symptom")

        assert result["status"] == "success"
        assert len(result["clarification_questions"]) >= 3  # Default questions
        assert any(
            "When did" in question for question in result["clarification_questions"]
        )

    def test_case_insensitive_symptom_questions(self):
        """Test that symptom questions are case insensitive."""
        result_upper = get_symptom_clarification_questions("CHEST_PAIN")
        result_lower = get_symptom_clarification_questions("chest_pain")

        assert len(result_upper["clarification_questions"]) == len(
            result_lower["clarification_questions"]
        )


class TestAnalyzeSymptomPattern:
    """Test the symptom pattern analysis functionality."""

    def test_analyze_with_severity_scores(self):
        """Test analysis with severity scores."""
        symptoms_with_details = {
            "chest_pain": {"severity": "8", "duration": "30 minutes"},
            "shortness_of_breath": {"severity": "7", "duration": "30 minutes"},
        }

        result = analyze_symptom_pattern(symptoms_with_details)

        assert result["status"] == "success"
        assert result["average_severity"] == 7.5
        assert result["urgency_level"] in ["urgent", "emergency"]
        assert len(result["concerning_combinations"]) > 0

    def test_analyze_with_low_severity(self):
        """Test analysis with low severity symptoms."""
        symptoms_with_details = {
            "runny_nose": {"severity": "3", "duration": "2 days"},
            "mild_cough": {"severity": "2", "duration": "2 days"},
        }

        result = analyze_symptom_pattern(symptoms_with_details)

        assert result["status"] == "success"
        assert result["average_severity"] == 2.5
        assert result["urgency_level"] == "routine"

    def test_analyze_with_empty_symptoms(self):
        """Test analysis with no symptoms."""
        result = analyze_symptom_pattern({})

        assert result["status"] == "error"
        assert "No symptom details provided" in result["message"]

    def test_analyze_concerning_combinations(self):
        """Test detection of concerning symptom combinations."""
        symptoms_with_details = {
            "chest_pain": {"severity": "9"},
            "shortness_of_breath": {"severity": "8"},
        }

        result = analyze_symptom_pattern(symptoms_with_details)

        assert result["urgency_level"] == "emergency"
        assert (
            "chest_pain_with_breathing_difficulty" in result["concerning_combinations"]
        )

    def test_analyze_with_invalid_severity(self):
        """Test analysis with invalid severity values."""
        symptoms_with_details = {
            "headache": {"severity": "not_a_number", "duration": "1 day"},
            "fever": {"severity": "5", "duration": "1 day"},
        }

        result = analyze_symptom_pattern(symptoms_with_details)

        assert result["status"] == "success"
        assert result["average_severity"] == 5.0  # Only valid severity counted
