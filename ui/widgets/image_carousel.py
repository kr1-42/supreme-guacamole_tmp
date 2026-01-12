"""
Simple image carousel widget that wraps ImagePreviewWidget with previous/next controls.
"""
from pathlib import Path
import shutil
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from core.paths import IMG_DIR

from ui.widgets.image_preview import ImagePreviewWidget


class ImageCarousel(QWidget):
    """Carousel to flip through a list of image paths."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._images = []
        self._index = 0
        self._build_ui()
        self.setAcceptDrops(True)

    def _build_ui(self):
        layout = QVBoxLayout()

        self.preview = ImagePreviewWidget()

        controls = QHBoxLayout()
        self.prev_btn = QPushButton("<")
        self.next_btn = QPushButton(">")
        self.prev_btn.clicked.connect(self.prev)
        self.next_btn.clicked.connect(self.next)
        controls.addWidget(self.prev_btn)
        controls.addWidget(self.next_btn)

        layout.addWidget(self.preview)
        layout.addLayout(controls)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self._update_controls()

    def set_images(self, paths):
        self._images = [Path(p) for p in paths if p]
        self._index = 0
        self._show_current()
        self._update_controls()

    def clear(self):
        self._images = []
        self._index = 0
        self.preview.clear()
        self._update_controls()

    def next(self):
        if not self._images:
            return
        self._index = (self._index + 1) % len(self._images)
        self._show_current()

    def prev(self):
        if not self._images:
            return
        self._index = (self._index - 1) % len(self._images)
        self._show_current()

    def _show_current(self):
        if not self._images:
            self.preview.clear()
            return
        self.preview.load_image(self._images[self._index])

    def _update_controls(self):
        enabled = len(self._images) > 1
        self.prev_btn.setEnabled(enabled)
        self.next_btn.setEnabled(enabled)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and self._has_image_urls(event.mimeData().urls()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        image_paths = [u.toLocalFile() for u in urls if u.isLocalFile() and self._is_image_file(u.toLocalFile())]
        if not image_paths:
            event.ignore()
            return

        persisted = []
        for src_str in image_paths:
            src = Path(src_str)
            dest = IMG_DIR / src.name
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.resolve() != src.resolve():
                    shutil.copy2(src, dest)
                persisted.append(dest)
            except Exception:
                # Skip files that cannot be copied
                continue

        if persisted:
            self.set_images(persisted)
            event.acceptProposedAction()
        else:
            event.ignore()

    def _has_image_urls(self, urls):
        return any(u.isLocalFile() and self._is_image_file(u.toLocalFile()) for u in urls)

    def _is_image_file(self, path_str):
        return Path(path_str).suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".ppm"}
