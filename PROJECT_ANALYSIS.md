# MedGuardian — Project Analysis (Step A)

**Date:** 2025-03-09  
**Purpose:** B.Sc. Computer Science Final Year Project submission readiness

---

## 1. FOLDER STRUCTURE & MAIN FILES

```
MedGuardian/
├── MedGuardian_Project/
│   ├── app.py                    # Streamlit entry point
│   ├── config.py                 # Configuration (env, DB path, auth)
│   ├── requirements.txt
│   ├── README.md
│   ├── .env.example
│   ├── database/
│   │   └── db_handler.py         # SQLite CRUD
│   ├── models/
│   │   ├── diabetes_model.py     # Risk scoring
│   │   └── reference_ranges.py   # Clinical reference ranges
│   ├── services/
│   │   ├── auth.py               # Session-based login
│   │   ├── normalization_service.py
│   │   └── pdf_parser.py         # PDF extraction + OCR
│   └── pages/
│       ├── 1_Patient_Profile.py
│       ├── 2_Upload_Report.py
│       ├── 3_Risk_Dashboard.py
│       └── 4_History.py
```

**Missing:** `__init__.py` in `database/`, `models/`, `services/` (may cause import issues in some setups).

---

## 2. TECH STACK

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Framework | Streamlit |
| Database | SQLite (via `sqlite3`) |
| PDF | pdfplumber, PyMuPDF (fitz) |
| OCR | pytesseract, Pillow |
| Charts | Plotly |
| Other | pandas, numpy, scikit-learn, python-dotenv |

**Note:** `scikit-learn` is in requirements but not used in the codebase — safe to remove for leaner deployment.

---

## 3. IDENTIFIED GAPS

| Gap | Severity | Location |
|-----|----------|----------|
| No `__init__.py` in packages | Low | database/, models/, services/ |
| `update_report_status` overwrites `extracted_text` with NULL when updating status | Medium | db_handler.py, 2_Upload_Report.py |
| No sample datasets or demo data | Medium | New — needed for demo/empty DB |
| No project report or presentation | High | New files required |
| No `.streamlit/config.toml` or `.gitignore` | Medium | Streamlit Cloud prep |
| App stops when DB is empty (no patients) | Medium | Pages use `st.stop()` — need fallback/seed |

---

## 4. CODE REVIEW

### Bugs
- **db_handler.update_report_status:** Always sets `extracted_text=?` in UPDATE. When called with only `status` and `record_id`, `extracted_text` defaults to `None`, overwriting the stored text. Fix: update only `status` and `record_id` when `extracted_text` is not provided, or pass it through.

### Error Handling
- Good: try/except in app.py for `create_tables()`, form validation in Patient Profile.
- Missing: graceful handling when Tesseract OCR is not installed (user sees generic error).
- `update_report_status` on exception path: overwrites extracted_text.

### Security
- Passwords hashed with SHA-256 (acceptable for demo; recommend bcrypt for production).
- SQL uses parameterised queries — good.
- No obvious SQL injection or XSS issues.

### Consistency
- `st.rerun()` used (correct for Streamlit 1.32+).
- Naming and structure are consistent.

---

## 5. FIX & IMPLEMENTATION CHECKLIST

- [ ] Add `__init__.py` to database/, models/, services/
- [ ] Fix `update_report_status` to avoid overwriting `extracted_text`
- [ ] Create sample CSV dataset (patients + health records) for demo
- [ ] Add data loader / seed utility for empty DB
- [ ] Document dataset format
- [ ] Create consolidated project report (Markdown)
- [ ] Add college front matter (title, certificate, declaration, acknowledgement)
- [ ] Add References and List of Abbreviations
- [ ] Create Marp presentation
- [ ] Trim requirements (remove unused scikit-learn if confirmed)
- [ ] Add `.streamlit/config.toml`, `.gitignore`
- [ ] Update README with Streamlit Cloud deploy instructions
- [ ] Ensure app handles empty DB (seed or clear messaging)
- [ ] Add Pandoc command for DOCX export

---

## 6. PROJECT METADATA (Placeholders)

- **Project name:** MedGuardian
- **One-line description:** AI Assisted Health Risk Insights — parses PDF lab reports and computes diabetes, hypertension, and cholesterol risk scores
- **College name:** [Your College Full Name]
- **College location:** [City, PIN]
- **Degree:** B.Sc. Computer Science
- **Your name:** [Your Full Name]
- **Roll/Register no.:** [Your Roll No]
- **Guide name:** [Guide Name]
- **Guide designation:** [e.g. Assistant Professor, Department of Computer Science]
- **Academic year:** [e.g. 2024 – 2025]
- **Deployment target:** Streamlit Cloud
