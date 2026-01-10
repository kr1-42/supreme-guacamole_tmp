"""Dialog for adding a new artwork."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QTextEdit, QSpinBox, QPushButton,
                              QFormLayout, QMessageBox, QComboBox, QFileDialog)
from pathlib import Path
from core.repositories import ArtworkRepository, ArtistRepository


class AddArtworkDialog(QDialog):
    """Dialog for adding or editing an artwork."""
    
    def __init__(self, parent=None, artwork_id: int = None):
        """Initialize add artwork dialog.
        
        Args:
            parent: Parent widget
            artwork_id: If provided, edit this artwork instead of creating new
        """
        super().__init__(parent)
        self.artwork_repo = ArtworkRepository()
        self.artist_repo = ArtistRepository()
        self.artwork_id = artwork_id
        self.selected_image_path = None
        self.init_ui()
        self.load_artists()
        
        if artwork_id:
            self.load_artwork(artwork_id)
            self.setWindowTitle("Edit Artwork")
        else:
            self.setWindowTitle("Add Artwork")
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setMinimumWidth(450)
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter artwork title")
        form_layout.addRow("Title:*", self.title_input)
        
        # Artist
        self.artist_combo = QComboBox()
        form_layout.addRow("Artist:*", self.artist_combo)
        
        # Year
        self.year_input = QSpinBox()
        self.year_input.setRange(0, 2100)
        self.year_input.setValue(2000)
        self.year_input.setSpecialValueText("Unknown")
        self.year_input.setMinimum(0)
        form_layout.addRow("Year:", self.year_input)
        
        # Medium
        self.medium_input = QLineEdit()
        self.medium_input.setPlaceholderText("e.g., Oil on canvas")
        form_layout.addRow("Medium:", self.medium_input)
        
        # Dimensions
        self.dimensions_input = QLineEdit()
        self.dimensions_input.setPlaceholderText("e.g., 100 x 80 cm")
        form_layout.addRow("Dimensions:", self.dimensions_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter description")
        self.description_input.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_input)
        
        # Image
        image_layout = QHBoxLayout()
        self.image_path_label = QLabel("No image selected")
        self.image_path_label.setStyleSheet("color: gray;")
        image_layout.addWidget(self.image_path_label)
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_image)
        image_layout.addWidget(self.browse_button)
        form_layout.addRow("Image:", image_layout)
        
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
        self.save_button.clicked.connect(self.save_artwork)
        self.save_button.setDefault(True)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def load_artists(self):
        """Load artists into the combo box."""
        self.artist_combo.clear()
        artists = self.artist_repo.get_all()
        
        for artist in artists:
            self.artist_combo.addItem(artist['name'], artist['id'])
        
        if not artists:
            QMessageBox.warning(
                self,
                "No Artists",
                "No artists found in the database. Please add an artist first."
            )
    
    def load_artwork(self, artwork_id: int):
        """Load artwork data into the form.
        
        Args:
            artwork_id: Artwork ID to load
        """
        artwork = self.artwork_repo.get_by_id(artwork_id)
        if artwork:
            self.title_input.setText(artwork['title'])
            
            # Set artist combo
            index = self.artist_combo.findData(artwork['artist_id'])
            if index >= 0:
                self.artist_combo.setCurrentIndex(index)
            
            if artwork.get('year'):
                self.year_input.setValue(artwork['year'])
            if artwork.get('medium'):
                self.medium_input.setText(artwork['medium'])
            if artwork.get('dimensions'):
                self.dimensions_input.setText(artwork['dimensions'])
            if artwork.get('description'):
                self.description_input.setPlainText(artwork['description'])
            if artwork.get('image_path'):
                self.selected_image_path = artwork['image_path']
                self.image_path_label.setText(Path(artwork['image_path']).name)
                self.image_path_label.setStyleSheet("color: black;")
    
    def browse_image(self):
        """Open file dialog to select an image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        
        if file_path:
            self.selected_image_path = file_path
            self.image_path_label.setText(Path(file_path).name)
            self.image_path_label.setStyleSheet("color: black;")
    
    def save_artwork(self):
        """Save the artwork data."""
        title = self.title_input.text().strip()
        artist_id = self.artist_combo.currentData()
        
        # Validation
        if not title:
            QMessageBox.warning(self, "Validation Error", "Artwork title is required.")
            self.title_input.setFocus()
            return
        
        if artist_id is None:
            QMessageBox.warning(self, "Validation Error", "Please select an artist.")
            self.artist_combo.setFocus()
            return
        
        year = self.year_input.value() if self.year_input.value() > 0 else None
        medium = self.medium_input.text().strip() or None
        dimensions = self.dimensions_input.text().strip() or None
        description = self.description_input.toPlainText().strip() or None
        
        try:
            if self.artwork_id:
                # Update existing artwork
                self.artwork_repo.update(
                    self.artwork_id,
                    title=title,
                    artist_id=artist_id,
                    year=year,
                    medium=medium,
                    dimensions=dimensions,
                    description=description,
                    image_path=self.selected_image_path
                )
            else:
                # Create new artwork
                self.artwork_repo.create(
                    title=title,
                    artist_id=artist_id,
                    year=year,
                    medium=medium,
                    dimensions=dimensions,
                    description=description,
                    image_path=self.selected_image_path
                )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save artwork: {str(e)}")
