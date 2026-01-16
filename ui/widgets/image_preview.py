"""
Image Preview Widget
Custom widget for displaying artwork images
"""

from pathlib import Path
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

try:
    from PIL import Image, ImageOps
except ImportError:
    Image = None
    ImageOps = None


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
        self.image_label.setMinimumWidth(300)
        self.image_label.setMinimumHeight(300)
        self.image_label.setMaximumWidth(400)
        self.image_label.setMaximumHeight(400)
        self.image_label.setStyleSheet(
            "border: 1px solid #555;"
            "background-color: #1e1e1e;"
            "color: #ddd;"
        )
        self.image_label.setScaledContents(False)
        # Ignore the pixmap's size hint so the label stays bounded by layout
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

        # Load and fix EXIF orientation using PIL
        pixmap = self._load_pixmap_with_exif_fix(str(path))
        if pixmap is None or pixmap.isNull():
            self.image_label.setText("Invalid image")
            return

        self._pixmap = pixmap
        self._update_pixmap()

    def _load_pixmap_with_exif_fix(self, image_path):
        """Load image and apply EXIF orientation using PIL"""
        if Image is None:
            # Fallback if PIL is not available
            return QPixmap(image_path)

        try:
            with Image.open(image_path) as img:
                # Apply EXIF orientation automatically
                if ImageOps is not None:
                    img = ImageOps.exif_transpose(img)
                
                # Convert PIL image to QPixmap
                import io
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue())
                return pixmap
        except Exception as e:
            print(f"Error loading image with EXIF fix: {e}")
            # Fallback to loading without EXIF fix
            return QPixmap(image_path)

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
        
        # Use the label's actual size (which should be square now)
        label_size = self.image_label.size()
        size = min(label_size.width(), label_size.height())
        
        if size <= 0:
            size = 300
        
        # Scale the pixmap to fit in a square while maintaining aspect ratio
        scaled_pixmap = self._pixmap.scaled(
            size,
            size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
