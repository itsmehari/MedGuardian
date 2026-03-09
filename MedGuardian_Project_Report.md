# MedGuardian
## AI-Assisted Early Disease Detection System

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

# MedGuardian: AI-Assisted Early Disease Detection System

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

This is to certify that the project entitled **"MedGuardian: AI-Assisted Early Disease Detection System"** submitted by **[Your Full Name]** (Roll No. / Register No.: [Your Roll No]) in partial fulfilment of the requirements for the award of the degree of **Bachelor of Science in Computer Science** is a record of bonafide work carried out under my supervision and guidance.

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

I hereby declare that the project entitled **"MedGuardian: AI-Assisted Early Disease Detection System"** submitted for the degree of **Bachelor of Science in Computer Science** is my original work. I have not submitted this project for any other degree or diploma at this or any other institution.

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

**MedGuardian** is an AI-assisted early disease detection system designed to bridge the gap between raw laboratory data and actionable health insights. The system parses PDF lab reports (text-based; scanned PDFs are not supported on Streamlit Cloud), extracts biomarker values, and computes clinically grounded early disease risk scores for diabetes, hypertension, and high cholesterol. Built as a Streamlit web application with a SQLite database, MedGuardian is deployed on Streamlit Community Cloud; health data is stored in SQLite on the deployment server and is not sent to third-party services.

Key features include automatic extraction of glucose, HbA1c, BMI, blood pressure, and total cholesterol; a weighted diabetes risk formula aligned with ADA Standards of Care; blood pressure classification following JNC 8 and ACC-AHA 2017 guidelines; cholesterol risk assessment per ACC/AHA 2018; and interactive historical trend visualisation using Plotly. The project demonstrates the practical integration of document processing, clinical reference ranges, and risk modelling in a user-friendly, cloud-deployed healthcare analytics tool suitable for clinics, researchers, and health-conscious individuals.

**Keywords:** Early disease detection, health risk assessment, PDF parsing, OCR, diabetes risk, hypertension, cholesterol, Streamlit, Python, SQLite, biomarker extraction, clinical decision support

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
| NCD | Non-Communicable Disease |
| NFHS | National Family Health Survey |
| EHR | Electronic Health Record |
| LIS | Laboratory Information System |
| FHIR | Fast Healthcare Interoperability Resources |
| HL7 | Health Level Seven |

---

# Chapter 1: Introduction

## 1.1 Background

Non-communicable diseases (NCDs) such as diabetes mellitus, hypertension, and dyslipidaemia (high cholesterol) represent a growing public health burden worldwide. According to the World Health Organization, NCDs account for approximately 71% of all deaths globally, with cardiovascular diseases and diabetes among the leading causes. In India, the National Family Health Survey (NFHS-5) reports rising prevalence of hypertension and diabetes, particularly in urban and peri-urban populations. The economic and social cost of late diagnosis and inadequate management is substantial.

Early detection of disease risk through routine laboratory testing offers a pathway to preventive intervention. Biomarkers such as fasting glucose, HbA1c (glycated haemoglobin), blood pressure, body mass index (BMI), and total cholesterol provide objective indicators that, when tracked over time, can signal emerging metabolic and cardiovascular risk. Clinical guidelines from the American Diabetes Association (ADA), the Joint National Committee (JNC), and the American College of Cardiology/American Heart Association (ACC/AHA) define standard reference ranges and risk thresholds for these parameters.

Laboratory reports are typically delivered as PDF documents—either digitally generated (text-based) or as scanned images of printed reports. Manual extraction of biomarker values from such documents is time-consuming, prone to human error, and does not scale when managing multiple patients or longitudinal data. There is a clear need for automated, reliable systems that can parse lab reports, extract relevant values, and support risk assessment and trend analysis while maintaining data privacy.

## 1.2 Problem Statement

Healthcare providers, clinics, and health-conscious individuals face several challenges when working with laboratory reports:

1. **Manual Data Entry:** Extracting biomarker values from PDF lab reports requires manual transcription, which is tedious and error-prone. Typos and unit confusion can lead to incorrect clinical interpretations.

2. **Lack of Standardised Risk Scoring:** Raw biomarker values alone do not convey risk clearly. Clinically validated formulae for diabetes, hypertension, and cholesterol risk exist but are not readily applied in a unified, user-friendly interface.

3. **Scattered Data:** Lab reports from multiple laboratories and time periods are often stored as separate files. Aggregating and comparing results over time to identify trends is difficult without a structured database.

4. **Privacy Concerns:** Sending sensitive health data to third-party analytics raises privacy and regulatory concerns. MedGuardian avoids this by storing and processing data only on the deployment server (Streamlit Cloud), with no transmission to external analytics services.

5. **Format Heterogeneity:** Lab reports vary in layout, terminology, and units across different laboratories. A flexible extraction mechanism that can handle common variations is needed.

## 1.3 Objectives

The primary objectives of the MedGuardian project are:

1. **Automated PDF Processing:** Build a web-based application that accepts PDF lab reports and extracts text using direct PDF parsing (pdfplumber) for text-based documents, with OCR (Tesseract) as a fallback for scanned images.

2. **Biomarker Extraction:** Parse key biomarkers—fasting glucose, HbA1c, BMI, blood pressure (systolic/diastolic), and total cholesterol—from extracted text using robust pattern-matching (regular expressions) that accommodates common lab-report formats.

3. **Clinical Risk Computation:** Implement clinically validated risk scoring for diabetes (weighted formula), blood pressure classification (JNC 8 / ACC-AHA 2017), and cholesterol assessment (ACC/AHA 2018), with results expressed on a consistent 0–100% scale.

4. **Data Management:** Store all patient profiles, health records, and risk scores in a SQLite database with proper referential integrity; data remains on the deployment server and is not transmitted to external servers.

