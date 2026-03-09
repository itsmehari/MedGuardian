# MedGuardian Dataset Format

Sample CSV files for demo and testing. Use the data loader utility to seed an empty database.

---

## sample_patients.csv

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| name | string | Yes | Full name of the patient |
| age | integer | Yes | Age (1–120) |
| gender | string | Yes | Male / Female / Other / Prefer not to say |
| email | string | No | Unique email (leave blank or use unique values) |

---

## sample_health_records.csv

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| user_id | integer | Yes | Foreign key to users table (patient ID) |
| test_date | date | Yes | YYYY-MM-DD format |
| glucose | float | No | Fasting glucose in mg/dL |
| hba1c | float | No | HbA1c in % |
| bmi | float | No | Body Mass Index in kg/m² |
| systolic_bp | float | No | Systolic blood pressure in mmHg |
| diastolic_bp | float | No | Diastolic blood pressure in mmHg |
| cholesterol | float | No | Total cholesterol in mg/dL |

Use 0 or empty for missing values. The loader treats 0 as NULL for biomarker fields.

---

## Usage

Run from project root:

```bash
python -m utils.data_loader
```

Or call programmatically:

```python
from utils.data_loader import load_sample_data
load_sample_data()  # Seeds DB if empty
```
