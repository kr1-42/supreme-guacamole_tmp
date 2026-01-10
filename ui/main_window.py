"""Main window for the art gallery management application."""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QTabWidget, QPushButton, QMessageBox, QSplitter,
                              QLabel, QGroupBox)
from PyQt6.QtCore import Qt
from core.database import Database
from core.repositories import ArtistRepository, ArtworkRepository, ExhibitionRepository
from ui.widgets.artist_list import ArtistListWidget
from ui.widgets.artwork_table import ArtworkTableWidget
from ui.widgets.image_preview import ImagePreviewWidget
from ui.dialogs.add_artist import AddArtistDialog
from ui.dialogs.add_artwork import AddArtworkDialog
from ui.dialogs.add_exhibition import AddExhibitionDialog


class MainWindow(QMainWindow):
    """Main application window for the art gallery management system."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.db = Database.get_instance()
        self.artist_repo = ArtistRepository()
        self.artwork_repo = ArtworkRepository()
        self.exhibition_repo = ExhibitionRepository()
        
        self.init_database()
        self.init_ui()
    
    def init_database(self):
        """Initialize the database schema."""
        try:
            self.db.initialize_schema()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Failed to initialize database: {str(e)}"
            )
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Art Gallery Management System")
        self.setMinimumSize(1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_artists_tab()
        self.create_artworks_tab()
        self.create_exhibitions_tab()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_artists_tab(self):
        """Create the artists management tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Title
        title_label = QLabel("Artists Management")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # Splitter for list and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Artist list
        list_group = QGroupBox("Artists")
        list_layout = QVBoxLayout(list_group)
        self.artist_list = ArtistListWidget()
        self.artist_list.artist_selected.connect(self.on_artist_selected)
        list_layout.addWidget(self.artist_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_artist_btn = QPushButton("Add Artist")
        add_artist_btn.clicked.connect(self.add_artist)
        button_layout.addWidget(add_artist_btn)
        
        edit_artist_btn = QPushButton("Edit Artist")
        edit_artist_btn.clicked.connect(self.edit_artist)
        button_layout.addWidget(edit_artist_btn)
        
        delete_artist_btn = QPushButton("Delete Artist")
        delete_artist_btn.clicked.connect(self.delete_artist)
        button_layout.addWidget(delete_artist_btn)
        
        list_layout.addLayout(button_layout)
        splitter.addWidget(list_group)
        
        # Artist details
        details_group = QGroupBox("Artist Details")
        details_layout = QVBoxLayout(details_group)
        self.artist_details_label = QLabel("Select an artist to view details")
        self.artist_details_label.setWordWrap(True)
        self.artist_details_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        details_layout.addWidget(self.artist_details_label)
        splitter.addWidget(details_group)
        
        splitter.setSizes([400, 400])
        layout.addWidget(splitter)
        
        self.tab_widget.addTab(tab, "Artists")
    
    def create_artworks_tab(self):
        """Create the artworks management tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Title
        title_label = QLabel("Artworks Management")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # Splitter for table and preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Artwork table
        table_group = QGroupBox("Artworks")
        table_layout = QVBoxLayout(table_group)
        self.artwork_table = ArtworkTableWidget()
        self.artwork_table.artwork_selected.connect(self.on_artwork_selected)
        table_layout.addWidget(self.artwork_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_artwork_btn = QPushButton("Add Artwork")
        add_artwork_btn.clicked.connect(self.add_artwork)
        button_layout.addWidget(add_artwork_btn)
        
        edit_artwork_btn = QPushButton("Edit Artwork")
        edit_artwork_btn.clicked.connect(self.edit_artwork)
        button_layout.addWidget(edit_artwork_btn)
        
        delete_artwork_btn = QPushButton("Delete Artwork")
        delete_artwork_btn.clicked.connect(self.delete_artwork)
        button_layout.addWidget(delete_artwork_btn)
        
        table_layout.addLayout(button_layout)
        splitter.addWidget(table_group)
        
        # Image preview and details
        preview_group = QGroupBox("Artwork Preview")
        preview_layout = QVBoxLayout(preview_group)
        self.image_preview = ImagePreviewWidget()
        preview_layout.addWidget(self.image_preview)
        self.artwork_details_label = QLabel("Select an artwork to view details")
        self.artwork_details_label.setWordWrap(True)
        preview_layout.addWidget(self.artwork_details_label)
        splitter.addWidget(preview_group)
        
        splitter.setSizes([600, 400])
        layout.addWidget(splitter)
        
        self.tab_widget.addTab(tab, "Artworks")
    
    def create_exhibitions_tab(self):
        """Create the exhibitions management tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Title
        title_label = QLabel("Exhibitions Management")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # Placeholder for exhibitions list (simplified)
        info_label = QLabel(
            "Manage exhibitions here.\n\n"
            "Use the buttons below to add, edit, or delete exhibitions."
        )
        info_label.setStyleSheet("margin: 20px; font-size: 14px;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_exhibition_btn = QPushButton("Add Exhibition")
        add_exhibition_btn.clicked.connect(self.add_exhibition)
        button_layout.addWidget(add_exhibition_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "Exhibitions")
    
    def on_artist_selected(self, artist_id: int):
        """Handle artist selection.
        
        Args:
            artist_id: Selected artist ID
        """
        artist = self.artist_repo.get_by_id(artist_id)
        if artist:
            details = f"<b>Name:</b> {artist['name']}<br>"
            if artist.get('birth_year'):
                details += f"<b>Birth Year:</b> {artist['birth_year']}<br>"
            if artist.get('nationality'):
                details += f"<b>Nationality:</b> {artist['nationality']}<br>"
            if artist.get('biography'):
                details += f"<br><b>Biography:</b><br>{artist['biography']}"
            
            self.artist_details_label.setText(details)
    
    def on_artwork_selected(self, artwork_id: int):
        """Handle artwork selection.
        
        Args:
            artwork_id: Selected artwork ID
        """
        artwork = self.artwork_repo.get_with_artist(artwork_id)
        if artwork:
            details = f"<b>Title:</b> {artwork['title']}<br>"
            details += f"<b>Artist:</b> {artwork.get('artist_name', 'Unknown')}<br>"
            if artwork.get('year'):
                details += f"<b>Year:</b> {artwork['year']}<br>"
            if artwork.get('medium'):
                details += f"<b>Medium:</b> {artwork['medium']}<br>"
            if artwork.get('dimensions'):
                details += f"<b>Dimensions:</b> {artwork['dimensions']}<br>"
            if artwork.get('description'):
                details += f"<br>{artwork['description']}"
            
            self.artwork_details_label.setText(details)
            
            # Update image preview
            if artwork.get('image_path'):
                self.image_preview.set_image(artwork['image_path'])
            else:
                self.image_preview.clear_image()
    
    def add_artist(self):
        """Open dialog to add a new artist."""
        dialog = AddArtistDialog(self)
        if dialog.exec():
            self.artist_list.load_artists()
            self.statusBar().showMessage("Artist added successfully", 3000)
    
    def edit_artist(self):
        """Open dialog to edit the selected artist."""
        artist_id = self.artist_list.get_selected_artist_id()
        if artist_id:
            dialog = AddArtistDialog(self, artist_id)
            if dialog.exec():
                self.artist_list.load_artists()
                self.on_artist_selected(artist_id)
                self.statusBar().showMessage("Artist updated successfully", 3000)
        else:
            QMessageBox.warning(self, "No Selection", "Please select an artist to edit.")
    
    def delete_artist(self):
        """Delete the selected artist."""
        artist_id = self.artist_list.get_selected_artist_id()
        if artist_id:
            artist = self.artist_repo.get_by_id(artist_id)
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete artist '{artist['name']}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    self.artist_repo.delete(artist_id)
                    self.artist_list.load_artists()
                    self.artist_details_label.setText("Select an artist to view details")
                    self.statusBar().showMessage("Artist deleted successfully", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete artist: {str(e)}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select an artist to delete.")
    
    def add_artwork(self):
        """Open dialog to add a new artwork."""
        dialog = AddArtworkDialog(self)
        if dialog.exec():
            self.artwork_table.load_artworks()
            self.statusBar().showMessage("Artwork added successfully", 3000)
    
    def edit_artwork(self):
        """Open dialog to edit the selected artwork."""
        artwork_id = self.artwork_table.get_selected_artwork_id()
        if artwork_id:
            dialog = AddArtworkDialog(self, artwork_id)
            if dialog.exec():
                self.artwork_table.load_artworks()
                self.on_artwork_selected(artwork_id)
                self.statusBar().showMessage("Artwork updated successfully", 3000)
        else:
            QMessageBox.warning(self, "No Selection", "Please select an artwork to edit.")
    
    def delete_artwork(self):
        """Delete the selected artwork."""
        artwork_id = self.artwork_table.get_selected_artwork_id()
        if artwork_id:
            artwork = self.artwork_repo.get_by_id(artwork_id)
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete artwork '{artwork['title']}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    self.artwork_repo.delete(artwork_id)
                    self.artwork_table.load_artworks()
                    self.artwork_details_label.setText("Select an artwork to view details")
                    self.image_preview.clear_image()
                    self.statusBar().showMessage("Artwork deleted successfully", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete artwork: {str(e)}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select an artwork to delete.")
    
    def add_exhibition(self):
        """Open dialog to add a new exhibition."""
        dialog = AddExhibitionDialog(self)
        if dialog.exec():
            self.statusBar().showMessage("Exhibition added successfully", 3000)
