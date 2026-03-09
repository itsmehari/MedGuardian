"""
Page 2 — Upload Lab Report

Accepts a PDF lab report, extracts text (with OCR fallback for scanned
documents), parses known biomarkers using regex, lets the user confirm
or correct the values, then saves a health record to the database.
"""

from datetime import date

import streamlit as st

from services.auth import require_auth, sidebar_user_info
from services.pdf_parser import extract_text_from_pdf, parse_biomarkers
from database.db_handler import (
    insert_health_record,
    insert_uploaded_report,
    update_report_status,
    get_all_users,
    get_user_by_id,
)

st.set_page_config(page_title="Upload Report – MedGuardian", layout="wide")
require_auth()
sidebar_user_info()

st.title("📄 Upload Lab Report")
st.markdown(
    "Upload a PDF lab report. MedGuardian will extract biomarker values "
    "automatically. You can review and correct them before saving."
)
st.divider()

# ---------------------------------------------------------------------------
# Patient selector (pre-fill from session if available)
# ---------------------------------------------------------------------------
users = get_all_users()
if not users:
    st.warning("No patients found. Please create a patient on the **Patient Profile** page first.")
    st.stop()

options = {
    f"{u['name']}  (ID {u['user_id']})": u["user_id"] for u in users
}
current_uid = st.session_state.get("current_user_id")
default_idx = 0
if current_uid:
    labels = list(options.keys())
    ids = list(options.values())
    if current_uid in ids:
        default_idx = ids.index(current_uid)

selected_label = st.selectbox("Select Patient *", list(options.keys()), index=default_idx)
selected_uid = options[selected_label]
st.session_state["current_user_id"] = selected_uid

st.divider()

# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Choose a PDF lab report",
    type=["pdf"],
    help="Text-based and scanned PDFs are both supported.",
)

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    st.info(f"File received: **{uploaded_file.name}** ({len(pdf_bytes) / 1024:.1f} KB)")

    with st.spinner("Extracting text from PDF…"):
        raw_text = extract_text_from_pdf(pdf_bytes)

    if not raw_text.strip():
        st.error(
            "Could not extract any text from this PDF. "
            "If it is a scanned document, ensure Tesseract OCR is installed on your system."
        )
        st.stop()

    with st.expander("📝 Raw extracted text (for debugging)"):
        st.text(raw_text[:3000] + ("…" if len(raw_text) > 3000 else ""))

    # Store the report record (status = pending until we save the health record)
    report_id = insert_uploaded_report(
        user_id=selected_uid,
        filename=uploaded_file.name,
        extracted_text=raw_text,
        status="pending",
    )

    # ---------------------------------------------------------------------------
    # Parse biomarkers and let the user verify / correct
    # ---------------------------------------------------------------------------
    parsed = parse_biomarkers(raw_text)

    st.subheader("📊 Parsed Biomarker Values")
    st.markdown(
        "Values were extracted automatically. Correct any that look wrong "
        "before saving, and fill in any that are blank."
    )

    biomarker_meta = {
        "glucose":      ("Fasting Glucose (mg/dL)",     0.0, 600.0),
        "hba1c":        ("HbA1c (%)",                   0.0,  20.0),
        "bmi":          ("BMI (kg/m²)",                 0.0,  80.0),
        "systolic_bp":  ("Systolic BP (mmHg)",          0.0, 300.0),
        "diastolic_bp": ("Diastolic BP (mmHg)",         0.0, 200.0),
        "cholesterol":  ("Total Cholesterol (mg/dL)",   0.0, 600.0),
    }

    col_left, col_right = st.columns(2)
    inputs: dict = {}
    keys = list(biomarker_meta.keys())

    for i, key in enumerate(keys):
        label, min_v, max_v = biomarker_meta[key]
        default = parsed.get(key)
        col = col_left if i % 2 == 0 else col_right
        with col:
            if default is not None:
                inputs[key] = st.number_input(
                    f"✅ {label}",
                    min_value=0.0,
                    max_value=max_v,
                    value=float(default),
                    step=0.1,
                    help="Auto-detected value — verify before saving.",
                )
            else:
                inputs[key] = st.number_input(
                    f"⬜ {label}",
                    min_value=0.0,
                    max_value=max_v,
                    value=0.0,
                    step=0.1,
                    help="Not detected in the PDF — enter manually or leave as 0.",
                )

    test_date = st.date_input("Test Date *", value=date.today())

    st.divider()

    if st.button("💾 Save Health Record", use_container_width=True, type="primary"):
        def none_if_zero(v: float):
            return None if v == 0.0 else v

        try:
            record_id = insert_health_record(
                user_id=selected_uid,
                test_date=str(test_date),
                glucose=none_if_zero(inputs["glucose"]),
                hba1c=none_if_zero(inputs["hba1c"]),
                bmi=none_if_zero(inputs["bmi"]),
                systolic_bp=none_if_zero(inputs["systolic_bp"]),
                diastolic_bp=none_if_zero(inputs["diastolic_bp"]),
                cholesterol=none_if_zero(inputs["cholesterol"]),
            )
            update_report_status(
                report_id=report_id,
                status="processed",
                record_id=record_id,
            )
            st.session_state["current_record_id"] = record_id
            st.success(
                f"Health record saved (Record ID: {record_id}). "
                "Head to the **Risk Dashboard** page to compute risk scores."
            )
        except Exception as exc:
            update_report_status(report_id=report_id, status="failed")
            st.error(f"Failed to save health record: {exc}")
