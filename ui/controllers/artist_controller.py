from PyQt5.QtWidgets import QMessageBox

from ui.dialogs.add_artist import AddArtistDialog


class ArtistController:
    """Handles artist CRUD UI actions."""

    def __init__(self, artist_repo, artist_list_widget, refresh_artworks_cb):
        self.artist_repo = artist_repo
        self.artist_list = artist_list_widget
        self.refresh_artworks = refresh_artworks_cb

    def load_artists(self):
        rows = self.artist_repo.get_all()
        artists = [dict(r) for r in rows]
        self.artist_list.load_artists(artists)

    def on_artist_selected(self, artist_id: int):
        self.refresh_artworks(artist_id)

    def on_artist_double_click(self, artist_id: int):
        record = self.artist_repo.get_by_id(artist_id)
        if not record:
            QMessageBox.warning(self.artist_list, "Artist", "Artist not found.")
            return

        info_lines = [
            f"Name: {record['name']}",
            f"Email: {record['email'] or '-'}",
            f"Phone: {record['phone'] or '-'}",
            f"Bio: {record['bio'] or '-'}",
            f"Notes: {record['notes'] or '-'}",
        ]
        msg = QMessageBox(self.artist_list)
        msg.setWindowTitle("Artist")
        msg.setText(record['name'])
        msg.setInformativeText("\n".join(info_lines))

        edit_btn = msg.addButton("Edit", QMessageBox.AcceptRole)
        delete_btn = msg.addButton("Delete", QMessageBox.DestructiveRole)
        msg.addButton(QMessageBox.Close)

        msg.exec()

        if msg.clickedButton() == edit_btn:
            self._edit_artist(record)
        elif msg.clickedButton() == delete_btn:
            self._delete_artist(record)

    def add_artist(self):
        dialog = AddArtistDialog(parent=self.artist_list)
        if dialog.exec():
            data = dialog.get_data()
            name = (data.get("name") or "").strip()
            if not name:
                QMessageBox.information(self.artist_list, "Add Artist", "Name is required.")
                return
            self.artist_repo.create(
                name=name,
                bio=data.get("bio", ""),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                notes=data.get("notes", ""),
            )
            self.load_artists()
            self.refresh_artworks()

    def _edit_artist(self, record):
        data = dict(record)
        dialog = AddArtistDialog(parent=self.artist_list)
        dialog.setWindowTitle("Edit Artist")
        dialog.set_data(data)

        if dialog.exec():
            new_data = dialog.get_data()
            name = (new_data.get("name") or "").strip()
            if not name:
                QMessageBox.information(self.artist_list, "Edit Artist", "Name is required.")
                return
            self.artist_repo.update(
                artist_id=record["id"],
                name=name,
                bio=new_data.get("bio", ""),
                email=new_data.get("email", ""),
                phone=new_data.get("phone", ""),
                notes=new_data.get("notes", ""),
            )
            self.load_artists()
            self.refresh_artworks()

    def _delete_artist(self, record):
        confirm = QMessageBox.question(
            self.artist_list,
            "Delete Artist",
            f"Delete artist '{record['name']}' and all related artworks will remain but lose the link. Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.artist_repo.delete(record["id"])
            self.load_artists()
            self.refresh_artworks()