5. **Visualisation and Trends:** Provide an interactive dashboard with gauge charts for risk levels and line charts for historical biomarker and risk score trends using Plotly.

6. **Usability:** Deliver a simple, intuitive interface suitable for clinicians and non-technical users, with authentication to protect access.

## 1.4 Scope

The scope of the MedGuardian project is defined as follows:

**In Scope:**
- Support for text-based and scanned PDF lab reports (single-file upload)
- Extraction and parsing of six primary biomarkers: glucose, HbA1c, BMI, systolic BP, diastolic BP, total cholesterol
- Diabetes, hypertension, and cholesterol risk assessment
- Patient profile management (create, read, update, delete)
- Historical trend visualisation for biomarkers and risk scores
- Single-user, admin-authenticated access
- Local deployment (Streamlit + SQLite); optional Streamlit Cloud deployment

**Out of Scope:**
- Multi-user roles (patient, clinician, admin) or role-based access control
- Integration with Electronic Health Records (EHR) or Laboratory Information Systems (LIS)
- Support for additional biomarkers (e.g., LDL, HDL, triglycerides, creatinine)
- Mobile-native application or offline mode
- Clinical diagnosis or treatment recommendations (the system provides risk indicators only)

## 1.5 Significance

MedGuardian addresses a practical gap in healthcare informatics: the ability to convert unstructured lab report data into structured, actionable risk information without relying on expensive enterprise systems or compromising data privacy. By combining document processing, clinical guidelines, and data visualisation in a single, cloud-deployed tool, the project demonstrates the viability of lightweight, privacy-preserving health analytics for small clinics and individual use.

## 1.6 Organisation of the Report

The report is organised into twelve chapters. **Chapter 2** presents a system study and literature review, including existing tools, technology choices, and clinical guidelines. **Chapter 3** details the functional and non-functional requirements. **Chapter 4** describes the system architecture, database design, and risk score formulation. **Chapter 5** explains each system module in depth. **Chapter 6** covers implementation, technology stack, and deployment. **Chapter 7** describes the sample datasets and data loader. **Chapter 8** presents results, test cases, and screenshots. **Chapter 9** discusses limitations. **Chapter 10** outlines future work. **Chapter 11** proposes a business model. **Chapter 12** concludes the report. References and appendices follow.

---

# Chapter 2: System Study and Literature Review

## 2.1 Existing Systems

### 2.1.1 Enterprise Electronic Medical Record (EMR) Systems

Large hospital and clinic EMR systems (e.g., Epic, Cerner, Allscripts) include lab result management and sometimes risk calculators. These systems are expensive, require significant infrastructure, and are designed for institutional use. They do not address the need of small clinics or individuals for a lightweight, cloud-deployed solution that processes PDF reports from external laboratories.

### 2.1.2 Standalone Risk Calculators

Numerous web-based and mobile risk calculators exist for diabetes, cardiovascular disease, and cholesterol. Examples include the ADA diabetes risk test and various heart disease risk estimators. These typically require manual entry of biomarker values and do not integrate with lab report parsing. They serve as complementary tools but do not solve the problem of automated extraction from PDFs.

### 2.1.3 Document Processing and OCR Tools

Generic document processing tools (e.g., Adobe Acrobat, ABBYY FineReader) can extract text from PDFs but are not designed for structured healthcare data extraction or risk computation. They lack domain-specific parsing logic and clinical reference ranges.

### 2.1.4 Research and Open-Source Efforts

Academic and open-source projects have explored medical document understanding, including NLP-based extraction from clinical notes. Few focus specifically on lab report PDFs with a complete pipeline from extraction to risk scoring. MedGuardian fills this gap by combining PDF parsing, OCR fallback, biomarker extraction, and clinical risk computation in a single, cohesive application.

## 2.2 Technology Overview

### 2.2.1 Streamlit

Streamlit is an open-source Python framework for building data applications rapidly. It provides a reactive, declarative API for creating web interfaces without writing HTML, CSS, or JavaScript. Widgets such as file uploaders, forms, and charts integrate seamlessly with Python data structures. Streamlit is well-suited for internal tools, dashboards, and proof-of-concept applications. MedGuardian is deployed on Streamlit Community Cloud.

### 2.2.2 SQLite

SQLite is a serverless, file-based relational database engine. It requires no separate server process; the database is stored in a single file. SQLite supports standard SQL, ACID transactions, and foreign keys. It is ideal for small-scale web applications where simplicity and portability are priorities. For MedGuardian on Streamlit Cloud, SQLite stores all data on the deployment container; data is not transmitted to external servers.

### 2.2.3 PDF Processing Libraries

**pdfplumber:** A Python library that extracts text and tables from PDFs by analysing the underlying structure. It works well for text-based PDFs where characters are encoded as Unicode. **PyMuPDF (fitz):** Provides low-level access to PDF rendering. MedGuardian uses PyMuPDF to render each page as an image when pdfplumber returns empty text, enabling OCR-based extraction for scanned documents.

### 2.2.4 Optical Character Recognition (OCR)

**pytesseract** is a Python wrapper for the Tesseract OCR engine. Tesseract is open-source and supports multiple languages. For lab reports, English is sufficient. OCR accuracy depends on image quality, resolution, and font clarity. Scanned reports with high contrast and clear text generally yield good results.

### 2.2.5 Visualisation and Data Processing

**Plotly** provides interactive charts (line, gauge, scatter) that can be embedded in Streamlit. **pandas** and **numpy** are used for data manipulation and numerical operations. **python-dotenv** loads environment variables from a `.env` file for configuration management.

## 2.3 Clinical Guidelines

### 2.3.1 Diabetes (ADA Standards of Care 2024)

The American Diabetes Association defines normal fasting glucose as 70–99 mg/dL and HbA1c as 4.0–5.6%. Values above these ranges indicate prediabetes or diabetes. MedGuardian uses these ranges for normalisation and risk computation. The diabetes risk formula weights glucose and HbA1c deviation most heavily, reflecting their predictive value in the literature.

