"""
Artwork Table Widget
Custom widget for displaying and managing artworks
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QLabel,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from core.paths import IMG_DIR


class ArtworkTableWidget(QWidget):
    """
    Widget displaying artworks in a table format
    """

    artwork_selected = pyqtSignal(int)  # Emits artwork ID when selected
    artwork_double_clicked = pyqtSignal(int)  # Emits artwork ID on double click

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Title", "Artist", "Image", "Price", "Artist %", "Final Price", "Qty", "Status"
        ])

        # Table settings
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(2, 150)  # Image column width
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.itemDoubleClicked.connect(self._on_double_click)

        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _on_selection_changed(self):
        """Emit signal when selection changes"""
        row = self.table.currentRow()
        if row >= 0:
            artwork_id = self.table.item(row, 0).data(Qt.UserRole)
            if artwork_id:
                self.artwork_selected.emit(artwork_id)

    def _on_double_click(self, item):
        """Emit signal on double click"""
        row = item.row()
        artwork_id = self.table.item(row, 0).data(Qt.UserRole)
        if artwork_id:
            self.artwork_double_clicked.emit(artwork_id)

    def load_artworks(self, artworks):
        """Load artworks into the table"""
        self.table.setRowCount(0)

        for artwork in artworks:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setRowHeight(row, 150)  # Set row height for image

            # Title
            title_item = QTableWidgetItem(artwork.get('title', ''))
            title_item.setData(Qt.UserRole, artwork.get('id'))
            self.table.setItem(row, 0, title_item)

            # Artist
            artist_item = QTableWidgetItem(artwork.get('artist_name', 'Unknown'))
            self.table.setItem(row, 1, artist_item)

            # Image
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignCenter)
            image_name = artwork.get('image', '')
            if image_name:
                image_path = IMG_DIR / image_name
                if image_path.exists():
                    pixmap = QPixmap(str(image_path))
                    if not pixmap.isNull():
                        scaled = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        image_label.setPixmap(scaled)
                    else:
                        image_label.setText("Invalid")
                else:
                    image_label.setText("Not found")
            else:
                image_label.setText("No image")
            self.table.setCellWidget(row, 2, image_label)

            # Price
            price = artwork.get('price')
            price_item = QTableWidgetItem(f"€ {price:.2f}" if price else '')
            self.table.setItem(row, 3, price_item)

            # Artist cut
            cut = artwork.get('artist_cut_percent')
            cut_item = QTableWidgetItem(f"{cut:.2f}%" if cut is not None else '')
            self.table.setItem(row, 4, cut_item)

            # Final Price
            final_price = None
            if price is not None and cut is not None and cut > 0:
                final_price = (price * cut) / 100
            final_price_item = QTableWidgetItem(f"€ {final_price:.2f}" if final_price else '')
            self.table.setItem(row, 5, final_price_item)

            # Quantity
            qty = artwork.get('quantity')
            qty_item = QTableWidgetItem(str(qty) if qty is not None else '')
            self.table.setItem(row, 6, qty_item)

            # Status
            status_item = QTableWidgetItem(artwork.get('status', 'available'))
            self.table.setItem(row, 7, status_item)

        # Resize columns to content (except image column)
        for col in range(self.table.columnCount()):
            if col != 2:
                self.table.resizeColumnToContents(col)

    def clear(self):
        """Clear the table"""
        self.table.setRowCount(0)

    def get_selected_artwork_id(self):
        """Get currently selected artwork ID"""
        row = self.table.currentRow()
        if row >= 0:
            return self.table.item(row, 0).data(Qt.UserRole)
        return None
