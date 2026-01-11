"""
Artwork repository - data access layer for artworks
"""

from pathlib import Path
from core.database import Database


class ArtworkRepository:
    """
    Repository for artwork CRUD operations
    """

    def __init__(self, db: Database):
        self.db = db
        self._ensure_artist_cut_column()

    def _ensure_artist_cut_column(self):
        """Ensure artist_cut_percent column exists for legacy databases."""
        cursor = self.db.execute("PRAGMA table_info(artwork)")
        columns = {row[1] for row in cursor.fetchall()}
        if "artist_cut_percent" not in columns:
            try:
                self.db.execute(
                    "ALTER TABLE artwork ADD COLUMN artist_cut_percent REAL DEFAULT 10"
                )
            except Exception:
                # If migration fails we leave DB untouched to avoid data loss
                pass

    def get_all(self):
        """Get all artworks"""
        cursor = self.db.execute(
            """
            SELECT a.*, ar.name as artist_name
            FROM artwork a
            LEFT JOIN artist ar ON a.artist_id = ar.id
            ORDER BY a.title
            """
        )
        return cursor.fetchall()

    def get_by_id(self, artwork_id: int):
        """Get artwork by ID"""
        cursor = self.db.execute(
            """
            SELECT a.*, ar.name as artist_name
            FROM artwork a
            LEFT JOIN artist ar ON a.artist_id = ar.id
            WHERE a.id = ?
            """,
            (artwork_id,)
        )
        return cursor.fetchone()

    def get_by_artist(self, artist_id: int):
        """Get all artworks by artist"""
        cursor = self.db.execute(
            """
            SELECT a.*, ar.name as artist_name
            FROM artwork a
            LEFT JOIN artist ar ON a.artist_id = ar.id
            WHERE a.artist_id = ?
            ORDER BY a.title
            """,
            (artist_id,)
        )
        return cursor.fetchall()

    def create(self, artist_id: int, title: str, description: str = "",
               type: str = "", year: int = None, price: float = None,
               artist_cut_percent: float = 10.0, image: str = "",
               status: str = "available", notes: str = ""):
        """Create new artwork"""
        cursor = self.db.execute(
            """
            INSERT INTO artwork
            (artist_id, title, description, type, year, price, artist_cut_percent, image, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (artist_id, title, description, type, year, price, artist_cut_percent, image, status, notes)
        )
        return cursor.lastrowid

    def update(self, artwork_id: int, artist_id: int, title: str,
               description: str = "", type: str = "", year: int = None,
               price: float = None, artist_cut_percent: float = 10.0,
               image: str = "", status: str = "available",
               notes: str = ""):
        """Update artwork"""
        self.db.execute(
            """
            UPDATE artwork
            SET artist_id = ?, title = ?, description = ?, type = ?,
                year = ?, price = ?, artist_cut_percent = ?, image = ?, status = ?, notes = ?
            WHERE id = ?
            """,
            (artist_id, title, description, type, year, price, artist_cut_percent, image,
             status, notes, artwork_id)
        )

    def delete(self, artwork_id: int):
        """Delete artwork"""
        self.db.execute("DELETE FROM artwork WHERE id = ?", (artwork_id,))

    def search(self, query: str):
        """Search artworks by title"""
        cursor = self.db.execute(
            """
            SELECT a.*, ar.name as artist_name
            FROM artwork a
            LEFT JOIN artist ar ON a.artist_id = ar.id
            WHERE a.title LIKE ?
            ORDER BY a.title
            """,
            (f"%{query}%",)
        )
        return cursor.fetchall()

    def get_by_status(self, status: str):
        """Get artworks by status"""
        cursor = self.db.execute(
            """
            SELECT a.*, ar.name as artist_name
            FROM artwork a
            LEFT JOIN artist ar ON a.artist_id = ar.id
            WHERE a.status = ?
            ORDER BY a.title
            """,
            (status,)
        )
        return cursor.fetchall()
