from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QTableWidget,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    """
    Main application window
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Art Catalog Manager")
        self.resize(1200, 700)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        main_layout = QHBoxLayout()

        # =========================
        # ARTISTS LIST
        # =========================
        self.artist_list = QListWidget()
        self.artist_list.setFixedWidth(250)

        # =========================
        # ARTWORK TABLE
        # =========================
        self.artwork_table = QTableWidget()
        self.artwork_table.setColumnCount(4)
        self.artwork_table.setHorizontalHeaderLabels(
            ["Title", "Type", "Year", "Status"]
        )

        # =========================
        # RIGHT PANEL
        # =========================
        right_panel = QVBoxLayout()

        self.preview = QLabel("Artwork preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(200)
        self.preview.setStyleSheet("border: 1px solid #999;")

        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        right_panel.addWidget(self.preview)
        right_panel.addWidget(self.add_btn)
        right_panel.addWidget(self.edit_btn)
        right_panel.addWidget(self.delete_btn)
        right_panel.addStretch()

        # =========================
        # LAYOUT ASSEMBLY
        # =========================
        main_layout.addWidget(self.artist_list)
        main_layout.addWidget(self.artwork_table, 1)
        main_layout.addLayout(right_panel)

        central.setLayout(main_layout)
        self.setCentralWidget(central)
