import sqlite3
import logging
from typing import Any, Dict, List, Optional

from config import DB_PATH

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database with row-dict support."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

def create_tables() -> None:
    """Create all application tables if they do not already exist."""
    ddl_statements = [
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL,
            age        INTEGER,
            gender     TEXT,
            email      TEXT    UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS health_records (
            record_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL
                             REFERENCES users(user_id) ON DELETE CASCADE,
            test_date    TEXT,
            glucose      REAL,
            hba1c        REAL,
            bmi          REAL,
            systolic_bp  REAL,
            diastolic_bp REAL,
            cholesterol  REAL,
            created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS risk_scores (
            score_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL
                            REFERENCES users(user_id) ON DELETE CASCADE,
            record_id   INTEGER
                            REFERENCES health_records(record_id) ON DELETE SET NULL,
            condition   TEXT    NOT NULL,
            risk_score  REAL    NOT NULL,
            risk_level  TEXT    NOT NULL,
            computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS uploaded_reports (
            report_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id        INTEGER NOT NULL
                               REFERENCES users(user_id) ON DELETE CASCADE,
            filename       TEXT,
            upload_time    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status         TEXT DEFAULT 'pending',
            extracted_text TEXT,
            record_id      INTEGER
                               REFERENCES health_records(record_id) ON DELETE SET NULL
        )
        """,
    ]

    try:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            for stmt in ddl_statements:
                cursor.execute(stmt)
            conn.commit()
            logger.info("Database tables created / verified at: %s", DB_PATH)
        finally:
            conn.close()
    except sqlite3.Error as exc:
        logger.error("Failed to initialise database tables: %s", exc)
        raise


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def insert_user(
    name: str,
    age: int,
    gender: str,
    email: Optional[str] = None,
) -> int:
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (name, age, gender, email) VALUES (?, ?, ?, ?)",
            (name, age, gender, email),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_users() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM users ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_user(
    user_id: int,
    name: str,
    age: int,
    gender: str,
    email: Optional[str] = None,
) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE users SET name=?, age=?, gender=?, email=? WHERE user_id=?",
            (name, age, gender, email, user_id),
        )
        conn.commit()
    finally:
        conn.close()


def delete_user(user_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Health Records
# ---------------------------------------------------------------------------

def insert_health_record(
    user_id: int,
    test_date: str,
    glucose: Optional[float] = None,
    hba1c: Optional[float] = None,
    bmi: Optional[float] = None,
    systolic_bp: Optional[float] = None,
    diastolic_bp: Optional[float] = None,
    cholesterol: Optional[float] = None,
) -> int:
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO health_records
               (user_id, test_date, glucose, hba1c, bmi,
                systolic_bp, diastolic_bp, cholesterol)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, test_date, glucose, hba1c, bmi,
             systolic_bp, diastolic_bp, cholesterol),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_health_records_by_user(user_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM health_records WHERE user_id=? ORDER BY test_date DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_health_record_by_id(record_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM health_records WHERE record_id=?", (record_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Risk Scores
# ---------------------------------------------------------------------------

def insert_risk_score(
    user_id: int,
    condition: str,
    risk_score: float,
    risk_level: str,
    record_id: Optional[int] = None,
) -> int:
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO risk_scores
               (user_id, record_id, condition, risk_score, risk_level)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, record_id, condition, risk_score, risk_level),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_risk_scores_by_user(user_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM risk_scores WHERE user_id=? ORDER BY computed_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Uploaded Reports
# ---------------------------------------------------------------------------

def insert_uploaded_report(
    user_id: int,
    filename: str,
    extracted_text: Optional[str] = None,
    record_id: Optional[int] = None,
    status: str = "pending",
) -> int:
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO uploaded_reports
               (user_id, filename, extracted_text, record_id, status)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, filename, extracted_text, record_id, status),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_report_status(
    report_id: int,
    status: str,
    record_id: Optional[int] = None,
    extracted_text: Optional[str] = None,
) -> None:
    """Update report status. Only updates extracted_text if explicitly provided."""
    conn = get_connection()
    try:
        if extracted_text is not None:
            conn.execute(
                """UPDATE uploaded_reports
                   SET status=?, record_id=?, extracted_text=?
                   WHERE report_id=?""",
                (status, record_id, extracted_text, report_id),
            )
        else:
            conn.execute(
                """UPDATE uploaded_reports
                   SET status=?, record_id=COALESCE(?, record_id)
                   WHERE report_id=?""",
                (status, record_id, report_id),
            )
        conn.commit()
    finally:
        conn.close()


def get_reports_by_user(user_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM uploaded_reports WHERE user_id=? ORDER BY upload_time DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
