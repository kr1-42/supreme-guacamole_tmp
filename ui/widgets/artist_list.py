"""Artist list widget for displaying artists."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                              QPushButton, QHBoxLayout, QLineEdit, QLabel)
from PyQt6.QtCore import pyqtSignal
from core.repositories import ArtistRepository


class ArtistListWidget(QWidget):
    """Widget for displaying and managing a list of artists."""
    
    artist_selected = pyqtSignal(int)  # Emits artist ID when selected
    artist_double_clicked = pyqtSignal(int)  # Emits artist ID when double-clicked
    
    def __init__(self, parent=None):
        """Initialize artist list widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.artist_repo = ArtistRepository()
        self.init_ui()
        self.load_artists()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search artists...")
        self.search_input.textChanged.connect(self.filter_artists)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Artist list
        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_artists)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def load_artists(self):
        """Load all artists from the database."""
        self.list_widget.clear()
        artists = self.artist_repo.get_all()
        
        for artist in artists:
            item = QListWidgetItem(self._format_artist(artist))
            item.setData(1, artist['id'])  # Store artist ID in item data
            self.list_widget.addItem(item)
    
    def filter_artists(self, query: str):
        """Filter artists by search query.
        
        Args:
            query: Search query string
        """
        self.list_widget.clear()
        
        if query.strip():
            artists = self.artist_repo.search(query)
        else:
            artists = self.artist_repo.get_all()
        
        for artist in artists:
            item = QListWidgetItem(self._format_artist(artist))
            item.setData(1, artist['id'])
            self.list_widget.addItem(item)
    
    def _format_artist(self, artist: dict) -> str:
        """Format artist data for display.
        
        Args:
            artist: Artist dictionary
            
        Returns:
            Formatted string
        """
        name = artist['name']
        if artist.get('birth_year'):
            name += f" (b. {artist['birth_year']})"
        if artist.get('nationality'):
            name += f" - {artist['nationality']}"
        return name
    
    def on_selection_changed(self):
        """Handle selection change in the list."""
        items = self.list_widget.selectedItems()
        if items:
            artist_id = items[0].data(1)
            self.artist_selected.emit(artist_id)
    
    def on_item_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on an item.
        
        Args:
            item: The clicked list item
        """
        artist_id = item.data(1)
        self.artist_double_clicked.emit(artist_id)
    
    def get_selected_artist_id(self) -> int:
        """Get the currently selected artist ID.
        
        Returns:
            Artist ID or None if no selection
        """
        items = self.list_widget.selectedItems()
        return items[0].data(1) if items else None
