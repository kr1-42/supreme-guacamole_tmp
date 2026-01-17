from pathlib import Path
import shutil

from PyQt5.QtWidgets import QMainWindow, QMessageBox

from core.database import Database
from core.paths import IMG_DIR, DB_PATH, ensure_paths
from core.repositories.artist_repo import ArtistRepository
from core.repositories.artwork_repo import ArtworkRepository
from core.repositories.sale_repo import SaleRepository
from ui.controllers.artist_controller import ArtistController
from ui.controllers.artwork_controller import ArtworkController
from ui.layouts.main_layout import build_main_layout


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_IMAGES_DIR = PROJECT_ROOT / "assets" / "test_images"


class MainWindow(QMainWindow):
    """
    Main application window
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Art Catalog Manager")
        self.resize(1200, 700)
        self.setAcceptDrops(True)
        
        # Set application-wide font size
        font = self.font()
        font.setPointSize(11)
        self.setFont(font)

        ensure_paths()
        self.db = Database(DB_PATH)
        self.artist_repo = ArtistRepository(self.db)
        self.artwork_repo = ArtworkRepository(self.db)
        self.sale_repo = SaleRepository(self.db)

        self._build_ui()
        self.artist_controller.load_artists()
        self.artwork_controller.load_artworks()

    def _build_ui(self):
        central, refs = build_main_layout()
        self.setCentralWidget(central)

        self.artist_list = refs["artist_list"]
        self.artwork_table = refs["artwork_table"]
        self.artwork_count_label = refs["artwork_count_label"]
        self.add_btn = refs["add_btn"]
        self.edit_btn = refs["edit_btn"]
        self.delete_btn = refs["delete_btn"]
        self.sell_btn = refs["sell_btn"]

        # Controllers
        self.artwork_controller = ArtworkController(
            self.artwork_repo,
            self.artist_repo,
            self.artwork_table,
            None,
            self.artwork_count_label,
            self.sale_repo,
        )
        self.artist_controller = ArtistController(
            self.artist_repo,
            self.artist_list,
            self.artwork_controller.load_artworks,
        )

        # Wiring
        self.artist_list.artist_selected.connect(self.artist_controller.on_artist_selected)
        self.artist_list.artist_double_clicked.connect(self.artist_controller.on_artist_double_click)
        self.artist_list.add_btn.clicked.connect(self.artist_controller.add_artist)

        self.artwork_table.artwork_selected.connect(self.artwork_controller.on_artwork_selected)
        self.artwork_table.artwork_double_clicked.connect(self.artwork_controller.edit_artwork)

        self.add_btn.clicked.connect(self.artwork_controller.add_artwork)
        self.edit_btn.clicked.connect(self.artwork_controller.edit_artwork)
        self.delete_btn.clicked.connect(self.artwork_controller.delete_artwork)
        self.sell_btn.clicked.connect(self.artwork_controller.sell_artwork)

    # =========================
    # DRAG & DROP (WINDOW LEVEL)
    # =========================
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and self.artwork_controller.handle_drop(event.mimeData().urls()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls() and self.artwork_controller.handle_drop(event.mimeData().urls()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)
