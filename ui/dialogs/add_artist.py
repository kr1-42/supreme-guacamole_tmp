"""
Add Artist Dialog
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QDialogButtonBox
)


class AddArtistDialog(QDialog):
    """
    Dialog for adding or editing an artist
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Artist")
        self.setMinimumWidth(400)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # Form fields
        self.name_input = QLineEdit()
        self.bio_input = QTextEdit()
        self.bio_input.setMaximumHeight(100)
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)

        form.addRow("Name:", self.name_input)
        form.addRow("Bio:", self.bio_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Phone:", self.phone_input)
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

    def get_data(self):
        """Get form data"""
        return {
            'name': self.name_input.text(),
            'bio': self.bio_input.toPlainText(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'notes': self.notes_input.toPlainText()
        }

    def set_data(self, data):
        """Set form data (for editing)"""
        self.name_input.setText(data.get('name', ''))
        self.bio_input.setPlainText(data.get('bio', ''))
        self.email_input.setText(data.get('email', ''))
        self.phone_input.setText(data.get('phone', ''))
        self.notes_input.setPlainText(data.get('notes', ''))
