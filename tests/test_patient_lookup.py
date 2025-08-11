"""
Unit tests for patient lookup tools.
"""

import pytest
from medical_diagnostic_agent.tools.patient_lookup import (
    lookup_patient_record,
    get_patient_medical_history,
    check_patient_risk_factors,
    list_available_patients,
    save_visit_summary,
    onboard_new_patient,
    update_patient_lifestyle,
)


class TestLookupPatientRecord:
    """Test the patient record lookup functionality."""

    def test_lookup_existing_patient(self, monkeypatch):
        """Test successful lookup of existing patient."""

        def mock_search(name):
            return {
                "name": "John",
                "age": 35,
                "occupation": "Engineer",
                "risk_factors": ["sedentary_work"],
                "lifestyle": {"sleep_pattern": "7-8 hours"},
            }

        def mock_get_all():
            return ["John", "Jane", "Bob"]

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.search_patient_records",
            mock_search,
        )
        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.get_all_patients",
            mock_get_all,
        )

        result = lookup_patient_record("John")

        assert result["status"] == "success"
        assert result["patient_found"] is True
        assert result["record"]["name"] == "John"
        assert result["record"]["age"] == 35
        assert "Found record for John" in result["message"]

    def test_lookup_nonexistent_patient(self, monkeypatch):
        """Test lookup of patient that doesn't exist."""

        def mock_search(name):
            return None

        def mock_get_all():
            return ["Jane", "Bob"]

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.search_patient_records",
            mock_search,
        )
        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.get_all_patients",
            mock_get_all,
        )

        result = lookup_patient_record("John")

        assert result["status"] == "not_found"
        assert "No record found for 'John'" in result["message"]
        assert result["available_patients"] == ["Jane", "Bob"]
        assert "We only use first names" in result["suggestion"]

    def test_lookup_empty_name(self):
        """Test lookup with empty patient name."""
        result = lookup_patient_record("")
        assert result["status"] == "error"
        assert "No patient name provided" in result["message"]

    def test_lookup_whitespace_name(self):
        """Test lookup with whitespace-only patient name."""
        result = lookup_patient_record("   ")
        assert result["status"] == "error"
        assert "No patient name provided" in result["message"]

    def test_lookup_none_name(self):
        """Test lookup with None patient name."""
        result = lookup_patient_record(None)
        assert result["status"] == "error"
        assert "No patient name provided" in result["message"]


class TestGetPatientMedicalHistory:
    """Test the patient medical history functionality."""

    def test_get_history_existing_patient(self, monkeypatch):
        """Test successful retrieval of patient medical history."""

        def mock_get_summary(name):
            return {
                "basic_info": {"name": "Sarah", "age": 42, "occupation": "Teacher"},
                "medical_history": ["hypertension", "asthma"],
                "risk_factors": ["family_history", "stress"],
                "lifestyle_factors": {"exercise": "moderate", "diet": "balanced"},
                "clinical_notes": ["Well-controlled asthma", "Monitor blood pressure"],
                "previous_visits_count": 5,
            }

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.get_patient_summary",
            mock_get_summary,
        )

        result = get_patient_medical_history("Sarah")

        assert result["status"] == "success"
        assert result["patient_name"] == "Sarah"
        assert result["age"] == 42
        assert result["occupation"] == "Teacher"
        assert result["medical_history"] == ["hypertension", "asthma"]
        assert result["risk_factors"] == ["family_history", "stress"]
        assert result["previous_visits"] == 5

    def test_get_history_nonexistent_patient(self, monkeypatch):
        """Test retrieval of medical history for non-existent patient."""

        def mock_get_summary(name):
            return None

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.get_patient_summary",
            mock_get_summary,
        )

        result = get_patient_medical_history("Unknown")

        assert result["status"] == "not_found"
        assert "No medical history found for 'Unknown'" in result["message"]

    def test_get_history_empty_name(self):
        """Test getting medical history with empty name."""
        result = get_patient_medical_history("")
        assert result["status"] == "error"
        assert "No patient name provided" in result["message"]


