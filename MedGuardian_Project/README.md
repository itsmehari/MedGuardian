# MedGuardian

**AI-Assisted Early Disease Detection System** — a Streamlit web application that
parses PDF lab reports, extracts biomarker values (with OCR fallback for
scanned documents), and detects early disease risk from biomarkers
for diabetes, hypertension, and high cholesterol.

---

## Features

- Upload PDF lab reports (text-based; scanned PDFs not supported on Streamlit Cloud)
- Automatic extraction of glucose, HbA1c, BMI, blood pressure, and cholesterol
- Diabetes risk scoring using a weighted clinical formula
- Blood pressure classification (JNC 8 / ACC-AHA 2017)
- Cholesterol risk assessment (ACC/AHA 2018)
- Patient profile management (create, edit, delete)
- Historical trend charts with Plotly
- Data stored in SQLite (on Streamlit Cloud; no data sent to third parties)

---

## Deployment (Streamlit Cloud)

1. Push the project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** (or **Create app**), select your repo and branch.
4. Set **Main file path** to `MedGuardian_Project/app.py` (if the repo root is the parent of `MedGuardian_Project`).
5. In **Advanced settings** → **Secrets**, add:
   - `ADMIN_USERNAME`: your admin username
   - `ADMIN_PASSWORD_HASH`: SHA-256 hash of your password (see "Changing the Admin Password" below)
6. Deploy. Your app will be available at `https://<your-app-name>.streamlit.app`.
7. Default login: **admin / admin123** — change via secrets before going live.
8. **Note:** Tesseract OCR is not available on Streamlit Cloud; only text-based PDFs are supported. The database is ephemeral (resets on redeploy).

### Load Sample Demo Data

If the database is empty, an expander on the Home page offers **Load sample data**. Click it to seed sample patients and health records.

---

## Project Structure

```
MedGuardian_Project/
├── app.py                          # Streamlit entry point
├── config.py                       # Centralised configuration (reads .env)
├── requirements.txt
├── README.md
├── .env.example                    # Template for environment variables
│
├── database/
│   ├── __init__.py
│   └── db_handler.py               # SQLite connection + full CRUD layer
│
├── models/
│   ├── __init__.py
│   ├── diabetes_model.py           # Diabetes risk scoring formula
│   └── reference_ranges.py        # Clinical reference ranges
│
├── services/
│   ├── __init__.py
│   ├── auth.py                     # Session-state based authentication
│   ├── normalization_service.py    # Biomarker deviation normalisation
│   └── pdf_parser.py               # PDF text extraction + biomarker regex
│
└── pages/
    ├── 1_Patient_Profile.py        # Create / manage patient records
    ├── 2_Upload_Report.py          # Upload PDF and save health record
    ├── 3_Risk_Dashboard.py         # Compute and display risk scores
    └── 4_History.py                # Historical trends and charts
```

---

## Risk Score Interpretation

| Range | Level | Colour |
|---|---|---|
| 0 – 20 % | Low | Green |
| 21 – 50 % | Moderate | Orange |
| 51 – 100 % | High | Red |

### Diabetes Risk Formula

```
score = 0.4 × glucose_deviation
      + 0.4 × hba1c_deviation
      + 0.1 × bmi_modifier        # continuous, 0.0 at BMI=18.5 → 1.0 at BMI=40
      + 0.1 × family_history      # binary: 1 = first-degree relative diagnosed
```

Capped at 1.0. Reference ranges follow ADA Standards of Care 2024.

---

## Changing the Admin Password

```bash
python -c "import hashlib; print(hashlib.sha256(b'YourNewPassword').hexdigest())"
```

Copy the output and set `ADMIN_PASSWORD_HASH=<hash>` in your `.env` file,
then restart the app.
