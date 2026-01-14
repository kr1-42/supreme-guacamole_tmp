"""
Art Catalog Manager
Main entry point
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication

from core.database import Database
from core.schema import SCHEMA_SQL
from ui.main_window import MainWindow


# =========================================================
# APP PATHS (LOCAL PROJECT DIR)
# =========================================================
# Store app data inside the project folder instead of under the home directory.
APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
IMG_DIR = APP_DIR / "images" / "artworks"
BACKUP_DIR = APP_DIR / "backups"

for d in (DATA_DIR, IMG_DIR, BACKUP_DIR):
    d.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "catalog.db"


# =========================================================
# DB INIT
# =========================================================
def init_database():
    if DB_PATH.exists():
        return

    db = Database(DB_PATH)
    db.executescript(SCHEMA_SQL)
    db.close()


# =========================================================
# MAIN
# =========================================================
def main():
    init_database()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
