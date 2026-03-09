# MedGuardian
## AI Assisted Health Risk Insights

**B.Sc. Computer Science — Final Year Project Report**

---

# Front Matter

## Title Page

**[College Name (Full)]**  
[College Address, City – PIN]

*(NAAC Accredited / Affiliated to [University Name])*

**Department of Computer Science**

---

### PROJECT REPORT

**On**

# MedGuardian: AI Assisted Health Risk Insights

*Submitted in partial fulfilment of the requirements for the award of the degree of*

**Bachelor of Science in Computer Science**

---

**Submitted by**  
**[Your Full Name]**  
Roll No. / Register No.: [Your Roll No]

**Under the guidance of**  
**[Guide Name]**  
[Guide Designation, Department of Computer Science]

**Academic Year:** [2024 – 2025]

---

## Bonafide Certificate

This is to certify that the project entitled **"MedGuardian: AI Assisted Health Risk Insights"** submitted by **[Your Full Name]** (Roll No. / Register No.: [Your Roll No]) in partial fulfilment of the requirements for the award of the degree of **Bachelor of Science in Computer Science** is a record of bonafide work carried out under my supervision and guidance.

This project has not been submitted elsewhere for the award of any other degree/diploma.

<br><br>

**[Guide Name]**  
[Guide Designation]  
Department of Computer Science

<br>

**Place:** [City]  
**Date:** [Date]

---

## Declaration

I hereby declare that the project entitled **"MedGuardian: AI Assisted Health Risk Insights"** submitted for the degree of **Bachelor of Science in Computer Science** is my original work. I have not submitted this project for any other degree or diploma at this or any other institution.

All sources of information have been duly acknowledged.

<br><br>

**[Your Full Name]**  
Roll No. / Register No.: [Your Roll No]  
Place: [City]  
Date: [Date]

---

## Acknowledgement

I would like to express my sincere gratitude to all those who contributed to the completion of this project.

I am deeply grateful to **[Guide Name]**, [Guide Designation], for his/her valuable guidance, constant encouragement, and constructive feedback throughout the project.

I thank the **Department of Computer Science** and the management of **[College Name]** for providing the necessary resources and facilities.

I extend my thanks to my family and friends for their support and patience during this endeavour.

<br><br>

**[Your Full Name]**

---

# Table of Contents

