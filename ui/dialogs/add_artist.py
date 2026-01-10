"""Dialog for adding a new artist."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QTextEdit, QSpinBox, QPushButton,
                              QFormLayout, QMessageBox)
from core.repositories import ArtistRepository


class AddArtistDialog(QDialog):
    """Dialog for adding or editing an artist."""
    
    def __init__(self, parent=None, artist_id: int = None):
        """Initialize add artist dialog.
        
        Args:
            parent: Parent widget
            artist_id: If provided, edit this artist instead of creating new
        """
        super().__init__(parent)
        self.artist_repo = ArtistRepository()
        self.artist_id = artist_id
        self.init_ui()
        
        if artist_id:
            self.load_artist(artist_id)
            self.setWindowTitle("Edit Artist")
        else:
            self.setWindowTitle("Add Artist")
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter artist name")
        form_layout.addRow("Name:*", self.name_input)
        
        # Birth year
        self.birth_year_input = QSpinBox()
        self.birth_year_input.setRange(1000, 2100)
        self.birth_year_input.setValue(1900)
        self.birth_year_input.setSpecialValueText("Unknown")
        self.birth_year_input.setMinimum(0)
        form_layout.addRow("Birth Year:", self.birth_year_input)
        
        # Nationality
        self.nationality_input = QLineEdit()
        self.nationality_input.setPlaceholderText("Enter nationality")
        form_layout.addRow("Nationality:", self.nationality_input)
        
        # Biography
        self.biography_input = QTextEdit()
        self.biography_input.setPlaceholderText("Enter biography")
        self.biography_input.setMaximumHeight(150)
        form_layout.addRow("Biography:", self.biography_input)
        
        layout.addLayout(form_layout)
        
        # Required field note
        note_label = QLabel("* Required field")
        note_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(note_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_artist)
        self.save_button.setDefault(True)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def load_artist(self, artist_id: int):
        """Load artist data into the form.
        
        Args:
            artist_id: Artist ID to load
        """
        artist = self.artist_repo.get_by_id(artist_id)
        if artist:
            self.name_input.setText(artist['name'])
            if artist.get('birth_year'):
                self.birth_year_input.setValue(artist['birth_year'])
            if artist.get('nationality'):
                self.nationality_input.setText(artist['nationality'])
            if artist.get('biography'):
                self.biography_input.setPlainText(artist['biography'])
    
    def save_artist(self):
        """Save the artist data."""
        name = self.name_input.text().strip()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Validation Error", "Artist name is required.")
            self.name_input.setFocus()
            return
        
        birth_year = self.birth_year_input.value() if self.birth_year_input.value() > 0 else None
        nationality = self.nationality_input.text().strip() or None
        biography = self.biography_input.toPlainText().strip() or None
        
        try:
            if self.artist_id:
                # Update existing artist
                self.artist_repo.update(
                    self.artist_id,
                    name=name,
                    birth_year=birth_year,
                    nationality=nationality,
                    biography=biography
                )
            else:
                # Create new artist
                self.artist_repo.create(
                    name=name,
                    birth_year=birth_year,
                    nationality=nationality,
                    biography=biography
                )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save artist: {str(e)}")
