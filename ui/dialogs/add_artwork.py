"""
Add Artwork Dialog
"""

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QDialogButtonBox,
    QFileDialog,
)


class AddArtworkDialog(QDialog):
    """
    Dialog for adding or editing an artwork
    """

    def __init__(self, artists=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Artwork")
        self.setMinimumWidth(500)
        self.artists = artists or []

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # Form fields
        self.artist_combo = QComboBox()
        for artist in self.artists:
            self.artist_combo.addItem(artist['name'], artist['id'])

        self.title_input = QLineEdit()
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)

        self.type_input = QLineEdit()

        self.year_input = QSpinBox()
        self.year_input.setRange(1000, 2100)
        self.year_input.setValue(2024)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 1000000)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("€ ")

        self.artist_cut_input = QDoubleSpinBox()
        self.artist_cut_input.setRange(0, 100)
        self.artist_cut_input.setDecimals(2)
        self.artist_cut_input.setSuffix(" %")
        self.artist_cut_input.setValue(10.0)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["available", "sold", "exhibition", "reserved"])

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)

        # Image selection
        image_layout = QVBoxLayout()
        self.image_input = QLineEdit()
        self.image_input.setPlaceholderText("No image selected")
        image_btn = QPushButton("Browse...")
        image_btn.clicked.connect(self._browse_image)
        image_layout.addWidget(self.image_input)
        image_layout.addWidget(image_btn)

        form.addRow("Artist:", self.artist_combo)
        form.addRow("Title:", self.title_input)
        form.addRow("Description:", self.description_input)
        form.addRow("Type:", self.type_input)
        form.addRow("Year:", self.year_input)
        form.addRow("Price:", self.price_input)
        form.addRow("Artist cut %:", self.artist_cut_input)
        form.addRow("Status:", self.status_combo)
        form.addRow("Image:", image_layout)
        form.addRow("Notes:", self.notes_input)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _browse_image(self):
        """Open file dialog to select image"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Artwork Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if filename:
            self.image_input.setText(filename)

    def get_data(self):
        """Get form data"""
        return {
            'artist_id': self.artist_combo.currentData(),
            'title': self.title_input.text(),
            'description': self.description_input.toPlainText(),
            'type': self.type_input.text(),
            'year': self.year_input.value(),
            'price': self.price_input.value(),
            'artist_cut_percent': self.artist_cut_input.value(),
            'status': self.status_combo.currentText(),
            'image': self.image_input.text(),
            'notes': self.notes_input.toPlainText()
        }

    def set_data(self, data):
        """Set form data (for editing)"""
        # Set artist
        artist_id = data.get('artist_id')
        for i in range(self.artist_combo.count()):
            if self.artist_combo.itemData(i) == artist_id:
                self.artist_combo.setCurrentIndex(i)
                break

        self.title_input.setText(data.get('title', ''))
        self.description_input.setPlainText(data.get('description', ''))
        self.type_input.setText(data.get('type', ''))

        year = data.get('year')
        if year:
            self.year_input.setValue(year)

        price = data.get('price')
        if price:
            self.price_input.setValue(price)

        artist_cut = data.get('artist_cut_percent')
        if artist_cut is not None:
            self.artist_cut_input.setValue(float(artist_cut))

        status = data.get('status', 'available')
        idx = self.status_combo.findText(status)
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)

        self.image_input.setText(data.get('image', ''))
        self.notes_input.setPlainText(data.get('notes', ''))
