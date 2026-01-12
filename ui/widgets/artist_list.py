"""
Artist List Widget
Custom widget for displaying and managing artists
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal


class ArtistListWidget(QWidget):
    """
    Widget displaying a searchable list of artists
    """

    artist_selected = pyqtSignal(int)  # Emits artist ID when selected
    artist_double_clicked = pyqtSignal(int)  # Emits artist ID on double click

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Artists")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")

        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search artists...")
        self.search_input.textChanged.connect(self._on_search)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        self.list_widget.itemDoubleClicked.connect(self._on_double_click)

        # Add button
        self.add_btn = QPushButton("+ Add Artist")

        layout.addWidget(title)
        layout.addWidget(self.search_input)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.add_btn)

        self.setLayout(layout)

    def _on_search(self, text):
        """Filter artists based on search text"""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def _on_selection_changed(self):
        """Emit signal when selection changes"""
        items = self.list_widget.selectedItems()
        if items:
            artist_id = items[0].data(Qt.UserRole)
            if artist_id:
                self.artist_selected.emit(artist_id)

    def _on_double_click(self, item):
        """Emit signal on double click"""
        artist_id = item.data(Qt.UserRole)
        if artist_id:
            self.artist_double_clicked.emit(artist_id)

    def load_artists(self, artists):
        """Load artists into the list"""
        self.list_widget.clear()
        for artist in artists:
            item_text = artist.get('name', 'Unknown')
            item = self.list_widget.addItem(item_text)
            # Store artist ID in item data
            self.list_widget.item(self.list_widget.count() - 1).setData(
                Qt.UserRole, artist.get('id')
            )

    def clear(self):
        """Clear the list"""
        self.list_widget.clear()

    def get_selected_artist_id(self):
        """Get currently selected artist ID"""
        items = self.list_widget.selectedItems()
        if items:
            return items[0].data(Qt.UserRole)
        return None
