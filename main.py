"""
Art Catalog Manager
Main entry point
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtGui import QPalette, QColor

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
def _apply_dark_theme(app: QApplication):
    """Force a dark theme for the entire application."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
    palette.setColor(QPalette.ToolTipBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipText, QColor(10, 10, 10))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    # Ensure backgrounds stay dark even if a widget doesn't use the palette
    app.setStyleSheet(
        """
        QWidget { background-color: #1e1e1e; color: #ddd; }
        QLabel { background-color: transparent; }
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
            background-color: #252526; color: #ddd; border: 1px solid #555;
        }
        QListWidget, QTableWidget, QTreeWidget, QScrollArea {
            background-color: #1e1e1e; color: #ddd;
        }
        QMenuBar, QMenu { background-color: #1e1e1e; color: #ddd; }
        QPushButton { background-color: #2d2d2d; color: #ddd; border: 1px solid #555; padding: 6px; }
        QPushButton:hover { background-color: #3a3a3a; }
        QPushButton:pressed { background-color: #1a1a1a; }
        QToolTip { color: #111; background-color: #f0f0f0; border: 1px solid #999; }
        """
    )


def main():
    init_database()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    _apply_dark_theme(app)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
