# main.py
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from core.database import init_db
from ui.main_window import MainWindow


def ensure_dirs():
    """Create necessary directory structure for data storage."""
    base = Path(__file__).parent
    (base / "data").mkdir(exist_ok=True)
    (base / "data/images/artists").mkdir(parents=True, exist_ok=True)
    (base / "data/images/artworks").mkdir(parents=True, exist_ok=True)
    (base / "data/images/exhibitions").mkdir(parents=True, exist_ok=True)
    (base / "data/documents/invoices").mkdir(parents=True, exist_ok=True)
    (base / "data/documents/contracts").mkdir(parents=True, exist_ok=True)
    (base / "data/documents/certificates").mkdir(parents=True, exist_ok=True)
    (base / "data/backups").mkdir(parents=True, exist_ok=True)


def main():
    ensure_dirs()
    init_db()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
