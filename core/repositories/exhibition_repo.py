"""
Exhibition repository - data access layer for exhibitions
"""

from pathlib import Path
from core.database import Database


class ExhibitionRepository:
    """
    Repository for exhibition CRUD operations
    """

    def __init__(self, db: Database):
        self.db = db

    def get_all(self):
        """Get all exhibitions"""
        cursor = self.db.execute(
            "SELECT * FROM exhibition ORDER BY start_date DESC"
        )
        return cursor.fetchall()

    def get_by_id(self, exhibition_id: int):
        """Get exhibition by ID"""
        cursor = self.db.execute(
            "SELECT * FROM exhibition WHERE id = ?", (exhibition_id,)
        )
        return cursor.fetchone()

    def create(self, name: str, location: str = "", start_date: str = "",
               end_date: str = "", description: str = ""):
        """Create new exhibition"""
        cursor = self.db.execute(
            """
            INSERT INTO exhibition (name, location, start_date, end_date, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, location, start_date, end_date, description)
        )
        return cursor.lastrowid

    def update(self, exhibition_id: int, name: str, location: str = "",
               start_date: str = "", end_date: str = "", description: str = ""):
        """Update exhibition"""
        self.db.execute(
            """
            UPDATE exhibition
            SET name = ?, location = ?, start_date = ?, end_date = ?, description = ?
            WHERE id = ?
            """,
            (name, location, start_date, end_date, description, exhibition_id)
        )

    def delete(self, exhibition_id: int):
        """Delete exhibition"""
        self.db.execute("DELETE FROM exhibition WHERE id = ?", (exhibition_id,))

    def add_artwork(self, exhibition_id: int, artwork_id: int):
        """Add artwork to exhibition"""
        self.db.execute(
            """
            INSERT OR IGNORE INTO exhibition_artwork (exhibition_id, artwork_id)
            VALUES (?, ?)
            """,
            (exhibition_id, artwork_id)
        )

    def remove_artwork(self, exhibition_id: int, artwork_id: int):
        """Remove artwork from exhibition"""
        self.db.execute(
            """
            DELETE FROM exhibition_artwork
            WHERE exhibition_id = ? AND artwork_id = ?
            """,
            (exhibition_id, artwork_id)
        )

    def get_artworks(self, exhibition_id: int):
        """Get all artworks in exhibition"""
        cursor = self.db.execute(
            """
            SELECT a.*, ar.name as artist_name
            FROM artwork a
            INNER JOIN exhibition_artwork ea ON a.id = ea.artwork_id
            LEFT JOIN artist ar ON a.artist_id = ar.id
            WHERE ea.exhibition_id = ?
            ORDER BY a.title
            """,
            (exhibition_id,)
        )
        return cursor.fetchall()
