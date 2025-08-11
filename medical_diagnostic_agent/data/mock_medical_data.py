"""
Mock medical data for demonstration purposes.
This is simplified medical knowledge for the take-home assignment.
"""

from typing import List, Set

# Common symptoms and their associated conditions
SYMPTOM_CONDITIONS = {
    "fever": ["common_cold", "flu", "infection", "covid"],
    "cough": ["common_cold", "flu", "bronchitis", "pneumonia", "covid"],
    "sore_throat": ["common_cold", "flu", "strep_throat"],
    "runny_nose": ["common_cold", "allergies", "flu"],
    "headache": ["tension_headache", "migraine", "flu", "dehydration"],
    "chest_pain": ["heart_attack", "angina", "muscle_strain", "anxiety"],
    "shortness_of_breath": ["asthma", "heart_attack", "pneumonia", "anxiety"],
    "nausea": ["food_poisoning", "flu", "migraine", "pregnancy"],
    "vomiting": ["food_poisoning", "flu", "migraine", "gastroenteritis"],
    "diarrhea": ["food_poisoning", "gastroenteritis", "ibs", "stress"],
    "fatigue": ["flu", "anemia", "depression", "sleep_deprivation"],
    "dizziness": ["dehydration", "low_blood_pressure", "inner_ear_problem"],
}

# Red flag symptoms that require immediate medical attention
RED_FLAG_SYMPTOMS = {
    "severe_chest_pain",
    "difficulty_breathing",
    "severe_abdominal_pain",
    "severe_headache",
    "loss_of_consciousness",
    "severe_bleeding",
    "signs_of_stroke",
    "severe_allergic_reaction",
}

# Condition information with descriptions and care recommendations
CONDITION_INFO = {
    "common_cold": {
        "description": "Viral upper respiratory infection",
        "care_level": "routine",
        "recommendations": [
            "Rest and hydration",
            "Over-the-counter medications for symptom relief",
            "See a doctor if symptoms worsen or last more than 10 days",
        ],
    },
    "flu": {
        "description": "Influenza viral infection",
        "care_level": "routine",
        "recommendations": [
            "Rest and hydration",
            "Antiviral medications if caught early",
            "Monitor for complications",
        ],
    },
    "heart_attack": {
        "description": "Acute myocardial infarction",
        "care_level": "emergency",
        "recommendations": [
            "Call 911 immediately",
            "Chew aspirin if not allergic",
            "Do not drive yourself to hospital",
        ],
    },
    "pneumonia": {
        "description": "Lung infection causing inflammation",
        "care_level": "urgent",
        "recommendations": [
            "See a doctor promptly",
            "May require antibiotics",
            "Monitor breathing and fever",
        ],
    },
    "anxiety": {
        "description": "Anxiety disorder with physical symptoms",
        "care_level": "routine",
        "recommendations": [
            "Practice relaxation techniques",
            "Consider counseling",
            "See primary care doctor for evaluation",
        ],
    },
}

# Symptom clarification questions
SYMPTOM_QUESTIONS = {
    "chest_pain": [
        "On a scale of 1-10, how severe is the pain?",
        "Does the pain radiate to your arm, jaw, or back?",
        "Is the pain crushing, sharp, or burning?",
        "Does physical activity make it worse?",
    ],
    "headache": [
        "On a scale of 1-10, how severe is the headache?",
        "Is this the worst headache you've ever had?",
        "Does light or sound make it worse?",
        "Do you have any visual changes?",
    ],
    "cough": [
        "Are you coughing up anything?",
        "Is the cough dry or productive?",
        "How long have you had the cough?",
        "Does it keep you awake at night?",
    ],
    "fever": [
        "What is your temperature?",
        "How long have you had the fever?",
        "Are you taking any fever-reducing medications?",
        "Do you have chills or sweats?",
    ],
}

# Age-based risk factors
AGE_RISK_FACTORS = {
    "pediatric": {"age_range": (0, 17), "risk_multiplier": 1.2},
    "adult": {"age_range": (18, 64), "risk_multiplier": 1.0},
    "elderly": {"age_range": (65, 120), "risk_multiplier": 1.5},
}


def get_conditions_for_symptoms(symptoms: List[str]) -> Set[str]:
    """Get possible conditions based on symptoms."""
    possible_conditions = set()
    for symptom in symptoms:
        if symptom in SYMPTOM_CONDITIONS:
            possible_conditions.update(SYMPTOM_CONDITIONS[symptom])
    return possible_conditions


def is_red_flag_symptom(symptom: str) -> bool:
    """Check if a symptom is a red flag requiring immediate attention."""
    return symptom.lower().replace(" ", "_") in RED_FLAG_SYMPTOMS


def get_care_level_for_condition(condition: str) -> str:
    """Get the recommended care level for a condition."""
    return CONDITION_INFO.get(condition, {}).get("care_level", "routine")
