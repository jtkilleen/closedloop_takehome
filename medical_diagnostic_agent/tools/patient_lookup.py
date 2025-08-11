"""
Patient lookup tools for accessing stored patient records and history.
"""

from typing import Any, Dict, List, Optional

from ..data.patient_records import (
    add_visit_note,
    create_new_patient,
    get_all_patients,
    get_patient_summary,
    search_patient_records,
    update_patient_record,
)


def lookup_patient_record(name: str) -> Dict[str, Any]:
    """
    Look up a patient's existing medical record by first name only.

    Args:
        name: Patient first name to search for (we only use first names)

    Returns:
        Dictionary containing patient record information or error message
    """
    if not name or not name.strip():
        return {
            "status": "error",
            "message": (
                "No patient name provided for lookup. "
                "Please provide your first name."
            ),
        }

    record = search_patient_records(name.strip())

    if not record:
        # Check if we have any patients and suggest alternatives
        all_patients = get_all_patients()
        return {
            "status": "not_found",
            "message": f"No record found for '{name}'.",
            "available_patients": all_patients,
            "suggestion": (
                "Please provide your first name. "
                "We only use first names in our system."
            ),
        }

    return {
        "status": "success",
        "patient_found": True,
        "record": record,
        "message": f"Found record for {record['name']}",
    }


def get_patient_medical_history(name: str) -> Dict[str, Any]:
    """
    Get detailed medical history and risk factors for a patient.

    Args:
        name: Patient name

    Returns:
        Dictionary containing medical history details
    """
    if not name or not name.strip():
        return {"status": "error", "message": "No patient name provided"}

    summary = get_patient_summary(name.strip())

    if not summary:
        return {
            "status": "not_found",
            "message": f"No medical history found for '{name}'",
        }

    return {
        "status": "success",
        "patient_name": summary["basic_info"]["name"],
        "age": summary["basic_info"]["age"],
        "occupation": summary["basic_info"]["occupation"],
        "medical_history": summary["medical_history"],
        "risk_factors": summary["risk_factors"],
        "lifestyle_factors": summary["lifestyle_factors"],
        "clinical_notes": summary["clinical_notes"],
        "previous_visits": summary["previous_visits_count"],
    }


def check_patient_risk_factors(name: str) -> Dict[str, Any]:
    """
    Check specific risk factors for a patient based on their record.

    Args:
        name: Patient name

    Returns:
        Dictionary containing risk factor analysis
    """
    record = search_patient_records(name.strip() if name else "")

    if not record:
        return {"status": "not_found", "message": f"No record found for '{name}'"}

    risk_factors = record.get("risk_factors", [])
    lifestyle = record.get("lifestyle", {})

    # Analyze risk factors
    high_risk_factors = []
    moderate_risk_factors = []

    for factor in risk_factors:
        if factor in ["smoking_history", "elderly", "chronic_sleep_deprivation"]:
            high_risk_factors.append(factor)
        else:
            moderate_risk_factors.append(factor)

    # Additional lifestyle-based risks
    lifestyle_risks = []
    if "sleep_pattern" in lifestyle and "5-6 hours" in str(lifestyle["sleep_pattern"]):
        lifestyle_risks.append("chronic_sleep_deprivation")

    if "smoking_history" in lifestyle:
        lifestyle_risks.append("former_smoker_status")

    return {
        "status": "success",
        "patient_name": record["name"],
        "age": record["age"],
        "high_risk_factors": high_risk_factors,
        "moderate_risk_factors": moderate_risk_factors,
        "lifestyle_risks": lifestyle_risks,
        "total_risk_factors": len(risk_factors),
        "recommendations": _generate_risk_recommendations(
            high_risk_factors, moderate_risk_factors
        ),
    }


def list_available_patients() -> Dict[str, Any]:
    """
    List all patients available in the system (first names only).

    Returns:
        Dictionary containing list of available patients
    """
    patients = get_all_patients()

    return {
        "status": "success",
        "total_patients": len(patients),
        "available_patients": patients,
        "message": (
            f"Found {len(patients)} patients in the system. "
            f"We only use first names: {', '.join(patients)}"
        ),
    }


def save_visit_summary(
    name: str, symptoms: List[str], assessment: str, recommendations: str
) -> Dict[str, Any]:
    """
    Save a visit summary to a patient's record.

    Args:
        name: Patient name
        symptoms: List of symptoms reported
        assessment: Clinical assessment
        recommendations: Care recommendations

    Returns:
        Dictionary indicating success or failure
    """
    if not name or not name.strip():
        return {"status": "error", "message": "No patient name provided"}

    visit_note = {
        "date": "current_visit",  # In real system, would use actual timestamp
        "symptoms": symptoms,
        "assessment": assessment,
        "recommendations": recommendations,
        "visit_type": "diagnostic_consultation",
    }

    success = add_visit_note(name.strip(), visit_note)

    if success:
        return {
            "status": "success",
            "message": f"Visit summary saved for {name}",
            "visit_saved": True,
        }
    else:
        return {
            "status": "error",
            "message": f"Could not save visit for '{name}' - patient not found",
            "visit_saved": False,
        }


def _generate_risk_recommendations(
    high_risk: List[str], moderate_risk: List[str]
) -> List[str]:
    """Generate recommendations based on risk factors."""
    recommendations = []

    if "smoking_history" in high_risk:
        recommendations.append("Continue smoking cessation support and monitoring")

    if "elderly" in high_risk:
        recommendations.append("Regular health screenings and fall prevention measures")

    if "chronic_sleep_deprivation" in high_risk:
        recommendations.append("Sleep hygiene counseling and stress management")

    if "sedentary_work" in moderate_risk:
        recommendations.append("Ergonomic assessment and regular movement breaks")

    if "high_caffeine_intake" in moderate_risk:
        recommendations.append("Gradual caffeine reduction and hydration counseling")

    return recommendations


def onboard_new_patient(
    name: str,
    age: int,
    occupation: str,
    lifestyle_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Onboard a new patient into the system.

    Args:
        name: Patient's first name
        age: Patient's age
        occupation: Patient's occupation
        lifestyle_info: Optional lifestyle information dictionary

    Returns:
        Dictionary containing onboarding result
    """
    if not name or not name.strip():
        return {"status": "error", "message": "Patient name is required for onboarding"}

    if age < 0 or age > 120:
        return {"status": "error", "message": "Age must be between 0 and 120"}

    if not occupation or not occupation.strip():
        return {"status": "error", "message": "Occupation is required for onboarding"}

    # Create new patient
    result = create_new_patient(
        name=name.strip(),
        age=age,
        occupation=occupation.strip(),
        lifestyle=lifestyle_info,
    )

    if result["status"] == "success":
        return {
            "status": "success",
            "message": f"Successfully onboarded {name} to the system",
            "patient": result["patient"],
            "next_steps": "You can now proceed with your medical consultation",
        }
    else:
        return result


def update_patient_lifestyle(
    name: str, lifestyle_updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a patient's lifestyle information.

    Args:
        name: Patient's first name
        lifestyle_updates: Dictionary containing lifestyle updates

    Returns:
        Dictionary indicating success or failure
    """
    if not name or not name.strip():
        return {"status": "error", "message": "Patient name is required"}

    # Check if patient exists
    record = search_patient_records(name.strip())
    if not record:
        return {
            "status": "not_found",
            "message": f"Patient '{name}' not found. Please onboard first.",
        }

    # Update lifestyle information
    updates = {"lifestyle": lifestyle_updates}
    result = update_patient_record(name.strip(), updates)

    return result
