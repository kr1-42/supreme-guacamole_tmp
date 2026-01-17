"""
Sell Artwork Dialog
"""

from datetime import date
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QDialogButtonBox,
    QDateEdit,
)
from PyQt5.QtCore import QDate


class SellArtworkDialog(QDialog):
    """
    Dialog for selling an artwork
    """

    def __init__(self, artwork: dict, parent=None):
        super().__init__(parent)
        self.artwork = artwork
        self.setWindowTitle("Vendi Opera")
        self.setMinimumWidth(450)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Artwork info header
        info_label = QLabel(
            f"<b>{self.artwork.get('title', 'Senza titolo')}</b><br>"
            f"Artista: {self.artwork.get('artist_name', '—')}<br>"
            f"Prezzo listino: € {self.artwork.get('price', 0):.2f}"
        )
        info_label.setStyleSheet("padding: 10px; border-radius: 5px;")
        layout.addWidget(info_label)

        form = QFormLayout()

        # Sale date
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        # Sale price
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 1000000)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("€ ")
        self.price_input.setValue(self.artwork.get('price', 0) or 0)

        # Buyer name
        self.buyer_input = QLineEdit()
        self.buyer_input.setPlaceholderText("Nome acquirente")

        # Payment method
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Contanti", "Carta", "Bonifico", "PayPal", "Altro"])

        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Note sulla vendita...")

        form.addRow("Data vendita:", self.date_input)
        form.addRow("Prezzo vendita:", self.price_input)
        form.addRow("Acquirente:", self.buyer_input)
        form.addRow("Metodo pagamento:", self.payment_combo)
        form.addRow("Note:", self.notes_input)

        layout.addLayout(form)

        # Artist payment preview
        artist_cut = self.artwork.get('artist_cut_percent', 0) or 0
        price = self.price_input.value()
        artist_amount = price * (artist_cut / 100)
        
        self.payment_preview = QLabel()
        self._update_payment_preview()
        self.payment_preview.setStyleSheet("padding: 10px; border-radius: 5px;")
        layout.addWidget(self.payment_preview)
        
        # Update preview when price changes
        self.price_input.valueChanged.connect(self._update_payment_preview)

        # Buttons - Italian labels
        buttons = QDialogButtonBox()
        ok_btn = buttons.addButton("Conferma", QDialogButtonBox.AcceptRole)
        cancel_btn = buttons.addButton("Annulla", QDialogButtonBox.RejectRole)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _update_payment_preview(self):
        artist_cut = self.artwork.get('artist_cut_percent', 0) or 0
        price = self.price_input.value()
        artist_amount = price * (artist_cut / 100)
        company_amount = price - artist_amount
        
        self.payment_preview.setText(
            f"<b>Riepilogo:</b><br>"
            f"Totale: € {price:.2f}<br>"
            f"Quota artista ({artist_cut:.1f}%): € {artist_amount:.2f}<br>"
            f"Quota azienda: € {company_amount:.2f}"
        )

    def get_data(self) -> dict:
        return {
            "artwork_id": self.artwork.get('id'),
            "sale_date": self.date_input.date().toString("yyyy-MM-dd"),
            "sale_price": self.price_input.value(),
            "buyer_name": self.buyer_input.text().strip(),
            "payment_method": self.payment_combo.currentText(),
            "notes": self.notes_input.toPlainText().strip(),
        }
