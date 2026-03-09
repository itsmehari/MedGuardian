"""
Data loader utility for MedGuardian.

Loads sample CSV datasets (patients, health records) into the database.
Useful for demos and when the database is empty.

Run from project root:
    python -m utils.data_loader
"""

import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Resolve paths relative to project root (parent of utils/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_PATIENTS = DATA_DIR / "sample_patients.csv"
SAMPLE_RECORDS = DATA_DIR / "sample_health_records.csv"


def _float_or_none(val: str) -> float | None:
    """Convert string to float, or None if empty/zero."""
    if not val or not val.strip():
        return None
    try:
        f = float(val.strip())
        return None if f == 0.0 else f
    except ValueError:
        return None


def load_sample_data(force: bool = False) -> dict:
    """
    Load sample patients and health records from CSV into the database.

    Args:
        force: If True, load even if DB already has data. Default False.

    Returns:
        Dict with counts: {"patients": N, "health_records": M}
    """
    from database.db_handler import (
        get_all_users,
        insert_user,
        insert_health_record,
    )

    users = get_all_users()
    if users and not force:
        logger.info("Database already has data. Use force=True to load anyway.")
        return {"patients": len(users), "health_records": "skipped"}

    counts = {"patients": 0, "health_records": 0}
    id_map = {}  # CSV row index -> actual user_id from DB

    # Load patients
    if SAMPLE_PATIENTS.exists():
        with open(SAMPLE_PATIENTS, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                name = (row.get("name") or "").strip()
                if not name:
                    continue
                try:
                    uid = insert_user(
                        name=name,
                        age=int(row.get("age", 30)),
                        gender=row.get("gender", "Male"),
                        email=(row.get("email") or "").strip() or None,
                    )
                    id_map[i] = uid
                    counts["patients"] += 1
                except Exception as e:
                    logger.warning("Skipped row %d: %s", i + 2, e)
    else:
        logger.warning("Sample patients file not found: %s", SAMPLE_PATIENTS)

    # Build reverse map: if user_id in CSV matches our new IDs
    # CSV user_id 1 -> first inserted, 2 -> second, etc.
    csv_id_to_db = {}
    for i, uid in sorted(id_map.items()):
        csv_id_to_db[i + 1] = uid  # CSV uses 1-based user_id

    # Load health records (user_id in CSV refers to 1-based position in patients file)
    if SAMPLE_RECORDS.exists() and csv_id_to_db:
        with open(SAMPLE_RECORDS, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    csv_uid = int(row.get("user_id", 0))
                    db_uid = csv_id_to_db.get(csv_uid)
                    if not db_uid:
                        continue
                    test_date = (row.get("test_date") or "").strip()
                    if not test_date:
                        continue
                    insert_health_record(
                        user_id=db_uid,
                        test_date=test_date,
                        glucose=_float_or_none(row.get("glucose")),
                        hba1c=_float_or_none(row.get("hba1c")),
                        bmi=_float_or_none(row.get("bmi")),
                        systolic_bp=_float_or_none(row.get("systolic_bp")),
                        diastolic_bp=_float_or_none(row.get("diastolic_bp")),
                        cholesterol=_float_or_none(row.get("cholesterol")),
                    )
                    counts["health_records"] += 1
                except Exception as e:
                    logger.warning("Skipped health record row: %s", e)
    elif SAMPLE_RECORDS.exists():
        logger.warning("No patients loaded; skipping health records.")
    else:
        logger.warning("Sample health records file not found: %s", SAMPLE_RECORDS)

    logger.info("Loaded sample data: %s", counts)
    return counts


if __name__ == "__main__":
    import sys
    from database.db_handler import create_tables

    create_tables()
    force = "--force" in sys.argv
    result = load_sample_data(force=force)
    print(f"Done: {result}")
