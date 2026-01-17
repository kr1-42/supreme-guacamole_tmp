from pathlib import Path
import shutil
import uuid
from PyQt5.QtWidgets import QMessageBox

from core.paths import IMG_DIR
from ui.dialogs.add_artwork import AddArtworkDialog
from ui.dialogs.sell_artwork import SellArtworkDialog


class ArtworkController:
    """Handles artwork CRUD and drag/drop."""

    def __init__(self, artwork_repo, artist_repo, artwork_table, detail_widget=None, count_label=None, sale_repo=None):
        self.artwork_repo = artwork_repo
        self.artist_repo = artist_repo
        self.sale_repo = sale_repo
        self.table = artwork_table
        self.detail = detail_widget
        self.count_label = count_label

    def load_artworks(self, artist_id=None):
        rows = self.artwork_repo.get_by_artist(artist_id) if artist_id else self.artwork_repo.get_all()
        artworks = []
        for r in rows:
            data = dict(r)
            data["artist_name"] = r["artist_name"] if "artist_name" in r.keys() else ""
            artworks.append(data)
        self.table.load_artworks(artworks)
        if self.detail:
            self.detail.clear()
        if self.count_label:
            self.count_label.setText(f"Artworks: {len(artworks)}")

    def on_artwork_selected(self, artwork_id: int):
        record = self.artwork_repo.get_by_id(artwork_id)
        if not record:
            if self.detail:
                self.detail.clear()
            return
        if self.detail:
            self.detail.show_artwork(dict(record))

    def add_artwork(self):
        artists = [dict(r) for r in self.artist_repo.get_all()]
        dialog = AddArtworkDialog(artists=artists, parent=self.table)
        if dialog.exec():
            data = dialog.get_data()
            code = self._clean_code(data.get("code")) or self._generate_code()
            image_name = self._persist_image(data.get("image"))
            self.artwork_repo.create(
                artist_id=data.get("artist_id"),
                code=code,
                title=data.get("title"),
                description=data.get("description", ""),
                type=data.get("type", ""),
                quantity=data.get("quantity", 1),
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
            new_code = self._clean_code(new_data.get("code")) or data.get("code") or self._generate_code()
            
            # Handle image: check if it's a new image or the existing one
            new_image_path = new_data.get("image", "")
            original_image = data.get("image", "")
            
            if new_image_path:
                # Check if it's the same as the original (just filename)
                if new_image_path == original_image:
                    image_name = original_image
                else:
                    # Try to persist as a new image
                    persisted = self._persist_image(new_image_path)
                    image_name = persisted if persisted else original_image
            else:
                image_name = original_image
            
            old_status = data.get("status", "available")
            new_status = new_data.get("status", "available")
            old_quantity = data.get("quantity", 1)
            
            # If marking as sold and quantity > 1, create a sold copy and decrement original
            if new_status == "sold" and old_status != "sold" and old_quantity > 1:
                # Use the original image name directly for the sold copy
                original_image = data.get("image", "")
                
                # Create a sold copy with quantity 1
                self.artwork_repo.create(
                    artist_id=new_data.get("artist_id"),
                    code=self._generate_code(),  # Generate new code for sold item
                    title=new_data.get("title"),
                    description=new_data.get("description", ""),
                    type=new_data.get("type", ""),
                    quantity=1,
                    year=new_data.get("year"),
                    price=new_data.get("price"),
                    artist_cut_percent=new_data.get("artist_cut_percent", data.get("artist_cut_percent", 10.0)),
                    image=original_image,
                    status="sold",
                    notes=new_data.get("notes", "")
                )
                
                # Update original: keep status as available, decrement quantity
                self.artwork_repo.update(
                    artwork_id=artwork_id,
                    artist_id=new_data.get("artist_id"),
                    code=new_code,
                    title=new_data.get("title"),
                    description=new_data.get("description", ""),
                    type=new_data.get("type", ""),
                    quantity=old_quantity - 1,
                    year=new_data.get("year"),
                    price=new_data.get("price"),
                    artist_cut_percent=new_data.get("artist_cut_percent", data.get("artist_cut_percent", 10.0)),
                    image=original_image,
                    status=old_status,  # Keep original status
                    notes=new_data.get("notes", "")
                )
            else:
                # Normal update
                self.artwork_repo.update(
                    artwork_id=artwork_id,
                    artist_id=new_data.get("artist_id"),
                    code=new_code,
                    title=new_data.get("title"),
                    description=new_data.get("description", ""),
                    type=new_data.get("type", ""),
                    quantity=new_data.get("quantity", data.get("quantity", 1)),
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
            if self.detail:
                self.detail.clear()

    def sell_artwork(self):
        """Open sell dialog for selected artwork."""
        artwork_id = self.table.get_selected_artwork_id()
        if not artwork_id:
            QMessageBox.information(self.table, "Vendi Opera", "Seleziona un'opera prima.")
            return

        record = self.artwork_repo.get_by_id(artwork_id)
        if not record:
            QMessageBox.warning(self.table, "Vendi Opera", "Opera non trovata.")
            return

        data = dict(record)
        
        # Check if already sold
        if data.get("status") == "sold":
            QMessageBox.warning(self.table, "Vendi Opera", "Questa opera è già stata venduta.")
            return
        
        # Check availability
        if data.get("quantity", 0) < 1:
            QMessageBox.warning(self.table, "Vendi Opera", "Nessuna copia disponibile.")
            return

        dialog = SellArtworkDialog(data, parent=self.table)
        if dialog.exec():
            sale_data = dialog.get_data()
            
            # Create sale record
            if self.sale_repo:
                sale_id = self.sale_repo.create(
                    artwork_id=sale_data["artwork_id"],
                    sale_date=sale_data["sale_date"],
                    sale_price=sale_data["sale_price"],
                    buyer_name=sale_data["buyer_name"],
                    payment_method=sale_data["payment_method"],
                    notes=sale_data["notes"],
                )
                
                # Add artist payment record if there's an artist
                if data.get("artist_id") and sale_id:
                    artist_cut = data.get("artist_cut_percent", 0) or 0
                    artist_amount = sale_data["sale_price"] * (artist_cut / 100)
                    self.sale_repo.add_artist_payment(
                        sale_id=sale_id,
                        artist_id=data["artist_id"],
                        percentage=artist_cut,
                        amount=artist_amount,
                    )
            
            # Update artwork: decrement quantity or mark as sold
            quantity = data.get("quantity", 1)
            if quantity > 1:
                self.artwork_repo.update(
                    artwork_id=artwork_id,
                    artist_id=data.get("artist_id"),
                    code=data.get("code"),
                    title=data.get("title"),
                    description=data.get("description", ""),
                    type=data.get("type", ""),
                    quantity=quantity - 1,
                    year=data.get("year"),
                    price=data.get("price"),
                    artist_cut_percent=data.get("artist_cut_percent", 10.0),
                    image=data.get("image", ""),
                    status=data.get("status", "available"),
                    notes=data.get("notes", ""),
                )
            else:
                # Last copy - mark as sold
                self.artwork_repo.update(
                    artwork_id=artwork_id,
                    artist_id=data.get("artist_id"),
                    code=data.get("code"),
                    title=data.get("title"),
                    description=data.get("description", ""),
                    type=data.get("type", ""),
                    quantity=0,
                    year=data.get("year"),
                    price=data.get("price"),
                    artist_cut_percent=data.get("artist_cut_percent", 10.0),
                    image=data.get("image", ""),
                    status="sold",
                    notes=data.get("notes", ""),
                )
            
            self.load_artworks()
            QMessageBox.information(
                self.table, 
                "Vendita Completata", 
                f"Opera venduta a {sale_data['buyer_name'] or 'acquirente'}\n"
                f"Prezzo: € {sale_data['sale_price']:.2f}"
            )

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
            code = self._clean_code(data.get("code")) or self._generate_code()
            final_image_name = self._persist_image(data.get("image")) if data.get("image") else image_name
            self.artwork_repo.create(
                artist_id=data.get("artist_id"),
                code=code,
                title=data.get("title"),
                description=data.get("description", ""),
                type=data.get("type", ""),
                quantity=data.get("quantity", 1),
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

    def _generate_code(self) -> str:
        """Generate a short unique code for artworks."""
        return f"ART-{uuid.uuid4().hex[:8].upper()}"

    def _clean_code(self, value):
        if value is None:
            return None
        value = str(value).strip()
        return value or None
