"""
Standard clinical reference ranges used throughout the application.

Sources:
  - Glucose / HbA1c: American Diabetes Association Standards of Care 2024
  - BMI: WHO classification
  - Blood Pressure: JNC 8 / ACC-AHA 2017 guidelines
  - Total Cholesterol: ACC/AHA 2018 guidelines
"""

from typing import Dict, Any

REFERENCE_RANGES: Dict[str, Dict[str, Any]] = {
    "glucose": {
        "low": 70.0,
        "high": 99.0,
        "unit": "mg/dL",
        "label": "Fasting Glucose",
    },
    "hba1c": {
        "low": 4.0,
        "high": 5.6,
        "unit": "%",
        "label": "HbA1c",
    },
    "bmi": {
        "low": 18.5,
        "high": 24.9,
        "unit": "kg/m²",
        "label": "BMI",
    },
    "systolic_bp": {
        "low": 90.0,
        "high": 120.0,
        "unit": "mmHg",
        "label": "Systolic Blood Pressure",
    },
    "diastolic_bp": {
        "low": 60.0,
        "high": 80.0,
        "unit": "mmHg",
        "label": "Diastolic Blood Pressure",
    },
    "cholesterol": {
        "low": 0.0,
        "high": 200.0,
        "unit": "mg/dL",
        "label": "Total Cholesterol",
    },
}
