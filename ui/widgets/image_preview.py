"""Image preview widget for displaying artwork images."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from pathlib import Path


class ImagePreviewWidget(QWidget):
    """Widget for previewing artwork images."""
    
    def __init__(self, parent=None):
        """Initialize image preview widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(300, 300)
        self.image_label.setStyleSheet("QLabel { background-color: #f0f0f0; border: 1px solid #ccc; }")
        self.image_label.setText("No image")
        
        layout.addWidget(self.image_label)
        
        # Info label
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
    
    def set_image(self, image_path: str = None):
        """Set the image to display.
        
        Args:
            image_path: Path to the image file. If None, displays placeholder.
        """
        if image_path and Path(image_path).exists():
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale the image to fit the label while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.info_label.setText(f"Image: {Path(image_path).name}")
            else:
                self.clear_image()
                self.info_label.setText("Error loading image")
        else:
            self.clear_image()
            if image_path:
                self.info_label.setText("Image file not found")
            else:
                self.info_label.setText("")
    
    def clear_image(self):
        """Clear the displayed image."""
        self.image_label.clear()
        self.image_label.setText("No image")
        self.info_label.setText("")
    
    def resizeEvent(self, event):
        """Handle widget resize to rescale the image.
        
        Args:
            event: Resize event
        """
        super().resizeEvent(event)
        # Re-scale the image if one is currently displayed
        pixmap = self.image_label.pixmap()
        if pixmap and not pixmap.isNull():
            # This would require storing the original path, so we'll skip re-scaling for now
            pass