class TestCheckPatientRiskFactors:
    """Test the patient risk factor analysis functionality."""

    def test_check_risk_factors_high_risk_patient(self, monkeypatch):
        """Test risk factor analysis for high-risk patient."""

        def mock_search(name):
            return {
                "name": "Robert",
                "age": 70,
                "risk_factors": ["smoking_history", "elderly", "diabetes"],
                "lifestyle": {"sleep_pattern": "5-6 hours"},
            }

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.search_patient_records",
            mock_search,
        )

        result = check_patient_risk_factors("Robert")

        assert result["status"] == "success"
        assert result["patient_name"] == "Robert"
        assert result["age"] == 70
        assert "smoking_history" in result["high_risk_factors"]
        assert "elderly" in result["high_risk_factors"]
        assert "chronic_sleep_deprivation" in result["lifestyle_risks"]
        assert result["total_risk_factors"] == 3
        assert len(result["recommendations"]) > 0

    def test_check_risk_factors_moderate_risk_patient(self, monkeypatch):
        """Test risk factor analysis for moderate-risk patient."""

        def mock_search(name):
            return {
                "name": "Lisa",
                "age": 45,
                "risk_factors": ["sedentary_work", "high_caffeine_intake"],
                "lifestyle": {"sleep_pattern": "7-8 hours"},
            }

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.search_patient_records",
            mock_search,
        )

        result = check_patient_risk_factors("Lisa")

        assert result["status"] == "success"
        assert result["patient_name"] == "Lisa"
        assert "sedentary_work" in result["moderate_risk_factors"]
        assert "high_caffeine_intake" in result["moderate_risk_factors"]
        assert result["total_risk_factors"] == 2

    def test_check_risk_factors_nonexistent_patient(self, monkeypatch):
        """Test risk factor analysis for non-existent patient."""

        def mock_search(name):
            return None

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.search_patient_records",
            mock_search,
        )

        result = check_patient_risk_factors("Unknown")

        assert result["status"] == "not_found"
        assert "No record found for 'Unknown'" in result["message"]


class TestListAvailablePatients:
    """Test the available patients listing functionality."""

    def test_list_available_patients(self, monkeypatch):
        """Test listing all available patients."""

        def mock_get_all():
            return ["Alice", "Bob", "Charlie", "Diana"]

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.get_all_patients",
            mock_get_all,
        )

        result = list_available_patients()

        assert result["status"] == "success"
        assert result["total_patients"] == 4
        assert result["available_patients"] == ["Alice", "Bob", "Charlie", "Diana"]
        assert "Found 4 patients" in result["message"]
        assert "Alice, Bob, Charlie, Diana" in result["message"]

    def test_list_available_patients_empty(self, monkeypatch):
        """Test listing when no patients are available."""

        def mock_get_all():
            return []

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.get_all_patients",
            mock_get_all,
        )

        result = list_available_patients()

        assert result["status"] == "success"
        assert result["total_patients"] == 0
        assert result["available_patients"] == []
        assert "Found 0 patients" in result["message"]


class TestSaveVisitSummary:
    """Test the visit summary saving functionality."""

    def test_save_visit_summary_success(self, monkeypatch):
        """Test successful saving of visit summary."""

        def mock_add_note(name, visit_note):
            return True

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.add_visit_note",
            mock_add_note,
        )

        result = save_visit_summary(
            "Emma",
            ["headache", "fatigue"],
            "Tension headache due to stress",
            "Rest, hydration, stress management",
        )

        assert result["status"] == "success"
        assert result["visit_saved"] is True
        assert "Visit summary saved for Emma" in result["message"]

    def test_save_visit_summary_failure(self, monkeypatch):
        """Test failed saving of visit summary."""

        def mock_add_note(name, visit_note):
            return False

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.add_visit_note",
            mock_add_note,
        )

        result = save_visit_summary(
            "Unknown",
            ["fever"],
            "Viral infection",
            "Rest and fluids",
        )

        assert result["status"] == "error"
        assert result["visit_saved"] is False
        assert "Could not save visit for 'Unknown'" in result["message"]

    def test_save_visit_summary_empty_name(self):
        """Test saving visit summary with empty patient name."""
        result = save_visit_summary("", ["symptom"], "assessment", "recommendations")
        assert result["status"] == "error"
        assert "No patient name provided" in result["message"]


