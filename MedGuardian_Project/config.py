import os
import logging
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Database — absolute path so the file always lands next to this config module
DB_PATH: str = os.getenv("MEDGUARDIAN_DB_PATH", str(BASE_DIR / "medguardian.db"))

# Auth credentials — override via .env before deploying
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
# Default is sha256("admin123") — CHANGE THIS before any real deployment
ADMIN_PASSWORD_HASH: str = os.getenv(
    "ADMIN_PASSWORD_HASH",
    "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
)

DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

LOG_FILE: str = str(BASE_DIR / "medguardian.log")

# ------------------------------------------------------------------
# Logging — configured once here; all modules use logging.getLogger()
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
