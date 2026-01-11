"""
Artist repository - data access layer for artists
"""

from pathlib import Path
from core.database import Database


class ArtistRepository:
    """
    Repository for artist CRUD operations
    """

    def __init__(self, db: Database):
        self.db = db

    def get_all(self):
        """Get all artists"""
        cursor = self.db.execute("SELECT * FROM artist ORDER BY name")
        return cursor.fetchall()

    def get_by_id(self, artist_id: int):
        """Get artist by ID"""
        cursor = self.db.execute(
            "SELECT * FROM artist WHERE id = ?", (artist_id,)
        )
        return cursor.fetchone()

    def create(self, name: str, bio: str = "", email: str = "", 
               phone: str = "", notes: str = ""):
        """Create new artist"""
        cursor = self.db.execute(
            """
            INSERT INTO artist (name, bio, email, phone, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, bio, email, phone, notes)
        )
        return cursor.lastrowid

    def update(self, artist_id: int, name: str, bio: str = "", 
               email: str = "", phone: str = "", notes: str = ""):
        """Update artist"""
        self.db.execute(
            """
            UPDATE artist
            SET name = ?, bio = ?, email = ?, phone = ?, notes = ?
            WHERE id = ?
            """,
            (name, bio, email, phone, notes, artist_id)
        )

    def delete(self, artist_id: int):
        """Delete artist"""
        self.db.execute("DELETE FROM artist WHERE id = ?", (artist_id,))

    def search(self, query: str):
        """Search artists by name"""
        cursor = self.db.execute(
            "SELECT * FROM artist WHERE name LIKE ? ORDER BY name",
            (f"%{query}%",)
        )
        return cursor.fetchall()
