"""
Image Preview Widget
Custom widget for displaying artwork images
"""

from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class ImagePreviewWidget(QWidget):
    """
    Widget for displaying artwork images with automatic scaling
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Image label
        self.image_label = QLabel("No image")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet(
            "border: 1px solid #999; background-color: #f5f5f5;"
        )
        self.image_label.setScaledContents(False)

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

        # Scale pixmap to fit label while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

    def clear(self):
        """Clear the image"""
        self.image_label.clear()
        self.image_label.setText("No image")

    def resizeEvent(self, event):
        """Handle resize events to rescale the image"""
        super().resizeEvent(event)
        if self.image_label.pixmap() and not self.image_label.pixmap().isNull():
            # Get the original pixmap and rescale it
            pixmap = self.image_label.pixmap()
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
