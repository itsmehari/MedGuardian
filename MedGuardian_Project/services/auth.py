"""
Simple session-state based authentication for MedGuardian.

Credentials are stored in config.py (loaded from .env). For a
production deployment replace this with a proper identity provider
or the ``streamlit-authenticator`` library.
"""

import hashlib
import streamlit as st

from config import ADMIN_USERNAME, ADMIN_PASSWORD_HASH


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _check_credentials(username: str, password: str) -> bool:
    return username == ADMIN_USERNAME and _hash(password) == ADMIN_PASSWORD_HASH


def login_page() -> None:
    """Render the login form. Stops the page if not yet authenticated."""
    st.set_page_config(page_title="MedGuardian – Login", layout="centered")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🏥 MedGuardian")
        st.markdown("### AI-Assisted Early Disease Detection System")
        st.divider()

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if _check_credentials(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

        st.caption("Default credentials: admin / admin123  ·  Change in .env before deployment.")


def require_auth() -> None:
    """
    Guard function — call at the top of every page script.

    If the user is not authenticated, renders the login form and halts
    page execution via ``st.stop()``.
    """
    if not st.session_state.get("authenticated"):
        login_page()
        st.stop()


def logout() -> None:
    """Clear session state and force a re-run to show the login form."""
    st.session_state.clear()
    st.rerun()


def sidebar_user_info() -> None:
    """Render the logged-in username and a logout button in the sidebar."""
    with st.sidebar:
        st.markdown(f"**Logged in as:** `{st.session_state.get('username', '')}`")
        if st.button("Logout", use_container_width=True):
            logout()
        st.divider()