class TestOnboardNewPatient:
    """Test the new patient onboarding functionality."""

    def test_onboard_new_patient_success(self, monkeypatch):
        """Test successful onboarding of new patient."""
        mock_patient = {
            "name": "Frank",
            "age": 30,
            "occupation": "Designer",
            "lifestyle": {"exercise": "regular", "diet": "vegetarian"},
        }

        def mock_create(name, age, occupation, lifestyle):
            return {"status": "success", "patient": mock_patient}

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.create_new_patient",
            mock_create,
        )

        result = onboard_new_patient(
            "Frank", 30, "Designer", {"exercise": "regular", "diet": "vegetarian"}
        )

        assert result["status"] == "success"
        assert "Successfully onboarded Frank" in result["message"]
        assert result["patient"] == mock_patient
        assert "next_steps" in result

    def test_onboard_new_patient_empty_name(self):
        """Test onboarding with empty patient name."""
        result = onboard_new_patient("", 30, "Engineer")
        assert result["status"] == "error"
        assert "Patient name is required" in result["message"]

    def test_onboard_new_patient_invalid_age(self):
        """Test onboarding with invalid age."""
        result = onboard_new_patient("Frank", -5, "Engineer")
        assert result["status"] == "error"
        assert "Age must be between 0 and 120" in result["message"]

        result = onboard_new_patient("Frank", 150, "Engineer")
        assert result["status"] == "error"
        assert "Age must be between 0 and 120" in result["message"]

    def test_onboard_new_patient_empty_occupation(self):
        """Test onboarding with empty occupation."""
        result = onboard_new_patient("Frank", 30, "")
        assert result["status"] == "error"
        assert "Occupation is required" in result["message"]


class TestUpdatePatientLifestyle:
    """Test the patient lifestyle update functionality."""

    def test_update_patient_lifestyle_success(self, monkeypatch):
        """Test successful update of patient lifestyle."""

        def mock_search(name):
            return {"name": "Grace", "age": 28}

        def mock_update(name, updates):
            return {"status": "success", "message": "Updated successfully"}

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.search_patient_records",
            mock_search,
        )
        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.update_patient_record",
            mock_update,
        )

        result = update_patient_lifestyle(
            "Grace", {"exercise": "daily", "sleep": "8 hours"}
        )

        assert result["status"] == "success"
        assert "Updated successfully" in result["message"]

    def test_update_patient_lifestyle_patient_not_found(self, monkeypatch):
        """Test lifestyle update for non-existent patient."""

        def mock_search(name):
            return None

        monkeypatch.setattr(
            "medical_diagnostic_agent.tools.patient_lookup.search_patient_records",
            mock_search,
        )

        result = update_patient_lifestyle("Unknown", {"exercise": "daily"})

        assert result["status"] == "not_found"
        assert "Patient 'Unknown' not found" in result["message"]
        assert "Please onboard first" in result["message"]

    def test_update_patient_lifestyle_empty_name(self):
        """Test lifestyle update with empty patient name."""
        result = update_patient_lifestyle("", {"exercise": "daily"})
        assert result["status"] == "error"
        assert "Patient name is required" in result["message"]


class TestRiskRecommendations:
    """Test the risk recommendation generation functionality."""

    def test_high_risk_recommendations(self):
        """Test recommendations for high-risk factors."""
        from medical_diagnostic_agent.tools.patient_lookup import (
            _generate_risk_recommendations,
        )

        high_risk = ["smoking_history", "elderly"]
        moderate_risk = ["sedentary_work"]

        recommendations = _generate_risk_recommendations(high_risk, moderate_risk)

        assert "smoking cessation support" in recommendations[0]
        assert "health screenings" in recommendations[1]
        assert "Ergonomic assessment" in recommendations[2]

    def test_moderate_risk_recommendations(self):
        """Test recommendations for moderate-risk factors."""
        from medical_diagnostic_agent.tools.patient_lookup import (
            _generate_risk_recommendations,
        )

        high_risk = []
        moderate_risk = ["high_caffeine_intake", "sedentary_work"]

        recommendations = _generate_risk_recommendations(high_risk, moderate_risk)

        assert "Ergonomic assessment" in recommendations[0]
        assert "caffeine reduction" in recommendations[1]

    def test_no_risk_recommendations(self):
        """Test recommendations when no risk factors present."""
        from medical_diagnostic_agent.tools.patient_lookup import (
            _generate_risk_recommendations,
        )

        high_risk = []
        moderate_risk = []

        recommendations = _generate_risk_recommendations(high_risk, moderate_risk)

        assert len(recommendations) == 0