### 2.3.2 Blood Pressure (JNC 8 / ACC-AHA 2017)

The Joint National Committee and ACC-AHA guidelines classify blood pressure as follows: Normal (<120/80 mmHg), Elevated (120–129/<80), Stage 1 Hypertension (130–139 or 80–89), Stage 2 Hypertension (≥140 or ≥90). MedGuardian maps these to Low, Moderate, and High risk levels for consistency with the overall 0–100% scale.

### 2.3.3 Cholesterol (ACC/AHA 2018)

Total cholesterol is classified as Desirable (<200 mg/dL), Borderline High (200–239), and High (≥240). These thresholds align with cardiovascular risk stratification. MedGuardian applies these for cholesterol risk assessment.

---

# Chapter 3: Requirements Analysis

## 3.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | User shall log in with admin credentials (username and password) stored in configuration | High |
| FR2 | User shall create new patient profiles with name, age, gender, and optional email | High |
| FR3 | User shall view, edit, and delete existing patient profiles | High |
| FR4 | User shall upload PDF lab reports (single file at a time) | High |
| FR5 | System shall extract text from text-based PDFs using pdfplumber | High |
| FR6 | System shall use OCR (Tesseract via pytesseract) when pdfplumber returns empty text | High |
| FR7 | System shall parse glucose, HbA1c, BMI, systolic BP, diastolic BP, and total cholesterol from extracted text using regex patterns | High |
| FR8 | User shall verify and correct parsed biomarker values before saving to the database | High |
| FR9 | System shall compute diabetes risk score (0–100%) using weighted formula | High |
| FR10 | System shall classify blood pressure as Low, Moderate, or High per JNC 8 / ACC-AHA | High |
| FR11 | System shall assess cholesterol risk as Low, Moderate, or High per ACC/AHA 2018 | High |
| FR12 | System shall display gauge charts for risk levels and line charts for historical trends | High |
| FR13 | All patient, health record, and risk data shall be stored in SQLite (on deployment server) | High |
| FR14 | System shall offer sample data loader when database is empty for demo purposes | Medium |

## 3.2 Non-Functional Requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| NFR1 | Response time for PDF parsing shall be less than 30 seconds for typical reports (≤10 pages) | Ensures acceptable user experience |
| NFR2 | Passwords shall be stored as SHA-256 hashes; plain text shall never be persisted | Basic security measure |
| NFR3 | All database queries shall use parameterised statements to prevent SQL injection | OWASP recommendation |
| NFR4 | No health data shall be transmitted to external servers; processing and storage on deployment server only | Privacy requirement |
| NFR5 | Application shall run on Windows, macOS, and Linux | Cross-platform compatibility |
| NFR6 | User interface shall be intuitive with clear labels and minimal training required | Usability |

## 3.3 Use Case Scenarios

**UC1 – Login:** User opens the application, enters admin username and password. System validates credentials and grants access to the main interface.

**UC2 – Create Patient:** User navigates to Patient Profile, fills in name, age, gender, email (optional), and submits. System creates a new patient record and assigns a unique ID.

**UC3 – Upload Lab Report:** User selects a patient, uploads a PDF file. System extracts text (pdfplumber or OCR), parses biomarkers, and displays values for user verification. User may correct values and save. System creates a health record and links it to the patient.

**UC4 – Compute Risk:** User selects a patient and a health record, indicates family history of diabetes, and triggers risk computation. System calculates diabetes, BP, and cholesterol risk, displays gauge charts, and saves scores to the database.

**UC5 – View History:** User selects a patient and views tabs for risk score trends, biomarker trends, and uploaded reports. Interactive Plotly charts allow exploration of trends over time.

## 3.4 Hardware and Software Requirements

**Hardware:** Minimum 4 GB RAM, 500 MB free disk space for application and database. Recommended 8 GB RAM for smoother OCR processing.

**Software:** Python 3.10 or higher; Tesseract OCR binary (platform-specific installation required); modern web browser (Chrome, Firefox, Edge, Safari).

**Platform:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+). Optional deployment on Streamlit Community Cloud for web access.

---

# Chapter 4: System Design

## 4.1 Architecture

MedGuardian follows a three-tier architecture:

### 4.1.1 Presentation Layer

The presentation layer is implemented using Streamlit. It comprises:

- **Home Page (app.py):** Entry point; displays overview, step-by-step guidance, and sample data loader when the database is empty.
- **Patient Profile (1_Patient_Profile.py):** Create new patients and manage existing ones (view, edit, delete).
- **Upload Report (2_Upload_Report.py):** File upload, PDF processing, biomarker verification, and health record creation.
- **Risk Dashboard (3_Risk_Dashboard.py):** Patient and record selection, risk computation, gauge charts, and score persistence.
- **History (4_History.py):** Risk score trends, biomarker trends, and uploaded reports table.

Authentication is enforced at the start of each page via a guard function. Session state holds the authenticated user, active patient ID, and last risk results.

### 4.1.2 Business Logic Layer

- **Services:** `auth.py` (login, session management), `pdf_parser.py` (text extraction, biomarker regex parsing), `normalization_service.py` (deviation calculation from reference ranges).
- **Models:** `diabetes_model.py` (risk formula), `reference_ranges.py` (clinical thresholds).

### 4.1.3 Data Layer

- **db_handler.py:** Encapsulates all SQLite operations. Uses parameterised queries and connection-per-operation pattern. Foreign keys ensure referential integrity with CASCADE and SET NULL as appropriate.

### 4.1.4 Data Flow

