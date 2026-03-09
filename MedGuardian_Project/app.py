import logging

import streamlit as st

from database.db_handler import create_tables
from services.auth import require_auth, sidebar_user_info

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="MedGuardian",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialise database on every cold start (idempotent — uses CREATE IF NOT EXISTS)
try:
    create_tables()
except Exception as exc:
    st.error(
        "⚠️ Database initialisation failed. Check the logs for details.\n\n"
        f"Error: {exc}"
    )
    logger.critical("create_tables() failed on startup: %s", exc)
    st.stop()

require_auth()
sidebar_user_info()

# Offer to load or reset sample data
from database.db_handler import get_all_users, clear_all_data
users = get_all_users()
if not users:
    with st.expander("📥 Load sample demo data", expanded=True):
        st.caption(
            "No patients found. Load sample patients and health records for demo?"
        )
        if st.button("Load sample data", type="primary"):
            try:
                from utils.data_loader import load_sample_data
                result = load_sample_data(force=True)
                st.success(
                    f"Loaded {result.get('patients', 0)} patients and "
                    f"{result.get('health_records', 0)} health records."
                )
                st.rerun()
            except Exception as e:
                st.error(f"Failed to load sample data: {e}")
else:
    with st.expander("🔄 Reset & load fresh sample data", expanded=False):
        st.caption(
            "Clear all existing patients and data, then load the 15 sample profiles "
            "(matching the sample PDF lab reports)."
        )
        if st.button("Reset database and load sample data", type="secondary"):
            try:
                clear_all_data()
                from utils.data_loader import load_sample_data
                result = load_sample_data(force=True)
                st.success(
                    f"Reset complete. Loaded {result.get('patients', 0)} patients and "
                    f"{result.get('health_records', 0)} health records."
                )
                st.rerun()
            except Exception as e:
                st.error(f"Failed: {e}")

# ---------------------------------------------------------------------------
# Home page content
# ---------------------------------------------------------------------------
st.title("🏥 MedGuardian")
st.subheader("AI-Assisted Early Disease Detection System")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.info("**Step 1**\n\nCreate a patient profile on the **Patient Profile** page.")
col2.info("**Step 2**\n\nUpload a PDF lab report on the **Upload Report** page.")
col3.info("**Step 3**\n\nCompute risk scores on the **Risk Dashboard** page.")
col4.info("**Step 4**\n\nTrack trends over time on the **History** page.")

st.divider()

st.markdown(
    """
    ### What MedGuardian analyses

    | Condition | Biomarkers Used |
    |---|---|
    | **Diabetes Risk** | Fasting Glucose, HbA1c, BMI, Family History |
    | **Hypertension Risk** | Systolic BP, Diastolic BP |
    | **Cholesterol Risk** | Total Cholesterol |

    Risk scores are on a **0 – 100 %** scale:
    - 🟢 **0 – 20 %** — Low risk
    - 🟡 **21 – 50 %** — Moderate risk
    - 🔴 **51 – 100 %** — High risk

    Data is stored in a SQLite database on the deployment server.
    No data is sent to any external service.
    """
)
