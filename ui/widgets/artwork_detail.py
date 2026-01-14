"""
Artwork Detail Widget
Shows expanded metadata for a selected artwork.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QFrame
from PyQt5.QtCore import Qt


class ArtworkDetailWidget(QWidget):
    """Display key fields of an artwork in a stacked form."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("—")
        self.artist_label = QLabel("—")
        self.type_label = QLabel("—")
        self.year_label = QLabel("—")
        self.price_label = QLabel("—")
        self.cut_label = QLabel("—")
        self.qty_label = QLabel("—")
        self.status_label = QLabel("—")

        self.description_label = QLabel("—")
        self.description_label.setWordWrap(True)
        self.notes_label = QLabel("—")
        self.notes_label.setWordWrap(True)

        form = QFormLayout()
        form.addRow("Title:", self.title_label)
        form.addRow("Artist:", self.artist_label)
        form.addRow("Type:", self.type_label)
        form.addRow("Year:", self.year_label)
        form.addRow("Price:", self.price_label)
        form.addRow("Artist %:", self.cut_label)
        form.addRow("Quantity:", self.qty_label)
        form.addRow("Status:", self.status_label)

        layout.addLayout(form)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)

        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_label)
        layout.addWidget(QLabel("Notes:"))
        layout.addWidget(self.notes_label)

        layout.addStretch()
        self.setLayout(layout)

    def show_artwork(self, artwork: dict):
        self.title_label.setText(artwork.get("title", "—") or "—")
        self.artist_label.setText(artwork.get("artist_name", "—") or "—")
        self.type_label.setText(artwork.get("type", "—") or "—")
        year = artwork.get("year")
        self.year_label.setText(str(year) if year else "—")
        price = artwork.get("price")
        self.price_label.setText(f"€ {price:.2f}" if price is not None else "—")
        cut = artwork.get("artist_cut_percent")
        self.cut_label.setText(f"{cut:.2f}%" if cut is not None else "—")
        qty = artwork.get("quantity")
        self.qty_label.setText(str(qty) if qty is not None else "—")
        self.status_label.setText(artwork.get("status", "—") or "—")
        self.description_label.setText(artwork.get("description", "—") or "—")
        self.notes_label.setText(artwork.get("notes", "—") or "—")

    def clear(self):
        self.show_artwork({})
