"""
Add Exhibition Dialog
"""

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QPushButton,
    QDialogButtonBox,
)
from PyQt5.QtCore import QDate


class AddExhibitionDialog(QDialog):
    """
    Dialog for adding or editing an exhibition
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Exhibition")
        self.setMinimumWidth(450)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # Form fields
        self.name_input = QLineEdit()
        self.location_input = QLineEdit()

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate().addDays(30))

        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(150)

        form.addRow("Name:", self.name_input)
        form.addRow("Location:", self.location_input)
        form.addRow("Start Date:", self.start_date_input)
        form.addRow("End Date:", self.end_date_input)
        form.addRow("Description:", self.description_input)

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
            'location': self.location_input.text(),
            'start_date': self.start_date_input.date().toString("yyyy-MM-dd"),
            'end_date': self.end_date_input.date().toString("yyyy-MM-dd"),
            'description': self.description_input.toPlainText()
        }

    def set_data(self, data):
        """Set form data (for editing)"""
        self.name_input.setText(data.get('name', ''))
        self.location_input.setText(data.get('location', ''))

        start_date = data.get('start_date')
        if start_date:
            self.start_date_input.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))

        end_date = data.get('end_date')
        if end_date:
            self.end_date_input.setDate(QDate.fromString(end_date, "yyyy-MM-dd"))

        self.description_input.setPlainText(data.get('description', ''))
