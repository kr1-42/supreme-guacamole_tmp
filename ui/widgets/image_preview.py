"""
Image Preview Widget
Custom widget for displaying artwork images
"""

from pathlib import Path
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class ImagePreviewWidget(QWidget):
    """
    Widget for displaying artwork images with automatic scaling
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Image label
        self.image_label = QLabel("No image")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(0)
        self.image_label.setStyleSheet(
            "border: 1px solid #555;"
            "background-color: #1e1e1e;"
            "color: #ddd;"
        )
        self.image_label.setScaledContents(False)
        # Ignore the pixmap's size hint so the label stays bounded by layout
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        layout.addWidget(self.image_label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def load_image(self, image_path):
        """Load and display an image"""
        if not image_path:
            self.clear()
            return

        path = Path(image_path)
        if not path.exists():
            self.image_label.setText("Image not found")
            return

        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            self.image_label.setText("Invalid image")
            return

        self._pixmap = pixmap
        self._update_pixmap()

    def clear(self):
        """Clear the image"""
        self.image_label.clear()
        self.image_label.setText("No image")
        self._pixmap = None

    def resizeEvent(self, event):
        """Handle resize events to rescale the image"""
        super().resizeEvent(event)
        self._update_pixmap()

    def _update_pixmap(self):
        if not self._pixmap:
            return
        scaled_pixmap = self._pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
