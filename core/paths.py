"""
Path configuration for Art Catalog Manager
"""

from pathlib import Path


# =========================================================
# APPLICATION PATHS (LOCAL PROJECT DIR)
# =========================================================
# Anchor to the project directory so data lives alongside the codebase.
APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data"
IMG_DIR = APP_DIR / "images" / "artworks"
BACKUP_DIR = APP_DIR / "backups"

# Database path
DB_PATH = DATA_DIR / "catalog.db"


def ensure_paths():
    """
    Ensure all application directories exist
    """
    for d in (DATA_DIR, IMG_DIR, BACKUP_DIR):
        d.mkdir(parents=True, exist_ok=True)