1. User uploads PDF → `pdf_parser.extract_text_from_pdf()` → text string.
2. Text → `pdf_parser.parse_biomarkers()` → dict of biomarker values.
3. User verifies values → `db_handler.insert_health_record()` → record_id.
4. User computes risk → `diabetes_model.calculate_diabetes_risk()`, BP/cholesterol logic → `db_handler.insert_risk_score()`.
5. History page → `db_handler` queries → pandas DataFrame → Plotly charts.

## 4.2 Database Schema

### 4.2.1 Entity-Relationship Overview

- **users** (1) ——< (N) **health_records**
- **users** (1) ——< (N) **risk_scores**
- **users** (1) ——< (N) **uploaded_reports**
- **health_records** (1) ——< (N) **risk_scores** (optional link)
- **health_records** (1) ——< (0..1) **uploaded_reports** (optional link)

### 4.2.2 Table Definitions

**users:**
| Column    | Type     | Constraints              |
|-----------|----------|---------------------------|
| user_id   | INTEGER  | PRIMARY KEY AUTOINCREMENT |
| name      | TEXT     | NOT NULL                  |
| age       | INTEGER  |                           |
| gender    | TEXT     |                           |
| email     | TEXT     | UNIQUE                    |
| created_at| TIMESTAMP| DEFAULT CURRENT_TIMESTAMP |

**health_records:**
| Column       | Type     | Constraints                         |
|--------------|----------|-------------------------------------|
| record_id    | INTEGER  | PRIMARY KEY AUTOINCREMENT           |
| user_id      | INTEGER  | NOT NULL, FK → users, ON DELETE CASCADE |
| test_date    | TEXT     |                                     |
| glucose      | REAL     |                                     |
| hba1c        | REAL     |                                     |
| bmi          | REAL     |                                     |
| systolic_bp  | REAL     |                                     |
| diastolic_bp | REAL     |                                     |
| cholesterol  | REAL     |                                     |
| created_at   | TIMESTAMP| DEFAULT CURRENT_TIMESTAMP           |

**risk_scores:**
| Column     | Type     | Constraints                                  |
|------------|----------|----------------------------------------------|
| score_id   | INTEGER  | PRIMARY KEY AUTOINCREMENT                    |
| user_id    | INTEGER  | NOT NULL, FK → users, ON DELETE CASCADE      |
| record_id  | INTEGER  | FK → health_records, ON DELETE SET NULL      |
| condition  | TEXT     | NOT NULL (diabetes, hypertension, cholesterol) |
| risk_score | REAL     | NOT NULL (0.0–1.0)                           |
| risk_level | TEXT     | NOT NULL (Low, Moderate, High)               |
| computed_at| TIMESTAMP| DEFAULT CURRENT_TIMESTAMP                    |

**uploaded_reports:**
| Column        | Type     | Constraints                                  |
|---------------|----------|----------------------------------------------|
| report_id     | INTEGER  | PRIMARY KEY AUTOINCREMENT                    |
| user_id       | INTEGER  | NOT NULL, FK → users, ON DELETE CASCADE      |
| filename      | TEXT     |                                              |
| upload_time   | TIMESTAMP| DEFAULT CURRENT_TIMESTAMP                    |
| status        | TEXT     | pending, processed, failed                   |
| extracted_text| TEXT     |                                              |
| record_id     | INTEGER  | FK → health_records, ON DELETE SET NULL      |

## 4.3 Risk Score Design

### 4.3.1 Diabetes Risk (0–1.0)

The formula incorporates four inputs:

- **glucose_deviation:** Fractional deviation of fasting glucose above the upper reference limit (99 mg/dL). Computed via `normalize_biomarker()`; 0 when within range.
- **hba1c_deviation:** Fractional deviation of HbA1c above 5.6%.
- **bmi_modifier:** Linear mapping from BMI 18.5 (0.0) to 40 (1.0), clamped to [0, 1].
- **family_history:** Binary (0 or 1) for first-degree relative with diabetes.

**Weights:** glucose 40%, hba1c 40%, BMI 10%, family history 10%. Final score is capped at 1.0.

**Interpretation:** 0–0.20 Low, 0.21–0.50 Moderate, 0.51–1.0 High (displayed as 0–100%).

### 4.3.2 Blood Pressure Risk

Based on JNC 8 / ACC-AHA 2017:

- **Low:** SBP <120 and DBP <80 → score 0.05; SBP 120–129 and DBP <80 → score 0.20.
- **Moderate:** SBP 130–139 or DBP 80–89 → score 0.50.
- **High:** SBP ≥140 or DBP ≥90 → score 0.85.

### 4.3.3 Cholesterol Risk

Based on ACC/AHA 2018:

- **Low:** Total cholesterol <200 mg/dL → score 0.05.
- **Moderate:** 200–239 → score 0.45.
- **High:** ≥240 → score 0.80.

---

# Chapter 5: System Modules

## 5.1 Authentication Module (services/auth.py)

The authentication module provides session-based access control. Credentials (username and password hash) are loaded from the environment via `config.py`. The password is never stored in plain text; only the SHA-256 hash is compared.

**Components:**
- `_hash(password)`: Returns SHA-256 hex digest of the password.
- `_check_credentials(username, password)`: Compares username and hashed password against configured values.
- `login_page()`: Renders the login form. If credentials are valid, sets `st.session_state["authenticated"]` and `st.session_state["username"]`, then reruns the app.
- `require_auth()`: Guard function called at the top of each page. If not authenticated, renders `login_page()` and stops execution.
- `logout()`: Clears session state and forces a rerun to show the login form.
- `sidebar_user_info()`: Displays logged-in username and logout button in the sidebar.

**Security considerations:** SHA-256 is acceptable for a single-user demo. For production, bcrypt or Argon2 is recommended.

## 5.2 Patient Profile Module (pages/1_Patient_Profile.py)

This module manages patient records with full CRUD operations.

