"""
Artwork Table Widget
Custom widget for displaying and managing artworks
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QLabel,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from core.paths import IMG_DIR


class ArtworkCard(QPushButton):
    """Custom button that tracks double clicks"""
    double_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
    
    def mouseDoubleClickEvent(self, event):
        """Handle double click"""
        self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)


class ArtworkTableWidget(QWidget):
    """
    Widget displaying artworks in a card/grid format
    """

    artwork_selected = pyqtSignal(int)  # Emits artwork ID when selected
    artwork_double_clicked = pyqtSignal(int)  # Emits artwork ID on double click

    def __init__(self, parent=None):
        super().__init__(parent)
        self._artwork_cards = {}  # Store {artwork_id: button_widget}
        self._selected_id = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Scroll area for cards
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; }")

        # Container for all content
        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Available section header
        self.available_label = QLabel("Disponibili")
        self.available_label.setStyleSheet("font-weight: bold; font-size: 14pt; color: #4CAF50; padding: 5px;")
        self.main_layout.addWidget(self.available_label)
        
        # Available artworks grid
        self.available_grid = QGridLayout()
        self.available_grid.setSpacing(10)
        self.main_layout.addLayout(self.available_grid)
        
        # Sold section header
        self.sold_label = QLabel("Venduti")
        self.sold_label.setStyleSheet("font-weight: bold; font-size: 14pt; color: #FF6B6B; padding: 5px; margin-top: 20px;")
        self.main_layout.addWidget(self.sold_label)
        
        # Sold artworks grid
        self.sold_grid = QGridLayout()
        self.sold_grid.setSpacing(10)
        self.main_layout.addLayout(self.sold_grid)
        
        self.main_layout.addStretch()
        self.container.setLayout(self.main_layout)

        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _create_artwork_card(self, artwork):
        """Create a card widget for an artwork"""
        card = ArtworkCard()
        card.setStyleSheet(
            "ArtworkCard { text-align: top; padding: 0px; border: 1px solid #555; background-color: #2a2a2a; }"
            "ArtworkCard:hover { background-color: #3a3a3a; }"
            "ArtworkCard:pressed { background-color: #1a1a1a; }"
        )
        card.setMinimumHeight(340)
        card.setMinimumWidth(240)
        
        # Create card content
        card_layout = QVBoxLayout()
        card_layout.setSpacing(5)
        card_layout.setContentsMargins(8, 8, 8, 8)

        # Image - bigger size
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setMinimumHeight(200)
        image_name = artwork.get('image', '')
        if image_name:
            image_path = IMG_DIR / image_name
            if image_path.exists():
                pixmap = QPixmap(str(image_path))
                if not pixmap.isNull():
                    scaled = pixmap.scaled(260, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(scaled)
                else:
                    image_label.setText("Invalid")
            else:
                image_label.setText("Not found")
        else:
            image_label.setText("No image")
        card_layout.addWidget(image_label)

        # Title
        title_label = QLabel(artwork.get('title', ''))
        title_label.setStyleSheet("font-weight: bold; color: #ddd; font-size: 11pt;")
        title_label.setWordWrap(True)
        card_layout.addWidget(title_label)

        # Artist and status - translate status to Italian
        status_map = {
            'available': 'Disponibile',
            'sold': 'Venduto',
            'exhibition': 'In Mostra',
            'reserved': 'Riservato'
        }
        status = artwork.get('status', 'available')
        status_it = status_map.get(status, status)
        info_text = f"{artwork.get('artist_name', 'Unknown')} | {status_it}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: #aaa; font-size: 11pt; font-weight: bold;")
        card_layout.addWidget(info_label)

        # Price
        price = artwork.get('price')
        price_text = f"€ {price:.2f}" if price is not None else "—"
        price_label = QLabel(price_text)
        price_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 12pt;")
        card_layout.addWidget(price_label)

        # Quantity
        quantity = artwork.get('quantity', 1)
        qty_text = f"Quantità: {quantity}"
        qty_label = QLabel(qty_text)
        qty_label.setStyleSheet("color: #64B5F6; font-size: 10pt;")
        card_layout.addWidget(qty_label)

        card_layout.addStretch()
        card.setLayout(card_layout)
        return card

    def _on_card_clicked(self, artwork_id):
        """Handle card click"""
        self._selected_id = artwork_id
        self.artwork_selected.emit(artwork_id)
        # Visual feedback
        for aid, card in self._artwork_cards.items():
            if aid == artwork_id:
                card.setStyleSheet(
                    "ArtworkCard { text-align: top; padding: 0px; border: 2px solid #FF6B6B; background-color: #3a3a3a; }"
                )
            else:
                card.setStyleSheet(
                    "ArtworkCard { text-align: top; padding: 0px; border: 1px solid #555; background-color: #2a2a2a; }"
                )

    def _on_card_double_clicked(self, artwork_id):
        """Handle card double click"""
        self.artwork_double_clicked.emit(artwork_id)

    def _clear_layout(self):
        """Safely clear all items from the grid layouts"""
        # Clear available grid
        while self.available_grid.count():
            item = self.available_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # Clear sold grid
        while self.sold_grid.count():
            item = self.sold_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def load_artworks(self, artworks):
        """Load artworks into the card view"""
        # Clear existing cards safely
        self._clear_layout()
        self._artwork_cards.clear()
        self._selected_id = None

        # Separate artworks by status
        available_artworks = [a for a in artworks if a.get('status') != 'sold']
        sold_artworks = [a for a in artworks if a.get('status') == 'sold']

        columns = 2  # 2 cards per row

        # Load available artworks
        row = 0
        col = 0
        for artwork in available_artworks:
            artwork_id = artwork.get('id')
            card = self._create_artwork_card(artwork)
            
            # Create handlers
            def make_click_handler(aid):
                def handler():
                    self._on_card_clicked(aid)
                return handler
            
            def make_double_click_handler(aid):
                def handler():
                    self._on_card_double_clicked(aid)
                return handler
            
            card.clicked.connect(make_click_handler(artwork_id))
            card.double_clicked.connect(make_double_click_handler(artwork_id))
            
            self._artwork_cards[artwork_id] = card
            self.available_grid.addWidget(card, row, col)
            
            col += 1
            if col >= columns:
                col = 0
                row += 1

        # Load sold artworks
        row = 0
        col = 0
        for artwork in sold_artworks:
            artwork_id = artwork.get('id')
            card = self._create_artwork_card(artwork)
            
            # Create handlers
            def make_click_handler(aid):
                def handler():
                    self._on_card_clicked(aid)
                return handler
            
            def make_double_click_handler(aid):
                def handler():
                    self._on_card_double_clicked(aid)
                return handler
            
            card.clicked.connect(make_click_handler(artwork_id))
            card.double_clicked.connect(make_double_click_handler(artwork_id))
            
            self._artwork_cards[artwork_id] = card
            self.sold_grid.addWidget(card, row, col)
            
            col += 1
            if col >= columns:
                col = 0
                row += 1

        # Update section visibility
        self.available_label.setVisible(len(available_artworks) > 0)
        self.sold_label.setVisible(len(sold_artworks) > 0)

    def clear(self):
        """Clear the cards"""
        self._clear_layout()
        self._artwork_cards.clear()
        self._selected_id = None

    def get_selected_artwork_id(self):
        """Get currently selected artwork ID"""
        return self._selected_id
