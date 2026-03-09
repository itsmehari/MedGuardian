---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section {
    font-size: 28px;
  }
  h1 {
    color: #2c3e50;
  }
  h2 {
    color: #3498db;
  }
---

# MedGuardian
## AI Assisted Health Risk Insights

**B.Sc. Computer Science — Final Year Project**

**[Your Full Name]** | **[Guide Name]** | **[College Name]** | [2024 – 2025]

---

# Agenda

1. Introduction & Problem Statement
2. Objectives & Scope
3. System Architecture
4. Key Modules
5. Technology Stack
6. Risk Score Formulae
7. Demo & Results
8. Limitations & Future Work
9. Conclusion

---

# 1. Introduction

- Chronic conditions (diabetes, hypertension, cholesterol) need early risk detection
- Lab reports are PDFs — text-based or scanned
- Manual data entry is tedious and error-prone
- **MedGuardian** automates extraction and risk computation

---

# 2. Problem Statement

- Extract biomarker values from PDF lab reports
- Support both text-based and scanned PDFs (OCR)
- Compute standardised risk scores for diabetes, BP, cholesterol
- Track trends over time
- Store data locally (no cloud dependency)

---

# 3. Objectives

- Build a Streamlit web app for health risk insights
- Parse PDFs with pdfplumber + Tesseract OCR fallback
- Use regex to extract glucose, HbA1c, BMI, BP, cholesterol
- Apply clinical formulae (ADA, JNC 8, ACC/AHA)
- Provide gauges and trend charts (Plotly)

---

# 4. System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Streamlit UI   │────▶│  Services /      │────▶│   SQLite    │
│  (5 pages)      │     │  Models          │     │   Database  │
└─────────────────┘     └──────────────────┘     └─────────────┘
        │                         │
        │  PDF Upload             │  Risk Scores
        ▼                         ▼
┌─────────────────┐     ┌──────────────────┐
│  PDF Parser +   │     │  Diabetes / BP / │
│  OCR            │     │  Cholesterol     │
└─────────────────┘     └──────────────────┘
```

---

# 5. Key Modules

| Module | Function |
|--------|----------|
| Auth | Session-based login, SHA-256 password hash |
| Patient Profile | CRUD for patients |
| Upload Report | PDF → text → biomarkers → health record |
| Risk Dashboard | Compute & display risk scores |
| History | Trend charts for biomarkers & risk |

---

# 6. Risk Score Formulae

**Diabetes (0–100%):**
- 0.4×glucose_dev + 0.4×hba1c_dev + 0.1×BMI_mod + 0.1×family_history
- Ranges: 0–20% Low, 21–50% Moderate, 51–100% High

**Blood Pressure:** JNC 8 / ACC-AHA 2017

**Cholesterol:** ACC/AHA 2018 (<200, 200–239, ≥240 mg/dL)

---

# 7. Technology Stack

- **Python 3.10+**, **Streamlit**
- **SQLite** (local database)
- **pdfplumber**, **PyMuPDF**, **pytesseract**, **Pillow**
- **Plotly**, **pandas**, **numpy**

---

# 8. Demo & Results

- Patient profile creation
- PDF upload and biomarker extraction
- Risk dashboard with gauge charts
- History trends (Plotly)
- Sample data loader for empty DB

---

# 9. Limitations

- Tesseract must be installed separately
- Single admin user
- Regex may not cover all lab formats
- No EHR/API integration

---

# 10. Future Work

- More biomarkers (triglycerides, LDL, HDL)
- Multi-user roles
- Export to PDF
- Cloud deployment (Streamlit Cloud)
- Mobile responsiveness

---

# 11. Conclusion

MedGuardian delivers an **AI-assisted health risk insight** system that:
- Parses PDF lab reports (text + OCR)
- Extracts biomarkers automatically
- Computes clinically-grounded risk scores
- Stores data locally in SQLite
- Provides visualisation for trends

**Thank You**

---

# Q & A

**Contact:** [Your Full Name]  
**Roll No:** [Your Roll No]  
**Guide:** [Guide Name]