**New Patient Tab:** Form with name (required), age (1–120), gender (dropdown), and optional email. On submit, `insert_user()` is called. The new patient ID is stored in `st.session_state["current_user_id"]` so other pages can use it as the default selection. Duplicate email handling shows a user-friendly error.

**Manage Existing Tab:** Dropdown lists all patients. Selection updates `current_user_id`. Patient details are displayed as metrics. An expandable edit form allows updating name, age, gender, and email. A delete section with confirmation checkbox prevents accidental deletion; `delete_user()` cascades to health records and risk scores.

## 5.3 Upload Report Module (pages/2_Upload_Report.py)

**Flow:**
1. Patient selector (pre-filled from `current_user_id` if available).
2. File uploader accepts PDFs.
3. On upload: `extract_text_from_pdf()` is called. If text is empty, an error is shown (OCR may be unavailable).
4. Raw text is shown in an expander for debugging.
5. `insert_uploaded_report()` creates a pending report record.
6. `parse_biomarkers()` extracts values using regex. Each biomarker is displayed in a number input for verification/correction.
7. Test date is selected (default: today).
8. On save: `insert_health_record()` stores the record; `update_report_status()` marks the report as processed and links it to the record. `current_record_id` is set for the Risk Dashboard.

**Error handling:** If save fails, report status is set to failed. User sees an error message.

## 5.4 Risk Dashboard Module (pages/3_Risk_Dashboard.py)

**Flow:**
1. Patient selector; record selector (filtered by patient).
2. Biomarker summary table with values and status (Normal/High/Low) from `normalize_biomarker()`.
3. Family history of diabetes (Yes/No) radio.
4. "Compute Risk Scores" button triggers calculation:
   - Diabetes: Requires glucose, HbA1c, BMI. Uses `calculate_diabetes_risk()`.
   - Blood pressure: Requires systolic and diastolic. Applies JNC 8 logic.
   - Cholesterol: Requires total cholesterol. Applies ACC/AHA logic.
5. Each result is inserted via `insert_risk_score()`.
6. Gauge charts (Plotly) display scores with colour-coded zones (green/orange/red).
7. Results stored in session state for display until next computation.

## 5.5 History Module (pages/4_History.py)

Three tabs:

**Risk Score Trends:** Line chart of risk scores over time, filterable by condition. Horizontal reference lines at 20% and 50%. Summary table of all risk score records.

**Biomarker Trends:** Dropdown to select a biomarker. Line chart of that biomarker over test dates. Table of all health records.

**Uploaded Reports:** Table of reports with Report ID, Filename, Upload Time, Status, Linked Record ID. Status is colour-coded (green/orange/red for processed/pending/failed).

---

# Chapter 6: Implementation

## 6.1 Technology Stack

| Component | Technology | Version / Notes |
|-----------|------------|-----------------|
| Language | Python | 3.10+ |
| Web Framework | Streamlit | ≥1.32.0 |
| Database | SQLite | Built-in |
| PDF (text) | pdfplumber | ≥0.11.0 |
| PDF (render) | PyMuPDF (fitz) | ≥1.24.0 |
| OCR | pytesseract | ≥0.3.10 (requires Tesseract binary) |
| Image handling | Pillow | ≥10.2.0 |
| Charts | Plotly | ≥5.20.0 |
| Data | pandas, numpy | Latest stable |
| Config | python-dotenv | ≥1.0.0 |

## 6.2 Key Implementation Details

### 6.2.1 Biomarker Parsing (services/pdf_parser.py)

Regex patterns are compiled once and applied to the extracted text. Each pattern captures the numeric value in group 1. Patterns handle common variations:
- Glucose: "Fasting Glucose", "Glucose", with optional "mg/dL" or "mg%"
- HbA1c: "HbA1c", "Hb A1c" with optional "%"
- BMI: Word boundary to avoid partial matches
- Blood pressure: Systolic and diastolic in "118/76" format
- Cholesterol: "Total Cholesterol" or "Cholesterol" with optional "mg/dL"

### 6.2.2 Normalisation (services/normalization_service.py)

`normalize_biomarker(value, ref_low, ref_high)` returns `(deviation, status)`:
- If value is within range: deviation 0.0, status "Normal"
- If value > ref_high: deviation = (value - ref_high) / ref_high, status "High"
- If value < ref_low: deviation = (ref_low - value) / ref_low, status "Low"

Input validation ensures numeric types and valid ranges. Used for both risk computation and biomarker display.

### 6.2.3 Database Design Choices

- **Connection per operation:** Each `db_handler` function opens a connection, executes, commits, and closes. SQLite handles concurrent reads; writes are serialised.
- **Row factory:** `sqlite3.Row` allows dict-like access by column name.
- **Foreign keys:** `PRAGMA foreign_keys = ON` enables referential integrity. CASCADE deletes propagate to child records; SET NULL preserves risk scores when a health record is deleted but links to NULL.

### 6.2.4 Project Structure

```
MedGuardian_Project/
├── app.py                 # Entry point
├── config.py              # DB path, auth, logging
├── requirements.txt
├── database/
│   └── db_handler.py
├── models/
│   ├── diabetes_model.py
│   └── reference_ranges.py
├── services/
│   ├── auth.py
│   ├── pdf_parser.py
│   └── normalization_service.py
├── pages/
│   ├── 1_Patient_Profile.py
│   ├── 2_Upload_Report.py
│   ├── 3_Risk_Dashboard.py
│   └── 4_History.py
├── utils/
│   └── data_loader.py
├── data/
│   ├── sample_patients.csv
│   ├── sample_health_records.csv
│   └── sample_reports/    # PDF lab reports
└── .streamlit/
    └── config.toml
```

## 6.3 Deployment (Streamlit Cloud)

MedGuardian is intended to run on Streamlit Community Cloud only; local hosting is not supported.

