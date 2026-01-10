"""Repository for exhibition data access."""

from typing import List, Optional, Dict, Any
from ..database import Database


class ExhibitionRepository:
    """Repository for managing exhibition data."""
    
    def __init__(self, db: Optional[Database] = None):
        """Initialize exhibition repository.
        
        Args:
            db: Database instance. If None, uses singleton instance.
        """
        self.db = db or Database.get_instance()
    
    def create(self, title: str, start_date: str, end_date: str,
               location: Optional[str] = None, description: Optional[str] = None) -> int:
        """Create a new exhibition.
        
        Args:
            title: Exhibition title
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            location: Location
            description: Description
            
        Returns:
            ID of created exhibition
        """
        cursor = self.db.execute(
            """INSERT INTO exhibitions (title, start_date, end_date, location, description)
               VALUES (?, ?, ?, ?, ?)""",
            (title, start_date, end_date, location, description)
        )
        return cursor.lastrowid
    
    def get_by_id(self, exhibition_id: int) -> Optional[Dict[str, Any]]:
        """Get exhibition by ID.
        
        Args:
            exhibition_id: Exhibition ID
            
        Returns:
            Exhibition data as dictionary or None
        """
        row = self.db.fetchone("SELECT * FROM exhibitions WHERE id = ?", (exhibition_id,))
        return dict(row) if row else None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all exhibitions.
        
        Returns:
            List of exhibition dictionaries
        """
        rows = self.db.fetchall("SELECT * FROM exhibitions ORDER BY start_date DESC")
        return [dict(row) for row in rows]
    
    def update(self, exhibition_id: int, title: Optional[str] = None,
               start_date: Optional[str] = None, end_date: Optional[str] = None,
               location: Optional[str] = None, description: Optional[str] = None):
        """Update an exhibition.
        
        Args:
            exhibition_id: Exhibition ID
            title: New title (if provided)
            start_date: New start date (if provided)
            end_date: New end date (if provided)
            location: New location (if provided)
            description: New description (if provided)
        """
        exhibition = self.get_by_id(exhibition_id)
        if not exhibition:
            raise ValueError(f"Exhibition with id {exhibition_id} not found")
        
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if start_date is not None:
            updates.append("start_date = ?")
            params.append(start_date)
        if end_date is not None:
            updates.append("end_date = ?")
            params.append(end_date)
        if location is not None:
            updates.append("location = ?")
            params.append(location)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if updates:
            params.append(exhibition_id)
            query = f"UPDATE exhibitions SET {', '.join(updates)} WHERE id = ?"
            self.db.execute(query, tuple(params))
    
    def delete(self, exhibition_id: int):
        """Delete an exhibition.
        
        Args:
            exhibition_id: Exhibition ID
        """
        # First delete exhibition-artwork relationships
        self.db.execute("DELETE FROM exhibition_artworks WHERE exhibition_id = ?", (exhibition_id,))
        # Then delete the exhibition
        self.db.execute("DELETE FROM exhibitions WHERE id = ?", (exhibition_id,))
    
    def add_artwork(self, exhibition_id: int, artwork_id: int):
        """Add an artwork to an exhibition.
        
        Args:
            exhibition_id: Exhibition ID
            artwork_id: Artwork ID
        """
        self.db.execute(
            "INSERT OR IGNORE INTO exhibition_artworks (exhibition_id, artwork_id) VALUES (?, ?)",
            (exhibition_id, artwork_id)
        )
    
    def remove_artwork(self, exhibition_id: int, artwork_id: int):
        """Remove an artwork from an exhibition.
        
        Args:
            exhibition_id: Exhibition ID
            artwork_id: Artwork ID
        """
        self.db.execute(
            "DELETE FROM exhibition_artworks WHERE exhibition_id = ? AND artwork_id = ?",
            (exhibition_id, artwork_id)
        )
    
    def get_artworks(self, exhibition_id: int) -> List[Dict[str, Any]]:
        """Get all artworks in an exhibition.
        
        Args:
            exhibition_id: Exhibition ID
            
        Returns:
            List of artwork dictionaries
        """
        rows = self.db.fetchall(
            """SELECT artworks.*, artists.name as artist_name
               FROM artworks
               JOIN exhibition_artworks ON artworks.id = exhibition_artworks.artwork_id
               JOIN artists ON artworks.artist_id = artists.id
               WHERE exhibition_artworks.exhibition_id = ?
               ORDER BY artworks.title""",
            (exhibition_id,)
        )
        return [dict(row) for row in rows]
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search exhibitions by title.
        
        Args:
            query: Search query
            
        Returns:
            List of matching exhibition dictionaries
        """
        rows = self.db.fetchall(
            "SELECT * FROM exhibitions WHERE title LIKE ? ORDER BY start_date DESC",
            (f"%{query}%",)
        )
        return [dict(row) for row in rows]
