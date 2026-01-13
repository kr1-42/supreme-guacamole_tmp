"""
Artwork Table Widget
Custom widget for displaying and managing artworks
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt, pyqtSignal


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
            "Title", "Artist", "Type", "Year", "Price", "Artist %", "Final Price", "Status"
        ])

        # Table settings
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
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

            # Title
            title_item = QTableWidgetItem(artwork.get('title', ''))
            title_item.setData(Qt.UserRole, artwork.get('id'))
            self.table.setItem(row, 0, title_item)

            # Artist
            artist_item = QTableWidgetItem(artwork.get('artist_name', 'Unknown'))
            self.table.setItem(row, 1, artist_item)

            # Type
            type_item = QTableWidgetItem(artwork.get('type', ''))
            self.table.setItem(row, 2, type_item)

            # Year
            year = artwork.get('year')
            year_item = QTableWidgetItem(str(year) if year else '')
            self.table.setItem(row, 3, year_item)

            # Price
            price = artwork.get('price')
            price_item = QTableWidgetItem(f"€ {price:.2f}" if price else '')
            self.table.setItem(row, 4, price_item)

            # Artist cut
            cut = artwork.get('artist_cut_percent')
            cut_item = QTableWidgetItem(f"{cut:.2f}%" if cut is not None else '')
            self.table.setItem(row, 5, cut_item)

            # Final Price (price / (artist_cut_percent / 100))
            final_price = None
            if price is not None and cut is not None and cut > 0:
                final_price = (price * cut) / 100
            final_price_item = QTableWidgetItem(f"€ {final_price:.2f}" if final_price else '')
            self.table.setItem(row, 6, final_price_item)

            # Status
            status_item = QTableWidgetItem(artwork.get('status', 'available'))
            self.table.setItem(row, 7, status_item)

        # Resize columns to content
        self.table.resizeColumnsToContents()

    def clear(self):
        """Clear the table"""
        self.table.setRowCount(0)

    def get_selected_artwork_id(self):
        """Get currently selected artwork ID"""
        row = self.table.currentRow()
        if row >= 0:
            return self.table.item(row, 0).data(Qt.UserRole)
        return None
