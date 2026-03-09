"""
Page 1 — Patient Profile

Allows creating new patient records and viewing / editing existing ones.
The selected patient is stored in ``st.session_state["current_user_id"]``
so other pages can pick it up automatically.
"""

import streamlit as st

from services.auth import require_auth, sidebar_user_info
from database.db_handler import (
    insert_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)

st.set_page_config(page_title="Patient Profile – MedGuardian", layout="wide")
require_auth()
sidebar_user_info()

st.title("👤 Patient Profile")
st.markdown("Create a new patient record or manage an existing one.")
st.divider()

tab_new, tab_manage = st.tabs(["➕ New Patient", "📋 Manage Existing"])

# ---------------------------------------------------------------------------
# Tab 1 — New Patient
# ---------------------------------------------------------------------------
with tab_new:
    with st.form("new_patient_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Full Name *", placeholder="e.g. Ravi Kumar")
            age = st.number_input("Age *", min_value=1, max_value=120, value=35, step=1)
        with col_b:
            gender = st.selectbox(
                "Gender *",
                ["Male", "Female", "Other", "Prefer not to say"],
            )
            email = st.text_input("Email (optional)", placeholder="ravi@example.com")

        submitted = st.form_submit_button("💾 Save Patient", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Patient name is required.")
        else:
            try:
                uid = insert_user(
                    name=name.strip(),
                    age=int(age),
                    gender=gender,
                    email=email.strip() or None,
                )
                st.session_state["current_user_id"] = uid
                st.success(
                    f"Patient **{name.strip()}** saved successfully (ID: {uid}). "
                    "They are now set as the active patient."
                )
            except Exception as exc:
                if "UNIQUE constraint" in str(exc):
                    st.error("A patient with that email address already exists.")
                else:
                    st.error(f"Could not save patient: {exc}")

# ---------------------------------------------------------------------------
# Tab 2 — Manage Existing
# ---------------------------------------------------------------------------
with tab_manage:
    users = get_all_users()

    if not users:
        st.info("No patients found. Create one in the **New Patient** tab.")
    else:
        options = {
            f"{u['name']}  (ID {u['user_id']}, age {u['age']}, {u['gender']})": u["user_id"]
            for u in users
        }
        selected_label = st.selectbox("Select a patient", list(options.keys()))
        selected_uid = options[selected_label]

        # Make this the active patient for the whole session
        st.session_state["current_user_id"] = selected_uid
        patient = get_user_by_id(selected_uid)

        if patient:
            st.subheader(f"Profile: {patient['name']}")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Age", patient.get("age", "—"))
            col2.metric("Gender", patient.get("gender", "—"))
            col3.metric("Email", patient.get("email") or "—")
            col4.metric("Patient ID", patient["user_id"])

            st.divider()

            # Inline edit form
            with st.expander("✏️ Edit this patient"):
                with st.form("edit_patient_form"):
                    e_col1, e_col2 = st.columns(2)
                    with e_col1:
                        e_name = st.text_input("Full Name", value=patient["name"])
                        e_age = st.number_input(
                            "Age",
                            min_value=1,
                            max_value=120,
                            value=patient.get("age") or 30,
                        )
                    with e_col2:
                        gender_opts = ["Male", "Female", "Other", "Prefer not to say"]
                        current_gender = patient.get("gender") or "Male"
                        idx = gender_opts.index(current_gender) if current_gender in gender_opts else 0
                        e_gender = st.selectbox("Gender", gender_opts, index=idx)
                        e_email = st.text_input(
                            "Email",
                            value=patient.get("email") or "",
                        )
                    save_edit = st.form_submit_button("Update Patient")

                if save_edit:
                    if not e_name.strip():
                        st.error("Name cannot be empty.")
                    else:
                        try:
                            update_user(
                                selected_uid,
                                e_name.strip(),
                                int(e_age),
                                e_gender,
                                e_email.strip() or None,
                            )
                            st.success("Patient record updated.")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Update failed: {exc}")

            # Delete with confirmation
            with st.expander("🗑️ Delete this patient"):
                st.warning(
                    "Deleting a patient will also remove all their health records, "
                    "risk scores, and uploaded reports. This cannot be undone."
                )
                confirm_del = st.checkbox(
                    f"I confirm I want to delete **{patient['name']}**"
                )
                if st.button("Delete Patient", disabled=not confirm_del):
                    delete_user(selected_uid)
                    st.session_state.pop("current_user_id", None)
                    st.success("Patient deleted.")
                    st.rerun()
