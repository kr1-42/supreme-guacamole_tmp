"""Dialog for adding a new exhibition."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QTextEdit, QPushButton, QFormLayout,
                              QMessageBox, QDateEdit, QListWidget, QListWidgetItem,
                              QAbstractItemView)
from PyQt6.QtCore import QDate, Qt
from core.repositories import ExhibitionRepository, ArtworkRepository


class AddExhibitionDialog(QDialog):
    """Dialog for adding or editing an exhibition."""
    
    def __init__(self, parent=None, exhibition_id: int = None):
        """Initialize add exhibition dialog.
        
        Args:
            parent: Parent widget
            exhibition_id: If provided, edit this exhibition instead of creating new
        """
        super().__init__(parent)
        self.exhibition_repo = ExhibitionRepository()
        self.artwork_repo = ArtworkRepository()
        self.exhibition_id = exhibition_id
        self.init_ui()
        self.load_artworks()
        
        if exhibition_id:
            self.load_exhibition(exhibition_id)
            self.setWindowTitle("Edit Exhibition")
        else:
            self.setWindowTitle("Add Exhibition")
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter exhibition title")
        form_layout.addRow("Title:*", self.title_input)
        
        # Start date
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        form_layout.addRow("Start Date:*", self.start_date_input)
        
        # End date
        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate().addDays(30))
        form_layout.addRow("End Date:*", self.end_date_input)
        
        # Location
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter location")
        form_layout.addRow("Location:", self.location_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter description")
        self.description_input.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_input)
        
        layout.addLayout(form_layout)
        
        # Artworks section
        artworks_label = QLabel("Artworks in Exhibition:")
        artworks_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(artworks_label)
        
        # Available artworks
        available_label = QLabel("Available Artworks:")
        layout.addWidget(available_label)
        
        self.available_artworks_list = QListWidget()
        self.available_artworks_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.available_artworks_list.setMaximumHeight(150)
        layout.addWidget(self.available_artworks_list)
        
        # Buttons to add/remove artworks
        artwork_button_layout = QHBoxLayout()
        self.add_artwork_button = QPushButton("Add Selected →")
        self.add_artwork_button.clicked.connect(self.add_selected_artworks)
        artwork_button_layout.addWidget(self.add_artwork_button)
        
        self.remove_artwork_button = QPushButton("← Remove Selected")
        self.remove_artwork_button.clicked.connect(self.remove_selected_artworks)
        artwork_button_layout.addWidget(self.remove_artwork_button)
        layout.addLayout(artwork_button_layout)
        
        # Selected artworks
        selected_label = QLabel("Selected Artworks:")
        layout.addWidget(selected_label)
        
        self.selected_artworks_list = QListWidget()
        self.selected_artworks_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.selected_artworks_list.setMaximumHeight(150)
        layout.addWidget(self.selected_artworks_list)
        
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
        self.save_button.clicked.connect(self.save_exhibition)
        self.save_button.setDefault(True)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def load_artworks(self):
        """Load available artworks into the list."""
        self.available_artworks_list.clear()
        artworks = self.artwork_repo.get_all_with_artists()
        
        for artwork in artworks:
            display_text = f"{artwork['title']} - {artwork.get('artist_name', 'Unknown')}"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, artwork['id'])
            self.available_artworks_list.addItem(item)
    
    def load_exhibition(self, exhibition_id: int):
        """Load exhibition data into the form.
        
        Args:
            exhibition_id: Exhibition ID to load
        """
        exhibition = self.exhibition_repo.get_by_id(exhibition_id)
        if exhibition:
            self.title_input.setText(exhibition['title'])
            
            # Parse and set dates
            start_date = QDate.fromString(exhibition['start_date'], "yyyy-MM-dd")
            if start_date.isValid():
                self.start_date_input.setDate(start_date)
            
            end_date = QDate.fromString(exhibition['end_date'], "yyyy-MM-dd")
            if end_date.isValid():
                self.end_date_input.setDate(end_date)
            
            if exhibition.get('location'):
                self.location_input.setText(exhibition['location'])
            if exhibition.get('description'):
                self.description_input.setPlainText(exhibition['description'])
            
            # Load exhibition artworks
            artworks = self.exhibition_repo.get_artworks(exhibition_id)
            for artwork in artworks:
                display_text = f"{artwork['title']} - {artwork.get('artist_name', 'Unknown')}"
                item = QListWidgetItem(display_text)
                item.setData(Qt.ItemDataRole.UserRole, artwork['id'])
                self.selected_artworks_list.addItem(item)
                
                # Remove from available list
                for i in range(self.available_artworks_list.count()):
                    available_item = self.available_artworks_list.item(i)
                    if available_item.data(Qt.ItemDataRole.UserRole) == artwork['id']:
                        self.available_artworks_list.takeItem(i)
                        break
    
    def add_selected_artworks(self):
        """Move selected artworks from available to selected list."""
        selected_items = self.available_artworks_list.selectedItems()
        for item in selected_items:
            row = self.available_artworks_list.row(item)
            taken_item = self.available_artworks_list.takeItem(row)
            self.selected_artworks_list.addItem(taken_item)
    
    def remove_selected_artworks(self):
        """Move selected artworks from selected to available list."""
        selected_items = self.selected_artworks_list.selectedItems()
        for item in selected_items:
            row = self.selected_artworks_list.row(item)
            taken_item = self.selected_artworks_list.takeItem(row)
            self.available_artworks_list.addItem(taken_item)
    
    def save_exhibition(self):
        """Save the exhibition data."""
        title = self.title_input.text().strip()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        
        # Validation
        if not title:
            QMessageBox.warning(self, "Validation Error", "Exhibition title is required.")
            self.title_input.setFocus()
            return
        
        if self.start_date_input.date() > self.end_date_input.date():
            QMessageBox.warning(self, "Validation Error", "Start date must be before end date.")
            self.start_date_input.setFocus()
            return
        
        location = self.location_input.text().strip() or None
        description = self.description_input.toPlainText().strip() or None
        
        try:
            if self.exhibition_id:
                # Update existing exhibition
                self.exhibition_repo.update(
                    self.exhibition_id,
                    title=title,
                    start_date=start_date,
                    end_date=end_date,
                    location=location,
                    description=description
                )
                
                # Clear existing artworks and re-add
                existing_artworks = self.exhibition_repo.get_artworks(self.exhibition_id)
                for artwork in existing_artworks:
                    self.exhibition_repo.remove_artwork(self.exhibition_id, artwork['id'])
                
                exhibition_id = self.exhibition_id
            else:
                # Create new exhibition
                exhibition_id = self.exhibition_repo.create(
                    title=title,
                    start_date=start_date,
                    end_date=end_date,
                    location=location,
                    description=description
                )
            
            # Add selected artworks
            for i in range(self.selected_artworks_list.count()):
                item = self.selected_artworks_list.item(i)
                artwork_id = item.data(Qt.ItemDataRole.UserRole)
                self.exhibition_repo.add_artwork(exhibition_id, artwork_id)
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save exhibition: {str(e)}")
