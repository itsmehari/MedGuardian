"""
Page 3 — Risk Dashboard

Displays early disease risk (from biomarkers) for a selected patient and health
record. Covers diabetes risk, blood pressure classification, and
cholesterol assessment. Scores are saved to the database.
"""

from typing import Optional

import plotly.graph_objects as go
import streamlit as st

from database.db_handler import (
    get_all_users,
    get_health_records_by_user,
    get_health_record_by_id,
    insert_risk_score,
)
from models.diabetes_model import calculate_diabetes_risk
from models.reference_ranges import REFERENCE_RANGES
from services.auth import require_auth, sidebar_user_info
from services.normalization_service import normalize_biomarker

st.set_page_config(page_title="Risk Dashboard – MedGuardian", layout="wide")
require_auth()
sidebar_user_info()

st.title("📊 Risk Dashboard")
st.markdown("Select a patient and a health record to compute and view risk scores.")
st.divider()

# ---------------------------------------------------------------------------
# Patient + record selectors
# ---------------------------------------------------------------------------
users = get_all_users()
if not users:
    st.warning("No patients found. Please create a patient on the **Patient Profile** page first.")
    st.stop()

patient_options = {
    f"{u['name']}  (ID {u['user_id']})": u["user_id"] for u in users
}
current_uid = st.session_state.get("current_user_id")
default_pidx = 0
if current_uid and current_uid in list(patient_options.values()):
    default_pidx = list(patient_options.values()).index(current_uid)

selected_patient_label = st.selectbox(
    "Select Patient", list(patient_options.keys()), index=default_pidx
)
selected_uid = patient_options[selected_patient_label]
st.session_state["current_user_id"] = selected_uid

records = get_health_records_by_user(selected_uid)
if not records:
    st.info(
        "No health records found for this patient. "
        "Upload a lab report on the **Upload Report** page first."
    )
    st.stop()

record_options = {
    f"Record {r['record_id']}  –  {r.get('test_date', 'No date')}": r["record_id"]
    for r in records
}
current_rid = st.session_state.get("current_record_id")
default_ridx = 0
if current_rid and current_rid in list(record_options.values()):
    default_ridx = list(record_options.values()).index(current_rid)

selected_record_label = st.selectbox(
    "Select Health Record", list(record_options.keys()), index=default_ridx
)
selected_rid = record_options[selected_record_label]
record = get_health_record_by_id(selected_rid)

if not record:
    st.error("Could not load the selected record.")
    st.stop()

st.divider()

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def risk_color(level: str) -> str:
    return {"Low": "green", "Moderate": "orange", "High": "red"}.get(level, "grey")


def classify_level(score: float) -> str:
    if score <= 0.20:
        return "Low"
    if score <= 0.50:
        return "Moderate"
    return "High"


def gauge_chart(title: str, score: float, level: str) -> go.Figure:
    color = {"Low": "#2ecc71", "Moderate": "#f39c12", "High": "#e74c3c"}.get(level, "#95a5a6")
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(score * 100, 1),
            number={"suffix": "%"},
            title={"text": title, "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 20], "color": "#d5f5e3"},
                    {"range": [20, 50], "color": "#fef9e7"},
                    {"range": [50, 100], "color": "#fadbd8"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 4},
                    "thickness": 0.8,
                    "value": round(score * 100, 1),
                },
            },
        )
    )
    fig.update_layout(height=250, margin=dict(t=40, b=20, l=20, r=20))
    return fig


# ---------------------------------------------------------------------------
# Biomarker summary table
# ---------------------------------------------------------------------------
st.subheader("🔬 Biomarker Summary")

biomarker_display = [
    ("Fasting Glucose", record.get("glucose"), "glucose", "mg/dL"),
    ("HbA1c", record.get("hba1c"), "hba1c", "%"),
    ("BMI", record.get("bmi"), "bmi", "kg/m²"),
    ("Systolic BP", record.get("systolic_bp"), "systolic_bp", "mmHg"),
    ("Diastolic BP", record.get("diastolic_bp"), "diastolic_bp", "mmHg"),
    ("Total Cholesterol", record.get("cholesterol"), "cholesterol", "mg/dL"),
]