1. [Abstract](#abstract)
2. [List of Abbreviations](#list-of-abbreviations)
3. [Chapter 1: Introduction](#chapter-1-introduction)
4. [Chapter 2: System Study and Literature Review](#chapter-2-system-study-and-literature-review)
5. [Chapter 3: Requirements Analysis](#chapter-3-requirements-analysis)
6. [Chapter 4: System Design](#chapter-4-system-design)
7. [Chapter 5: System Modules](#chapter-5-system-modules)
8. [Chapter 6: Implementation](#chapter-6-implementation)
9. [Chapter 7: Datasets](#chapter-7-datasets)
10. [Chapter 8: Results](#chapter-8-results)
11. [Chapter 9: Limitations](#chapter-9-limitations)
12. [Chapter 10: Future Work](#chapter-10-future-work)
13. [Chapter 11: Business Model](#chapter-11-business-model)
14. [Chapter 12: Conclusion](#chapter-12-conclusion)
15. [References](#references)
16. [Appendices](#appendices)

---

# Abstract

**MedGuardian** is an AI-assisted health risk insight system that parses PDF lab reports, extracts biomarker values (with OCR fallback for scanned documents), and computes clinically-grounded health risk scores for diabetes, hypertension, and high cholesterol. The system is built as a Streamlit web application with a local SQLite database, ensuring that all data remains on the user's machine. Key features include automatic extraction of glucose, HbA1c, BMI, blood pressure, and cholesterol; diabetes risk scoring using a weighted clinical formula; blood pressure classification (JNC 8 / ACC-AHA 2017); cholesterol risk assessment (ACC/AHA 2018); and historical trend visualisation using Plotly. The project demonstrates the integration of document processing, clinical reference ranges, and risk modelling in a user-friendly healthcare analytics tool.

**Keywords:** Health risk assessment, PDF parsing, OCR, diabetes risk, hypertension, cholesterol, Streamlit, Python, SQLite

---

# List of Abbreviations

| Abbreviation | Full Form |
|--------------|-----------|
| ACC-AHA | American College of Cardiology – American Heart Association |
| ADA | American Diabetes Association |
| BMI | Body Mass Index |
| BP | Blood Pressure |
| CRUD | Create, Read, Update, Delete |
| CSV | Comma-Separated Values |
| DDL | Data Definition Language |
| HbA1c | Glycated Haemoglobin |
| JNC | Joint National Committee |
| NAAC | National Assessment and Accreditation Council |
| OCR | Optical Character Recognition |
| PDF | Portable Document Format |
| SQL | Structured Query Language |
| SQLite | SQL Lightweight Database |
| UI | User Interface |
| WHO | World Health Organization |

---

# Chapter 1: Introduction

## 1.1 Background

Chronic conditions such as diabetes, hypertension, and high cholesterol are major health concerns globally. Early identification of risk through routine lab reports can support preventive care. However, lab reports are often in PDF format—either text-based or scanned—and manual entry of biomarker values is tedious and error-prone.

## 1.2 Problem Statement

Healthcare providers and individuals need a simple tool to:
- Extract biomarker values from PDF lab reports automatically
- Compute standardised risk scores for diabetes, hypertension, and cholesterol
- Track trends over time
- Store data locally without sending it to external servers

## 1.3 Objectives

1. Build a web-based application that accepts PDF lab reports
2. Extract text using direct PDF parsing and OCR for scanned documents
3. Parse biomarkers using pattern matching (regular expressions)
4. Compute risk scores using clinically validated formulae
5. Provide a dashboard for visualising risk levels and trends
6. Store all data in a local SQLite database

## 1.4 Scope

- Supports text-based and scanned PDF lab reports
- Covers diabetes, hypertension, and cholesterol risk
- Single-user, admin-authenticated interface
- Local deployment (Streamlit + SQLite)

## 1.5 Organisation of the Report

The report is organised as follows: Chapter 2 discusses system study and literature review; Chapter 3 outlines requirements; Chapter 4 describes design; Chapter 5 covers modules; Chapter 6 presents implementation; Chapter 7 details datasets; Chapter 8 shows results; Chapter 9 discusses limitations; Chapter 10 outlines future work; Chapter 11 presents a business model; and Chapter 12 concludes the report.

---

# Chapter 2: System Study and Literature Review

## 2.1 Existing Systems

Several commercial and open-source tools exist for lab report management and risk assessment. Most are either enterprise EMR systems or standalone calculators. Few combine PDF parsing, OCR, and risk scoring in a single, locally deployable application.

## 2.2 Technology Overview

- **Streamlit:** Rapid prototyping and deployment of data apps in Python
- **SQLite:** Lightweight, file-based relational database
- **pdfplumber / PyMuPDF:** PDF text extraction and rendering
- **pytesseract:** OCR for scanned documents
- **Plotly:** Interactive charts for trends

## 2.3 Clinical Guidelines

- **Diabetes:** ADA Standards of Care 2024 for glucose and HbA1c reference ranges
- **Blood Pressure:** JNC 8 / ACC-AHA 2017 classification
- **Cholesterol:** ACC/AHA 2018 guidelines for total cholesterol thresholds

---

# Chapter 3: Requirements Analysis

## 3.1 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR1 | User shall log in with admin credentials |
| FR2 | User shall create, view, edit, and delete patient profiles |
| FR3 | User shall upload PDF lab reports |
| FR4 | System shall extract text from text-based PDFs using pdfplumber |
| FR5 | System shall use OCR (Tesseract) for scanned PDFs |
| FR6 | System shall parse glucose, HbA1c, BMI, BP, and cholesterol from extracted text |
| FR7 | User shall verify and correct parsed values before saving |
| FR8 | System shall compute diabetes risk score (0–100%) |
| FR9 | System shall classify blood pressure (Low/Moderate/High) |
| FR10 | System shall assess cholesterol risk (Low/Moderate/High) |
| FR11 | System shall display historical trends for biomarkers and risk scores |
| FR12 | All data shall be stored in SQLite locally |

## 3.2 Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR1 | Response time for PDF parsing < 30 seconds for typical reports |
| NFR2 | Passwords stored as SHA-256 hashes |
| NFR3 | SQL injection prevention via parameterised queries |
| NFR4 | No data sent to external servers |

## 3.3 Hardware and Software Requirements

**Hardware:** 4 GB RAM, 500 MB disk space  
**Software:** Python 3.10+, Tesseract OCR, modern web browser  
**Platform:** Windows / macOS / Linux; Streamlit Cloud for deployment

---

# Chapter 4: System Design

## 4.1 Architecture

MedGuardian follows a three-tier structure:

1. **Presentation:** Streamlit pages (Home, Patient Profile, Upload Report, Risk Dashboard, History)
2. **Business Logic:** Services (auth, PDF parser, normalisation) and models (diabetes risk, reference ranges)
3. **Data:** SQLite database with users, health_records, risk_scores, uploaded_reports

## 4.2 Database Schema

- **users:** user_id, name, age, gender, email, created_at
- **health_records:** record_id, user_id, test_date, glucose, hba1c, bmi, systolic_bp, diastolic_bp, cholesterol, created_at
- **risk_scores:** score_id, user_id, record_id, condition, risk_score, risk_level, computed_at
- **uploaded_reports:** report_id, user_id, filename, upload_time, status, extracted_text, record_id

## 4.3 Risk Score Design

**Diabetes Risk (0–1.0):**

- score = 0.4 × glucose_deviation + 0.4 × hba1c_deviation + 0.1 × bmi_modifier + 0.1 × family_history
- Capped at 1.0; interpreted as 0–20% Low, 21–50% Moderate, 51–100% High

**Blood Pressure:** JNC 8 / ACC-AHA thresholds (systolic/diastolic)  
**Cholesterol:** ACC/AHA 2018 (total cholesterol < 200, 200–239, ≥ 240 mg/dL)

---

# Chapter 5: System Modules

## 5.1 Authentication Module

Session-state based login. Credentials from `.env`; password hashed with SHA-256.

## 5.2 Patient Profile Module

CRUD for patients; stores active patient in `st.session_state["current_user_id"]`.

## 5.3 Upload Report Module

PDF upload → text extraction (pdfplumber / OCR) → biomarker regex parsing → user verification → save to health_records.

## 5.4 Risk Dashboard Module

Select patient and record → compute diabetes, BP, cholesterol risk → display gauge charts → save risk_scores.

## 5.5 History Module

Plotly line charts for risk scores and biomarker trends over time; table of uploaded reports.

---

# Chapter 6: Implementation

## 6.1 Technology Stack

- Python 3.10+, Streamlit, pandas, numpy, plotly
- pdfplumber, PyMuPDF, pytesseract, Pillow
- SQLite, python-dotenv

## 6.2 Key Implementation Details

- Biomarker parsing uses regex patterns for common lab-report formats
- Normalisation maps raw values to deviation scores using reference ranges
- Database uses foreign keys and CASCADE/SET NULL for referential integrity

## 6.3 Deployment

- Local: `streamlit run app.py`
- Streamlit Cloud: Connect GitHub repo, set secrets (ADMIN_PASSWORD_HASH, etc.)

---

# Chapter 7: Datasets

## 7.1 Sample Data

Two CSV files are provided:
- **sample_patients.csv:** name, age, gender, email
- **sample_health_records.csv:** user_id, test_date, glucose, hba1c, bmi, systolic_bp, diastolic_bp, cholesterol

## 7.2 Data Loader

The `utils.data_loader` module loads sample data when the database is empty. Format is documented in `data/DATASET_FORMAT.md`.

---

# Chapter 8: Results

## 8.1 Screenshots

*[Insert screenshots of: Home page, Patient Profile, Upload Report, Risk Dashboard, History charts]*

## 8.2 Test Cases

| Test | Expected | Result |
|------|----------|--------|
| Login with correct credentials | Access granted | ✓ |
| Upload text PDF | Biomarkers extracted | ✓ |
| Compute diabetes risk | Score 0–100% | ✓ |
| Empty DB + Load sample data | Patients and records loaded | ✓ |

---

# Chapter 9: Limitations

- Tesseract OCR must be installed separately; accuracy depends on scan quality
- Single admin user; no multi-tenancy
- PDF parsing patterns may not cover all lab report formats
- No integration with external health APIs or EHR systems

---

# Chapter 10: Future Work

- Support for more biomarkers (e.g., triglycerides, LDL, HDL)
- Multi-user roles (admin, clinician, patient)
- Export reports to PDF
- Integration with lab information systems
- Mobile-responsive design improvements

---

# Chapter 11: Business Model

MedGuardian can be offered as:
- **Open-source** tool for clinics and researchers
- **SaaS** version with cloud hosting and advanced analytics
- **On-premise** deployment for hospitals with strict data residency requirements

---

# Chapter 12: Conclusion

MedGuardian successfully implements an AI-assisted health risk insight system that parses PDF lab reports, extracts biomarkers, and computes diabetes, hypertension, and cholesterol risk scores. The application demonstrates practical use of document processing, clinical guidelines, and data visualisation. With sample datasets and a data loader, it supports demos and testing even when the database is empty. Future enhancements can extend biomarker coverage and integrate with enterprise health systems.

---

# References

1. Streamlit Documentation. (2024). *Streamlit Docs*. https://docs.streamlit.io/
2. Python Software Foundation. (2024). *Python 3.12 Documentation*. https://docs.python.org/3/
3. American Diabetes Association. (2024). *Standards of Care in Diabetes*. https://professional.diabetes.org/
4. Whelton, P. K., et al. (2017). *ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA Guideline for the Prevention, Detection, Evaluation, and Management of High Blood Pressure in Adults*. Journal of the American College of Cardiology.
5. Grundy, S. M., et al. (2018). *AHA/ACC/AACVPR/AAPA/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Blood Cholesterol*. Circulation.
6. SQLite. (2024). *SQLite Documentation*. https://www.sqlite.org/docs.html
7. NAAC. *National Assessment and Accreditation Council*. https://www.naac.gov.in/
8. [College Name]. *Official Website*. [College URL]

---

# Appendices

## Appendix A: Installation Steps

```bash
cd MedGuardian_Project
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env
# Edit .env with ADMIN_PASSWORD_HASH
streamlit run app.py
```

## Appendix B: Sample Biomarker Regex Patterns

- Glucose: `(?:fasting\s+)?glucose[^:\n]*?[:\s]+(\d+(?:\.\d+)?)`
- HbA1c: `hb\s*a1c[^:\n]*?[:\s]+(\d+(?:\.\d+)?)\s*%?`
- BMI: `\bbmi\b[^:\n]*?[:\s]+(\d+(?:\.\d+)?)`
- BP: systolic/diastolic patterns for mmHg

## Appendix C: Reference Ranges (Summary)

| Biomarker | Low | High | Unit |
|-----------|-----|------|------|
| Fasting Glucose | 70 | 99 | mg/dL |
| HbA1c | 4.0 | 5.6 | % |
| BMI | 18.5 | 24.9 | kg/m² |
| Systolic BP | 90 | 120 | mmHg |
| Diastolic BP | 60 | 80 | mmHg |
| Total Cholesterol | 0 | 200 | mg/dL |

---

*End of Report*