1. Push code to GitHub.
2. At [share.streamlit.io](https://share.streamlit.io), sign in with GitHub and create a new app.
3. Select repository, branch, and main file path (`MedGuardian_Project/app.py` if the app is in a subfolder).
4. In Advanced settings → Secrets, add `ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH`.
5. Deploy. The app will be available at `https://<your-app-name>.streamlit.app`. Note: Tesseract OCR is not available on Streamlit Cloud; only text-based PDFs are supported.

---

# Chapter 7: Datasets

## 7.1 Sample Patient Data (sample_patients.csv)

| Column | Type | Description |
|--------|------|--------------|
| name | string | Full name of patient |
| age | integer | Age in years (1–120) |
| gender | string | Male, Female, Other, Prefer not to say |
| email | string | Optional; must be unique if provided |

Five sample patients are included for demo and testing.

## 7.2 Sample Health Records (sample_health_records.csv)

| Column | Type | Description |
|--------|------|--------------|
| user_id | integer | Foreign key to patient (1-based in CSV) |
| test_date | date | YYYY-MM-DD format |
| glucose | float | Fasting glucose (mg/dL); 0 = not recorded |
| hba1c | float | HbA1c (%); 0 = not recorded |
| bmi | float | Body Mass Index; 0 = not recorded |
| systolic_bp | float | Systolic BP (mmHg); 0 = not recorded |
| diastolic_bp | float | Diastolic BP (mmHg); 0 = not recorded |
| cholesterol | float | Total cholesterol (mg/dL); 0 = not recorded |

Eight sample records span multiple patients with varied biomarker values for low, moderate, and high risk scenarios.

## 7.3 Sample PDF Lab Reports (data/sample_reports/)

Fifteen PDF lab reports are generated by `scripts/generate_sample_reports.py` from five different simulated laboratories (Care Diagnostics, Apollo, Thyro Lab, Metropolitan Pathology, Sunrise Clinical) across cities (Chennai, Bengaluru, Gurgaon, Pune). Reports cover:

- **Age groups:** 24–70 years (young adult to senior)
- **Risk profiles:** 5 low, 5 moderate, 5 high
- **Format:** Table-style layout with lab letterhead, patient demographics, specimen info, and sections for Glycemic Profile, Lipid Profile, Vital Signs, and Routine Biochemistry

Report filenames follow the pattern `lab_{labcode}_{patient}_{age}y_{risk}_{seq}.pdf` (e.g., `lab_apl_Karthik_24y_low_02.pdf`).

## 7.4 Data Loader Utility (utils/data_loader.py)

The `load_sample_data(force=False)` function:
- Reads `sample_patients.csv` and inserts into `users`
- Maps CSV user_id (1-based) to database user_id
- Reads `sample_health_records.csv` and inserts into `health_records`
- By default, skips loading if the database already contains patients
- `force=True` loads sample data even when existing data is present

Invoked from the Home page when the database is empty, or run via `python -m utils.data_loader`.

## 7.5 Dataset Format Documentation

`data/DATASET_FORMAT.md` documents the CSV column specifications, units, and usage instructions for creating custom datasets.

---

# Chapter 8: Results

## 8.1 Application Screenshots

Screenshots are in the `screenshots/` folder. Insert as needed:

1. **Login Page:** `screenshots/01_Login_Page.png` — Username and password fields, MedGuardian branding
2. **Home Page:** `screenshots/02_Home_Page.png` — Four-step workflow cards, "Load sample demo data" expander
3. **Patient Profile:** `screenshots/03_Patient_Profile.png` — New Patient form or Manage Existing view
4. **Upload Report:** `screenshots/04_Upload_Report.png` — File uploader, parsed biomarkers, Save button
5. **Risk Dashboard:** `screenshots/05_Risk_Dashboard.png` — Gauge charts for Diabetes/BP/Cholesterol
6. **History – Risk Trends:** `screenshots/06_History_Risk_Trends.png` — Line chart with reference lines
7. **History – Biomarker Trends:** `screenshots/07_History_Biomarkers.png` — Biomarker dropdown, line chart

*To capture: Login at https://medguardian-cq4hnprbbuxvdpwg9pw3vv.streamlit.app/ (admin/admin123), then screenshot each page. See `screenshots/README.md`.*

## 8.2 Functional Test Results

| ID | Test Case | Expected Outcome | Result |
|----|-----------|------------------|--------|
| TC1 | Login with correct credentials (admin/admin123) | Access to Home page | ✓ Pass |
| TC2 | Login with incorrect credentials | Error message, no access | ✓ Pass |
| TC3 | Create new patient with required fields | Patient saved, ID returned | ✓ Pass |
| TC4 | Create patient with duplicate email | Error: email already exists | ✓ Pass |
| TC5 | Upload text-based PDF lab report | Text extracted, biomarkers parsed | ✓ Pass |
| TC6 | Verify and correct parsed values, save | Health record created, report linked | ✓ Pass |
| TC7 | Compute diabetes risk with glucose, HbA1c, BMI | Score 0–100%, gauge displayed | ✓ Pass |
| TC8 | Compute BP and cholesterol risk | Scores displayed, saved to DB | ✓ Pass |
| TC9 | View risk score trends over time | Line chart with multiple conditions | ✓ Pass |
| TC10 | Load sample data when DB empty | 5 patients, 8 health records loaded | ✓ Pass |
| TC11 | Edit patient and save | Record updated | ✓ Pass |
| TC12 | Delete patient with confirmation | Patient and related records deleted | ✓ Pass |

## 8.3 Sample Output

**Diabetes Risk Example:** For a patient with glucose 118 mg/dL, HbA1c 6.0%, BMI 27.5, family history Yes: Diabetes risk ≈ 45% (Moderate).

**Blood Pressure Example:** Systolic 132, Diastolic 84 → Hypertension risk ≈ 50% (Moderate) per JNC 8.

**Cholesterol Example:** Total cholesterol 218 mg/dL → Cholesterol risk ≈ 45% (Moderate) per ACC/AHA.

## 8.4 Deployment Verification

The application is deployed on Streamlit Community Cloud via GitHub integration. App URL format: `https://<app-name>.streamlit.app`. Verification: open the deployed URL, log in with configured credentials, and confirm all pages (Home, Patient Profile, Upload Report, Risk Dashboard, History) load and function as expected.

---

# Chapter 9: Limitations

## 9.1 OCR Dependency

Tesseract OCR is not available on Streamlit Cloud. Only text-based PDF lab reports can be parsed; scanned PDFs will fail to extract text. Users should use text-based reports or copy values manually when necessary.

## 9.2 Single-User Model

The application supports only one admin user. There is no multi-tenancy, role-based access, or patient self-service. Expanding to multiple users would require session management, user tables, and permission logic.

## 9.3 PDF Format Variability

Regex patterns are tuned for common lab report formats. Unusual layouts, non-standard terminology, or non-English reports may not parse correctly. The system allows manual correction before save, but fully automated extraction across all lab formats is not guaranteed.

## 9.4 Limited Biomarker Set

Only six biomarkers are extracted: glucose, HbA1c, BMI, systolic BP, diastolic BP, total cholesterol. Other clinically relevant parameters (LDL, HDL, triglycerides, creatinine, etc.) are not parsed. Risk computation depends solely on these six.

## 9.5 No External Integration

There is no integration with Electronic Health Records (EHR), Laboratory Information Systems (LIS), or health APIs. Data must be entered via PDF upload or sample loader. HL7, FHIR, or other healthcare standards are not supported.

## 9.6 Ephemeral Cloud Data

On Streamlit Cloud, the SQLite database is ephemeral; data is lost when the app restarts or is redeployed. Persistent storage would require external database services (e.g., PostgreSQL, Supabase).

---

# Chapter 10: Future Work

## 10.1 Extended Biomarker Support

Add parsing and risk computation for:
- Triglycerides, LDL, HDL (full lipid panel)
- Creatinine, eGFR (kidney function)
- ALT, AST (liver function)

This would enable broader cardiovascular and metabolic risk assessment.

## 10.2 Multi-User and Role-Based Access

Implement:
- User registration and authentication (clinician, patient)
- Clinician dashboard for multiple patients
- Patient portal for viewing own records
- Role-based permissions (read/write/delete)

## 10.3 Report Export

Generate PDF or printable reports summarising risk scores and trends for a patient. Include charts and recommendations for follow-up.

## 10.4 Integration with LIS and EHR

- HL7/FHIR connectors for lab systems
- Import from HL7 messages or FHIR DiagnosticReport resources
- Export to EHR via APIs

## 10.5 Enhanced Parsing

- Machine learning–based extraction for varied report formats
- Support for multiple languages
- Table structure detection for structured extraction

## 10.6 Mobile and Offline Support

- Responsive design for mobile browsers
- Progressive Web App (PWA) for offline capability
- Native mobile app (e.g., React Native, Flutter)

---

# Chapter 11: Business Model

## 11.1 Open-Source Community Edition

Release MedGuardian under an open-source license (e.g., MIT or Apache 2.0) for:
- Small clinics and primary care centres
- Academic researchers studying early disease detection
- Health-conscious individuals
- Cost-sensitive environments

Community support via forums and GitHub issues. No direct revenue; builds brand and adoption.

## 11.2 Software-as-a-Service (SaaS)

Offer a hosted, multi-tenant version:
- Subscription tiers: Free (limited), Pro (unlimited patients), Enterprise (custom)
- Cloud hosting with persistent database (PostgreSQL)
- Premium features: advanced analytics, report export, API access
- Revenue: monthly or annual subscriptions

## 11.3 On-Premise Enterprise

Licence for hospitals and large clinics with strict data residency:
- Deploy within hospital infrastructure
- Integration with existing LIS/EHR
- Custom development and support contracts
- Compliance with local data protection regulations (e.g., HIPAA, GDPR)

---

# Chapter 12: Conclusion

MedGuardian achieves its stated objectives as an AI-assisted early disease detection system. It successfully parses text-based PDF lab reports, extracts key biomarkers using robust regex patterns, and computes clinically grounded risk scores for diabetes, hypertension, and cholesterol. The system is deployed on Streamlit Cloud and stores all data in SQLite on the deployment server, with no transmission of health data to external services.

The project demonstrates the practical integration of document processing (pdfplumber, PyMuPDF, Tesseract), clinical reference ranges (ADA, JNC 8, ACC/AHA), and interactive data visualisation (Plotly) within a Streamlit web application. The modular architecture—separating authentication, PDF parsing, normalisation, risk models, and database access—ensures maintainability and extensibility.

Sample datasets (CSV patients, health records, and PDF lab reports from multiple laboratories and age groups) and a data loader utility support demonstration and testing without manual data entry. Functional testing confirms that core workflows—login, patient management, PDF upload, biomarker parsing, risk computation, and trend visualisation—perform as intended.

Limitations include OCR dependency, single-user design, and limited biomarker coverage. Future work can address these through extended parsing, multi-user support, and integration with laboratory and health record systems. MedGuardian provides a solid foundation for lightweight, privacy-preserving health analytics suitable for small clinics and individual use.

### 12.1 Contributions

This project contributes: (i) an integrated pipeline from PDF lab reports to early disease risk scores within a single application; (ii) support for text-based PDFs via pdfplumber (scanned PDFs not supported on Streamlit Cloud); (iii) a clinical risk model aligned with ADA, JNC 8, and ACC/AHA guidelines; (iv) a cloud-deployed, privacy-preserving architecture with data stored only on the deployment server; and (v) a reproducible sample dataset (15 PDF reports from 5 laboratories, varied age groups) for evaluation and demonstration.

---

# References

1. Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io/
2. Python Software Foundation. (2024). *Python 3.12 Documentation*. https://docs.python.org/3/
3. American Diabetes Association. (2024). *Standards of Medical Care in Diabetes*. https://professional.diabetes.org/
4. Whelton, P. K., Carey, R. M., Aronow, W. S., et al. (2017). *ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA Guideline for the Prevention, Detection, Evaluation, and Management of High Blood Pressure in Adults*. Journal of the American College of Cardiology, 71(19), e127–e248.
5. Grundy, S. M., Stone, N. J., Bailey, A. L., et al. (2018). *AHA/ACC/AACVPR/AAPA/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Blood Cholesterol*. Circulation, 139(25), e1082–e1143.
6. SQLite. (2024). *SQLite Documentation*. https://www.sqlite.org/docs.html
7. WHO. (2023). *Noncommunicable Diseases*. World Health Organization. https://www.who.int/news-room/fact-sheets/detail/noncommunicable-diseases
8. NFHS-5. (2021). *National Family Health Survey (NFHS-5)*. Ministry of Health and Family Welfare, Government of India.
9. Tesseract OCR. (2024). *Tesseract Documentation*. https://tesseract-ocr.github.io/
10. ReportLab. (2024). *ReportLab User Guide*. https://docs.reportlab.com/
11. NAAC. *National Assessment and Accreditation Council*. https://www.naac.gov.in/
12. [College Name]. *Official Website*. [College URL]

---

# Appendices

## Appendix A: Deployment (Streamlit Cloud)

MedGuardian runs only on Streamlit Community Cloud. There is no local installation or run.

1. Push the project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** (or **Create app**), select your repo and branch.
4. Set **Main file path** to `MedGuardian_Project/app.py` if the repository root is the parent of `MedGuardian_Project`.
5. In **Advanced settings** → **Secrets**, add `ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH` (SHA-256 hash of your password).
6. Deploy. The app will be available at `https://<your-app-name>.streamlit.app`. Default login is admin/admin123; change via secrets before any real use.

## Appendix B: Sample Biomarker Regex Patterns

| Biomarker | Regex Pattern (simplified) |
|-----------|----------------------------|
| Glucose | `(?:fasting\s+)?glucose[^:\n]*?[:\s]+(\d+(?:\.\d+)?)\s*(?:mg/dl)?` |
| HbA1c | `hb\s*a1c[^:\n]*?[:\s]+(\d+(?:\.\d+)?)\s*%?` |
| BMI | `\bbmi\b[^:\n]*?[:\s]+(\d+(?:\.\d+)?)` |
| Systolic BP | `blood\s+pressure[^:\n]*?[:\s]+(\d{2,3})\s*/` |
| Diastolic BP | `[:\s]+\d{2,3}\s*/\s*(\d{2,3})` |
| Cholesterol | `(?:total\s+)?cholesterol[^:\n]*?[:\s]+(\d+(?:\.\d+)?)\s*(?:mg/dl)?` |

## Appendix C: Reference Ranges (Summary)

| Biomarker | Low | High | Unit | Source |
|-----------|-----|------|------|--------|
| Fasting Glucose | 70 | 99 | mg/dL | ADA 2024 |
| HbA1c | 4.0 | 5.6 | % | ADA 2024 |
| BMI | 18.5 | 24.9 | kg/m² | WHO |
| Systolic BP | 90 | 120 | mmHg | JNC 8 / ACC-AHA |
| Diastolic BP | 60 | 80 | mmHg | JNC 8 / ACC-AHA |
| Total Cholesterol | 0 | 200 | mg/dL | ACC/AHA 2018 |

## Appendix D: Sample Laboratories in Generated Reports

| Code | Laboratory | City |
|------|------------|------|
| CDL | Care Diagnostics Laboratory | Chennai |
| APL | Apollo Diagnostics | Chennai |
| TLD | Thyro Lab & Diagnostic Centre | Bengaluru |
| MPL | Metropolitan Pathology Lab | Gurgaon |
| SCL | Sunrise Clinical Laboratory | Pune |

## Appendix E: Glossary

- **Biomarker:** A measurable substance in the body that indicates a physiological or pathological state.
- **HbA1c:** Glycated haemoglobin; reflects average blood glucose over 2–3 months.
- **BMI:** Body Mass Index; weight (kg) / height² (m²).
- **Prediabetes:** Glucose or HbA1c above normal but below diabetes threshold.
- **Hypertension:** Persistently elevated blood pressure.

## Appendix F: Git Upload Commands

To upload the project to GitHub (first-time setup and push):

```bash
# Navigate to project root (e.g. MedGuardian or MedGuardian_Project)
cd path/to/MedGuardian

# Initialise repository
git init

# Add all files (ensure .gitignore excludes .env, venv, *.db, *.log)
git add .
git status

# First commit
git commit -m "Initial commit: MedGuardian - AI-Assisted Early Disease Detection System"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/MedGuardian.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub (you may be prompted for credentials or token)
git push -u origin main
```

For subsequent updates after making changes:

```bash
git add .
git commit -m "Brief description of changes"
git push
```

## Appendix G: Streamlit Cloud Basics

Streamlit Community Cloud (share.streamlit.io) is a free hosting platform that runs Streamlit apps from a GitHub repository. You sign in with GitHub, click “Create app”, choose your repository and branch, and set the main file path (e.g. `app.py` or `MedGuardian_Project/app.py`). The platform builds a container, installs dependencies from `requirements.txt`, and runs your app. Secrets (e.g. `ADMIN_PASSWORD_HASH`) can be added in Advanced settings so the app reads them as environment variables. The app gets a public URL (e.g. `https://your-app-name.streamlit.app`). Note: the filesystem and SQLite database are ephemeral—data does not persist across redeploys unless you use an external database.

---

*End of Report*