bm_cols = st.columns(len(biomarker_display))
for col, (label, value, key, unit) in zip(bm_cols, biomarker_display):
    if value is None:
        col.metric(label, "N/A")
    else:
        rng = REFERENCE_RANGES[key]
        _, status = normalize_biomarker(
            value,
            rng["low"] if rng["low"] > 0 else 0.01,
            rng["high"],
        )
        delta_str = f"↑ High" if status == "High" else ("↓ Low" if status == "Low" else "Normal")
        col.metric(label, f"{value} {unit}", delta=delta_str)

st.divider()

# ---------------------------------------------------------------------------
# Risk Score Computation
# ---------------------------------------------------------------------------
st.subheader("⚠️ Risk Assessment")

family_history = st.radio(
    "Family history of diabetes (first-degree relative)?",
    options=[0, 1],
    format_func=lambda x: "Yes" if x else "No",
    horizontal=True,
)

compute_btn = st.button("🧮 Compute Risk Scores", type="primary", use_container_width=True)

if compute_btn:
    results = {}

    # --- Diabetes Risk ---
    glucose = record.get("glucose")
    hba1c = record.get("hba1c")
    bmi = record.get("bmi")

    if glucose and hba1c and bmi:
        g_rng = REFERENCE_RANGES["glucose"]
        h_rng = REFERENCE_RANGES["hba1c"]
        g_dev, _ = normalize_biomarker(glucose, g_rng["low"], g_rng["high"])
        h_dev, _ = normalize_biomarker(hba1c, h_rng["low"], h_rng["high"])
        try:
            d_score = calculate_diabetes_risk(g_dev, h_dev, bmi, family_history)
            d_level = classify_level(d_score)
            results["Diabetes"] = (d_score, d_level)
            insert_risk_score(selected_uid, "diabetes", d_score, d_level, selected_rid)
        except (TypeError, ValueError) as exc:
            st.warning(f"Diabetes risk calculation skipped: {exc}")
    else:
        st.info("Diabetes risk requires Glucose, HbA1c, and BMI values.")

    # --- Blood Pressure Risk ---
    sbp = record.get("systolic_bp")
    dbp = record.get("diastolic_bp")
    if sbp and dbp:
        # JNC 8 / ACC-AHA simplified classification
        if sbp < 120 and dbp < 80:
            bp_level, bp_score = "Low", 0.05
        elif sbp < 130 and dbp < 80:
            bp_level, bp_score = "Low", 0.20
        elif sbp < 140 or dbp < 90:
            bp_level, bp_score = "Moderate", 0.50
        else:
            bp_level, bp_score = "High", 0.85
        results["Hypertension"] = (bp_score, bp_level)
        insert_risk_score(selected_uid, "hypertension", bp_score, bp_level, selected_rid)
    else:
        st.info("Blood pressure risk requires both Systolic and Diastolic BP values.")

    # --- Cholesterol Risk ---
    chol = record.get("cholesterol")
    if chol:
        # ACC/AHA thresholds (total cholesterol)
        if chol < 200:
            c_level, c_score = "Low", 0.05
        elif chol < 240:
            c_level, c_score = "Moderate", 0.45
        else:
            c_level, c_score = "High", 0.80
        results["High Cholesterol"] = (c_score, c_level)
        insert_risk_score(selected_uid, "cholesterol", c_score, c_level, selected_rid)
    else:
        st.info("Cholesterol risk requires a Total Cholesterol value.")

    st.session_state["last_risk_results"] = results

# Show gauges if results exist
if "last_risk_results" in st.session_state and st.session_state["last_risk_results"]:
    results = st.session_state["last_risk_results"]
    st.divider()

    gauge_cols = st.columns(len(results))
    for col, (condition, (score, level)) in zip(gauge_cols, results.items()):
        with col:
            st.plotly_chart(
                gauge_chart(condition, score, level),
                use_container_width=True,
            )
            color = risk_color(level)
            st.markdown(
                f"<div style='text-align:center; color:{color}; font-weight:bold; "
                f"font-size:1.2em;'>{level} Risk</div>",
                unsafe_allow_html=True,
            )

    st.divider()
    st.success("Risk scores have been saved to the database. View trends on the **History** page.")
