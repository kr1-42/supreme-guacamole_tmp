"""Repository for artist data access."""

from typing import List, Optional, Dict, Any
from ..database import Database


class ArtistRepository:
    """Repository for managing artist data."""
    
    def __init__(self, db: Optional[Database] = None):
        """Initialize artist repository.
        
        Args:
            db: Database instance. If None, uses singleton instance.
        """
        self.db = db or Database.get_instance()
    
    def create(self, name: str, birth_year: Optional[int] = None,
               nationality: Optional[str] = None, biography: Optional[str] = None) -> int:
        """Create a new artist.
        
        Args:
            name: Artist name
            birth_year: Year of birth
            nationality: Artist nationality
            biography: Artist biography
            
        Returns:
            ID of created artist
        """
        cursor = self.db.execute(
            "INSERT INTO artists (name, birth_year, nationality, biography) VALUES (?, ?, ?, ?)",
            (name, birth_year, nationality, biography)
        )
        return cursor.lastrowid
    
    def get_by_id(self, artist_id: int) -> Optional[Dict[str, Any]]:
        """Get artist by ID.
        
        Args:
            artist_id: Artist ID
            
        Returns:
            Artist data as dictionary or None
        """
        row = self.db.fetchone("SELECT * FROM artists WHERE id = ?", (artist_id,))
        return dict(row) if row else None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all artists.
        
        Returns:
            List of artist dictionaries
        """
        rows = self.db.fetchall("SELECT * FROM artists ORDER BY name")
        return [dict(row) for row in rows]
    
    def update(self, artist_id: int, name: Optional[str] = None,
               birth_year: Optional[int] = None, nationality: Optional[str] = None,
               biography: Optional[str] = None):
        """Update an artist.
        
        Args:
            artist_id: Artist ID
            name: New name (if provided)
            birth_year: New birth year (if provided)
            nationality: New nationality (if provided)
            biography: New biography (if provided)
        """
        artist = self.get_by_id(artist_id)
        if not artist:
            raise ValueError(f"Artist with id {artist_id} not found")
        
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if birth_year is not None:
            updates.append("birth_year = ?")
            params.append(birth_year)
        if nationality is not None:
            updates.append("nationality = ?")
            params.append(nationality)
        if biography is not None:
            updates.append("biography = ?")
            params.append(biography)
        
        if updates:
            params.append(artist_id)
            query = f"UPDATE artists SET {', '.join(updates)} WHERE id = ?"
            self.db.execute(query, tuple(params))
    
    def delete(self, artist_id: int):
        """Delete an artist.
        
        Args:
            artist_id: Artist ID
        """
        self.db.execute("DELETE FROM artists WHERE id = ?", (artist_id,))
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search artists by name.
        
        Args:
            query: Search query
            
        Returns:
            List of matching artist dictionaries
        """
        rows = self.db.fetchall(
            "SELECT * FROM artists WHERE name LIKE ? ORDER BY name",
            (f"%{query}%",)
        )
        return [dict(row) for row in rows]
