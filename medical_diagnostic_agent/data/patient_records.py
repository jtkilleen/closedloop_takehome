"""
Patient records database for storing and retrieving patient information.
This allows the medical diagnostic agent to access previous patient notes and history.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# Path to the JSON file
PATIENTS_JSON_PATH = Path(__file__).parent / "patients.json"


def load_patient_records() -> Dict[str, Any]:
    """
    Load patient records from JSON file.

    Returns:
        Dictionary containing patient records
    """
    try:
        with open(PATIENTS_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("patients", {})
    except FileNotFoundError:
        print(f"Warning: Patient records file not found at {PATIENTS_JSON_PATH}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error reading patient records: {e}")
        return {}


def save_patient_records(patients: Dict[str, Any]) -> bool:
    """
    Save patient records to JSON file.

    Args:
        patients: Dictionary containing patient records

    Returns:
        True if successful, False otherwise
    """
    try:
        data = {"patients": patients}
        with open(PATIENTS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving patient records: {e}")
        return False


# Load patient records from JSON
PATIENT_RECORDS = load_patient_records()


def search_patient_records(name: str) -> Optional[Dict[str, Any]]:
    """
    Search for a patient record by name.

    Args:
        name: Patient name to search for

    Returns:
        Patient record dictionary if found, None otherwise
    """
    if not name:
        return None

    # Normalize name for searching
    normalized_name = name.lower().strip()

    # Direct lookup
    if normalized_name in PATIENT_RECORDS:
        return PATIENT_RECORDS[normalized_name]

    # Partial name matching
    for patient_key, record in PATIENT_RECORDS.items():
        if normalized_name in patient_key or normalized_name in record["name"].lower():
            return record

    return None


def get_all_patients() -> List[str]:
    """
    Get list of all patient names in the system.

    Returns:
        List of patient names
    """
    return [record["name"] for record in PATIENT_RECORDS.values()]


def add_visit_note(name: str, visit_note: Dict[str, Any]) -> bool:
    """
    Add a visit note to a patient's record.

    Args:
        name: Patient name
        visit_note: Dictionary containing visit information

    Returns:
        True if successful, False if patient not found
    """
    normalized_name = name.lower().strip()

    if normalized_name in PATIENT_RECORDS:
        PATIENT_RECORDS[normalized_name]["previous_visits"].append(visit_note)
        return True

    return False


def get_patient_summary(name: str) -> Optional[Dict[str, Any]]:
    """
    Get a comprehensive summary of a patient's record.

    Args:
        name: Patient name

    Returns:
        Formatted patient summary or None if not found
    """
    record = search_patient_records(name)

    if not record:
        return None

    summary = {
        "basic_info": {
            "name": record["name"],
            "age": record["age"],
            "occupation": record["occupation"],
        },
        "lifestyle_factors": record["lifestyle"],
        "medical_history": record["medical_history"],
        "risk_factors": record["risk_factors"],
        "clinical_notes": record["notes"],
        "previous_visits_count": len(record["previous_visits"]),
    }

    return summary


def create_new_patient(
    name: str, age: int, occupation: str, lifestyle: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Create a new patient record.

    Args:
        name: Patient's first name
        age: Patient's age
        occupation: Patient's occupation
        lifestyle: Optional lifestyle information

    Returns:
        Dictionary containing the new patient record
    """
    normalized_name = name.lower().strip()

    # Check if patient already exists
    if normalized_name in PATIENT_RECORDS:
        return {
            "status": "error",
            "message": f"Patient '{name}' already exists in the system",
        }

    # Create new patient record
    new_patient = {
        "name": name.strip(),
        "age": age,
        "occupation": occupation,
        "lifestyle": lifestyle or {},
        "medical_history": [],
        "risk_factors": [],
        "previous_visits": [],
        "notes": f"New patient - {name}, {age}, {occupation}",
    }

    # Add to records
    PATIENT_RECORDS[normalized_name] = new_patient

    # Save to JSON file
    if save_patient_records(PATIENT_RECORDS):
        return {
            "status": "success",
            "message": f"Successfully created new patient record for {name}",
            "patient": new_patient,
        }
    else:
        return {
            "status": "error",
            "message": f"Created patient record for {name} but failed to save to file",
        }


def update_patient_record(name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing patient record.

    Args:
        name: Patient's first name
        updates: Dictionary containing fields to update

    Returns:
        Dictionary indicating success or failure
    """
    normalized_name = name.lower().strip()

    if normalized_name not in PATIENT_RECORDS:
        return {
            "status": "error",
            "message": f"Patient '{name}' not found in the system",
        }

    # Update the record
    for key, value in updates.items():
        if key in PATIENT_RECORDS[normalized_name]:
            PATIENT_RECORDS[normalized_name][key] = value

    # Save to JSON file
    if save_patient_records(PATIENT_RECORDS):
        return {
            "status": "success",
            "message": f"Successfully updated patient record for {name}",
            "patient": PATIENT_RECORDS[normalized_name],
        }
    else:
        return {
            "status": "error",
            "message": f"Updated patient record for {name} but failed to save to file",
        }
