# MedGuardian

**AI-Assisted Early Disease Detection System** — a Streamlit web application that
parses PDF lab reports, extracts biomarker values (with OCR fallback for
scanned documents), and detects early disease risk from biomarkers
for diabetes, hypertension, and high cholesterol.

---

## Features

- Upload PDF lab reports — text-based or scanned (via Tesseract OCR)
- Automatic extraction of glucose, HbA1c, BMI, blood pressure, and cholesterol
- Diabetes risk scoring using a weighted clinical formula
- Blood pressure classification (JNC 8 / ACC-AHA 2017)
- Cholesterol risk assessment (ACC/AHA 2018)
- Patient profile management (create, edit, delete)
- Historical trend charts with Plotly
- All data stored locally in SQLite — nothing leaves your machine

---

## Prerequisites

### 1. Python 3.10+

```bash
python --version
```

### 2. Tesseract OCR binary (required for scanned PDFs)

MedGuardian uses `pytesseract`, which is a Python wrapper around the
Tesseract OCR engine. You must install the engine separately.

**Windows**

1. Download the installer from the [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) page.
2. Run the installer (default path: `C:\Program Files\Tesseract-OCR\`).
3. Add the install directory to your `PATH`, **or** set the path explicitly
   in your `.env` file if needed.

**macOS**

```bash
brew install tesseract
```

**Ubuntu / Debian**

```bash
sudo apt-get install tesseract-ocr
```

---

## Installation

```bash
# 1. Clone or download the project
cd MedGuardian_Project

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the example environment file and edit it
copy .env.example .env      # Windows
cp .env.example .env        # macOS / Linux
```

Edit `.env` to set your credentials:

```
ADMIN_USERNAME=admin
# Generate a new hash: python -c "import hashlib; print(hashlib.sha256(b'YourPassword').hexdigest())"
ADMIN_PASSWORD_HASH=<your_hash_here>
```

---

## Running the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

Default login: **admin / admin123**  
**Change this before any real deployment.**

### Load Sample Demo Data

If the database is empty, an expander on the Home page offers **Load sample data**. Click it to seed sample patients and health records for demo/testing.

---

## Deploying to Streamlit Cloud

1. Push the project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select your repo and branch.
4. Set **Main file path** to `app.py` (ensure the app root is `MedGuardian_Project` or adjust the working directory).
5. In **Advanced settings**, add secrets:
   - `ADMIN_USERNAME`: your admin username
   - `ADMIN_PASSWORD_HASH`: SHA-256 hash of your password (see "Changing the Admin Password" below)
6. Deploy. The app will create `medguardian.db` in the container (ephemeral — data resets on redeploy).
7. **Note:** Tesseract OCR may not be available on Streamlit Cloud; scanned PDFs may fail. Text-based PDFs will work.

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
