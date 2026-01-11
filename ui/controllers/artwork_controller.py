from pathlib import Path
import shutil
from PySide6.QtWidgets import QMessageBox

from core.paths import IMG_DIR
PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_IMAGES_DIR = PROJECT_ROOT / "assets" / "test_images"
from ui.dialogs.add_artwork import AddArtworkDialog


class ArtworkController:
    """Handles artwork CRUD, preview, and drag/drop."""

    def __init__(self, artwork_repo, artist_repo, artwork_table, preview_widget):
        self.artwork_repo = artwork_repo
        self.artist_repo = artist_repo
        self.table = artwork_table
        self.preview = preview_widget

    def load_artworks(self, artist_id=None):
        rows = self.artwork_repo.get_by_artist(artist_id) if artist_id else self.artwork_repo.get_all()
        artworks = []
        for r in rows:
            data = dict(r)
            data["artist_name"] = r["artist_name"] if "artist_name" in r.keys() else ""
            artworks.append(data)
        self.table.load_artworks(artworks)
        self.preview.clear()

    def on_artwork_selected(self, artwork_id: int):
        record = self.artwork_repo.get_by_id(artwork_id)
        if not record:
            self.preview.clear()
            return
        image_name = record["image"] if "image" in record.keys() else ""
        images = []
        if image_name:
            images.append(IMG_DIR / image_name)
        if not images:
            images = sorted(TEST_IMAGES_DIR.glob("test_image_*.ppm"))
        self.preview.set_images(images)

    def add_artwork(self):
        artists = [dict(r) for r in self.artist_repo.get_all()]
        dialog = AddArtworkDialog(artists=artists, parent=self.table)
        if dialog.exec():
            data = dialog.get_data()
            image_name = self._persist_image(data.get("image"))
            self.artwork_repo.create(
                artist_id=data.get("artist_id"),
                title=data.get("title"),
                description=data.get("description", ""),
                type=data.get("type", ""),
                year=data.get("year"),
                price=data.get("price"),
                artist_cut_percent=data.get("artist_cut_percent", 10.0),
                image=image_name or "",
                status=data.get("status", "available"),
                notes=data.get("notes", "")
            )
            self.load_artworks()

    def edit_artwork(self):
        artwork_id = self.table.get_selected_artwork_id()
        if not artwork_id:
            QMessageBox.information(self.table, "Edit Artwork", "Select an artwork first.")
            return

        record = self.artwork_repo.get_by_id(artwork_id)
        if not record:
            QMessageBox.warning(self.table, "Edit Artwork", "Artwork not found.")
            return

        data = dict(record)
        artists = [dict(r) for r in self.artist_repo.get_all()]
        dialog = AddArtworkDialog(artists=artists, parent=self.table)
        dialog.setWindowTitle("Edit Artwork")
        dialog.set_data(data)

        if dialog.exec():
            new_data = dialog.get_data()
            image_name = self._persist_image(new_data.get("image")) if new_data.get("image") else data.get("image", "")
            self.artwork_repo.update(
                artwork_id=artwork_id,
                artist_id=new_data.get("artist_id"),
                title=new_data.get("title"),
                description=new_data.get("description", ""),
                type=new_data.get("type", ""),
                year=new_data.get("year"),
                price=new_data.get("price"),
                artist_cut_percent=new_data.get("artist_cut_percent", data.get("artist_cut_percent", 10.0)),
                image=image_name or "",
                status=new_data.get("status", "available"),
                notes=new_data.get("notes", "")
            )
            self.load_artworks()

    def delete_artwork(self):
        artwork_id = self.table.get_selected_artwork_id()
        if not artwork_id:
            QMessageBox.information(self.table, "Delete Artwork", "Select an artwork first.")
            return

        confirm = QMessageBox.question(
            self.table,
            "Delete Artwork",
            "Are you sure you want to delete this artwork?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.artwork_repo.delete(artwork_id)
            self.load_artworks()
            self.preview.clear()

    # ---------- Drag & drop helpers ----------
    def handle_drop(self, urls):
        image_paths = [u.toLocalFile() for u in urls if u.isLocalFile() and self._is_image_file(u.toLocalFile())]
        if not image_paths:
            return False
        image_name = self._persist_image(image_paths[0])
        if not image_name:
            return False
        self._prompt_add_artwork_with_image(image_name)
        return True

    def _prompt_add_artwork_with_image(self, image_name: str):
        artists = [dict(r) for r in self.artist_repo.get_all()]
        dialog = AddArtworkDialog(artists=artists, parent=self.table)
        dialog.setWindowTitle("Add Artwork")
        dialog.set_data({'image': str(IMG_DIR / image_name)})
        if dialog.exec():
            data = dialog.get_data()
            final_image_name = self._persist_image(data.get("image")) if data.get("image") else image_name
            self.artwork_repo.create(
                artist_id=data.get("artist_id"),
                title=data.get("title"),
                description=data.get("description", ""),
                type=data.get("type", ""),
                year=data.get("year"),
                price=data.get("price"),
                artist_cut_percent=data.get("artist_cut_percent", 10.0),
                image=final_image_name or "",
                status=data.get("status", "available"),
                notes=data.get("notes", "")
            )
            self.load_artworks()

    def _persist_image(self, source_path: str):
        if not source_path:
            return ""
        src = Path(source_path)
        if not src.exists():
            return ""
        dest = IMG_DIR / src.name
        try:
            if dest.resolve() != src.resolve():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            return dest.name
        except Exception:
            return ""

    def _is_image_file(self, path_str: str):
        return Path(path_str).suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".ppm"}
