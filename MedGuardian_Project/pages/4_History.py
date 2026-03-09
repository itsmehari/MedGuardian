"""
Page 4 — History & Trends

Shows a timeline of risk scores and biomarker values for a selected
patient using interactive Plotly charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from database.db_handler import (
    get_all_users,
    get_health_records_by_user,
    get_risk_scores_by_user,
    get_reports_by_user,
)
from services.auth import require_auth, sidebar_user_info

st.set_page_config(page_title="History – MedGuardian", layout="wide")
require_auth()
sidebar_user_info()

st.title("📈 History & Trends")
st.markdown("Track how a patient's biomarkers and risk scores change over time.")
st.divider()

# ---------------------------------------------------------------------------
# Patient selector
# ---------------------------------------------------------------------------
users = get_all_users()
if not users:
    st.warning("No patients found. Create one on the **Patient Profile** page first.")
    st.stop()

patient_options = {
    f"{u['name']}  (ID {u['user_id']})": u["user_id"] for u in users
}
current_uid = st.session_state.get("current_user_id")
default_idx = 0
if current_uid and current_uid in list(patient_options.values()):
    default_idx = list(patient_options.values()).index(current_uid)

selected_label = st.selectbox(
    "Select Patient", list(patient_options.keys()), index=default_idx
)
selected_uid = patient_options[selected_label]
st.session_state["current_user_id"] = selected_uid

st.divider()

# ---------------------------------------------------------------------------
# Fetch data
# ---------------------------------------------------------------------------
health_records = get_health_records_by_user(selected_uid)
risk_scores = get_risk_scores_by_user(selected_uid)
reports = get_reports_by_user(selected_uid)

if not health_records and not risk_scores:
    st.info(
        "No data found for this patient. Upload a lab report and compute "
        "risk scores first."
    )
    st.stop()

tab_risk, tab_biomarkers, tab_reports = st.tabs(
    ["⚠️ Risk Score Trends", "🔬 Biomarker Trends", "📁 Uploaded Reports"]
)

# ---------------------------------------------------------------------------
# Tab 1 — Risk Score Trends
# ---------------------------------------------------------------------------
with tab_risk:
    if not risk_scores:
        st.info("No risk scores computed yet. Use the **Risk Dashboard** page.")
    else:
        df_risk = pd.DataFrame(risk_scores)
        df_risk["computed_at"] = pd.to_datetime(df_risk["computed_at"])
        df_risk["risk_pct"] = (df_risk["risk_score"] * 100).round(1)

        conditions = df_risk["condition"].unique().tolist()
        selected_conditions = st.multiselect(
            "Filter by condition",
            conditions,
            default=conditions,
        )
        df_filtered = df_risk[df_risk["condition"].isin(selected_conditions)]

        if df_filtered.empty:
            st.info("No data for the selected conditions.")
        else:
            fig = px.line(
                df_filtered,
                x="computed_at",
                y="risk_pct",
                color="condition",
                markers=True,
                labels={
                    "computed_at": "Date",
                    "risk_pct": "Risk Score (%)",
                    "condition": "Condition",
                },
                title="Risk Score Over Time",
            )
            fig.add_hline(y=20, line_dash="dot", line_color="green",
                          annotation_text="Low threshold (20%)")
            fig.add_hline(y=50, line_dash="dot", line_color="orange",
                          annotation_text="High threshold (50%)")
            fig.update_layout(yaxis_range=[0, 105])
            st.plotly_chart(fig, use_container_width=True)

        # Summary table
        st.subheader("All Risk Score Records")
        display_cols = ["computed_at", "condition", "risk_pct", "risk_level", "record_id"]
        available = [c for c in display_cols if c in df_risk.columns]
        st.dataframe(
            df_risk[available].rename(columns={
                "computed_at": "Computed At",
                "condition": "Condition",
                "risk_pct": "Score (%)",
                "risk_level": "Level",
                "record_id": "Record ID",
            }),
            use_container_width=True,
            hide_index=True,
        )

# ---------------------------------------------------------------------------
# Tab 2 — Biomarker Trends
# ---------------------------------------------------------------------------
with tab_biomarkers:
    if not health_records:
        st.info("No health records found for this patient.")
    else:
        df_hr = pd.DataFrame(health_records)
        df_hr["test_date"] = pd.to_datetime(df_hr["test_date"], errors="coerce")
        df_hr = df_hr.sort_values("test_date")

        biomarker_cols = {
            "glucose": "Glucose (mg/dL)",
            "hba1c": "HbA1c (%)",
            "bmi": "BMI (kg/m²)",
            "systolic_bp": "Systolic BP (mmHg)",
            "diastolic_bp": "Diastolic BP (mmHg)",
            "cholesterol": "Cholesterol (mg/dL)",
        }

        available_bm = [
            col for col in biomarker_cols
            if col in df_hr.columns and df_hr[col].notna().any()
        ]

        if not available_bm:
            st.info("No biomarker values recorded yet.")
        else:
            selected_bm = st.selectbox(
                "Select biomarker to view",
                available_bm,
                format_func=lambda k: biomarker_cols[k],
            )

            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=df_hr["test_date"],
                    y=df_hr[selected_bm],
                    mode="lines+markers",
                    name=biomarker_cols[selected_bm],
                    line=dict(width=2),
                    marker=dict(size=8),
                )
            )
            fig2.update_layout(
                title=f"{biomarker_cols[selected_bm]} Over Time",
                xaxis_title="Test Date",
                yaxis_title=biomarker_cols[selected_bm],
                height=400,
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Full biomarker table
        st.subheader("All Health Records")
        rename_map = {"test_date": "Test Date", "record_id": "Record ID"}
        rename_map.update({k: v for k, v in biomarker_cols.items()})
        show_cols = ["record_id", "test_date"] + available_bm
        st.dataframe(
            df_hr[[c for c in show_cols if c in df_hr.columns]].rename(columns=rename_map),
            use_container_width=True,
            hide_index=True,
        )

# ---------------------------------------------------------------------------
# Tab 3 — Uploaded Reports
# ---------------------------------------------------------------------------
with tab_reports:
    if not reports:
        st.info("No reports uploaded yet.")
    else:
        df_rep = pd.DataFrame(reports)
        display = df_rep[
            [c for c in ["report_id", "filename", "upload_time", "status", "record_id"]
             if c in df_rep.columns]
        ].rename(columns={
            "report_id": "Report ID",
            "filename": "Filename",
            "upload_time": "Uploaded At",
            "status": "Status",
            "record_id": "Linked Record ID",
        })

        def colour_status(val):
            colours = {"processed": "background-color: #d5f5e3",
                       "pending": "background-color: #fef9e7",
                       "failed": "background-color: #fadbd8"}
            return colours.get(val, "")

        st.dataframe(
            display.style.applymap(colour_status, subset=["Status"]),
            use_container_width=True,
            hide_index=True,
        )
