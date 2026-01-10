"""Artwork table widget for displaying artworks."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                              QPushButton, QHBoxLayout, QLineEdit, QLabel, QHeaderView)
from PyQt6.QtCore import pyqtSignal, Qt
from core.repositories import ArtworkRepository


class ArtworkTableWidget(QWidget):
    """Widget for displaying and managing a table of artworks."""
    
    artwork_selected = pyqtSignal(int)  # Emits artwork ID when selected
    artwork_double_clicked = pyqtSignal(int)  # Emits artwork ID when double-clicked
    
    def __init__(self, parent=None):
        """Initialize artwork table widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.artwork_repo = ArtworkRepository()
        self.init_ui()
        self.load_artworks()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search artworks...")
        self.search_input.textChanged.connect(self.filter_artworks)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Artwork table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Title', 'Artist', 'Year', 'Medium', 'Dimensions'])
        
        # Configure table
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        layout.addWidget(self.table_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_artworks)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def load_artworks(self):
        """Load all artworks from the database."""
        self.table_widget.setRowCount(0)
        artworks = self.artwork_repo.get_all_with_artists()
        
        self.table_widget.setRowCount(len(artworks))
        for row, artwork in enumerate(artworks):
            self._populate_row(row, artwork)
    
    def filter_artworks(self, query: str):
        """Filter artworks by search query.
        
        Args:
            query: Search query string
        """
        self.table_widget.setRowCount(0)
        
        if query.strip():
            artworks = self.artwork_repo.search(query)
            # Need to get artist names for search results
            artworks_with_artists = []
            for artwork in artworks:
                artwork_data = self.artwork_repo.get_with_artist(artwork['id'])
                if artwork_data:
                    artworks_with_artists.append(artwork_data)
            artworks = artworks_with_artists
        else:
            artworks = self.artwork_repo.get_all_with_artists()
        
        self.table_widget.setRowCount(len(artworks))
        for row, artwork in enumerate(artworks):
            self._populate_row(row, artwork)
    
    def _populate_row(self, row: int, artwork: dict):
        """Populate a table row with artwork data.
        
        Args:
            row: Row index
            artwork: Artwork dictionary
        """
        # Title
        title_item = QTableWidgetItem(artwork['title'])
        title_item.setData(Qt.ItemDataRole.UserRole, artwork['id'])  # Store artwork ID
        self.table_widget.setItem(row, 0, title_item)
        
        # Artist
        artist_name = artwork.get('artist_name', 'Unknown')
        self.table_widget.setItem(row, 1, QTableWidgetItem(artist_name))
        
        # Year
        year = str(artwork['year']) if artwork.get('year') else ''
        self.table_widget.setItem(row, 2, QTableWidgetItem(year))
        
        # Medium
        medium = artwork.get('medium', '')
        self.table_widget.setItem(row, 3, QTableWidgetItem(medium or ''))
        
        # Dimensions
        dimensions = artwork.get('dimensions', '')
        self.table_widget.setItem(row, 4, QTableWidgetItem(dimensions or ''))
    
    def on_selection_changed(self):
        """Handle selection change in the table."""
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            item = self.table_widget.item(current_row, 0)
            if item:
                artwork_id = item.data(Qt.ItemDataRole.UserRole)
                self.artwork_selected.emit(artwork_id)
    
    def on_cell_double_clicked(self, row: int, column: int):
        """Handle double-click on a cell.
        
        Args:
            row: Row index
            column: Column index
        """
        item = self.table_widget.item(row, 0)
        if item:
            artwork_id = item.data(Qt.ItemDataRole.UserRole)
            self.artwork_double_clicked.emit(artwork_id)
    
    def get_selected_artwork_id(self) -> int:
        """Get the currently selected artwork ID.
        
        Returns:
            Artwork ID or None if no selection
        """
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            item = self.table_widget.item(current_row, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None
