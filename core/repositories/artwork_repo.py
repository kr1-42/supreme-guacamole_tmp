"""Repository for artwork data access."""

from typing import List, Optional, Dict, Any
from ..database import Database


class ArtworkRepository:
    """Repository for managing artwork data."""
    
    def __init__(self, db: Optional[Database] = None):
        """Initialize artwork repository.
        
        Args:
            db: Database instance. If None, uses singleton instance.
        """
        self.db = db or Database.get_instance()
    
    def create(self, title: str, artist_id: int, year: Optional[int] = None,
               medium: Optional[str] = None, dimensions: Optional[str] = None,
               description: Optional[str] = None, image_path: Optional[str] = None) -> int:
        """Create a new artwork.
        
        Args:
            title: Artwork title
            artist_id: ID of the artist
            year: Year created
            medium: Medium (e.g., oil on canvas)
            dimensions: Dimensions
            description: Description
            image_path: Path to image file
            
        Returns:
            ID of created artwork
        """
        cursor = self.db.execute(
            """INSERT INTO artworks (title, artist_id, year, medium, dimensions, description, image_path)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title, artist_id, year, medium, dimensions, description, image_path)
        )
        return cursor.lastrowid
    
    def get_by_id(self, artwork_id: int) -> Optional[Dict[str, Any]]:
        """Get artwork by ID.
        
        Args:
            artwork_id: Artwork ID
            
        Returns:
            Artwork data as dictionary or None
        """
        row = self.db.fetchone("SELECT * FROM artworks WHERE id = ?", (artwork_id,))
        return dict(row) if row else None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all artworks.
        
        Returns:
            List of artwork dictionaries
        """
        rows = self.db.fetchall("SELECT * FROM artworks ORDER BY title")
        return [dict(row) for row in rows]
    
    def get_by_artist(self, artist_id: int) -> List[Dict[str, Any]]:
        """Get all artworks by an artist.
        
        Args:
            artist_id: Artist ID
            
        Returns:
            List of artwork dictionaries
        """
        rows = self.db.fetchall(
            "SELECT * FROM artworks WHERE artist_id = ? ORDER BY year DESC, title",
            (artist_id,)
        )
        return [dict(row) for row in rows]
    
    def update(self, artwork_id: int, title: Optional[str] = None,
               artist_id: Optional[int] = None, year: Optional[int] = None,
               medium: Optional[str] = None, dimensions: Optional[str] = None,
               description: Optional[str] = None, image_path: Optional[str] = None):
        """Update an artwork.
        
        Args:
            artwork_id: Artwork ID
            title: New title (if provided)
            artist_id: New artist ID (if provided)
            year: New year (if provided)
            medium: New medium (if provided)
            dimensions: New dimensions (if provided)
            description: New description (if provided)
            image_path: New image path (if provided)
        """
        artwork = self.get_by_id(artwork_id)
        if not artwork:
            raise ValueError(f"Artwork with id {artwork_id} not found")
        
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if artist_id is not None:
            updates.append("artist_id = ?")
            params.append(artist_id)
        if year is not None:
            updates.append("year = ?")
            params.append(year)
        if medium is not None:
            updates.append("medium = ?")
            params.append(medium)
        if dimensions is not None:
            updates.append("dimensions = ?")
            params.append(dimensions)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if image_path is not None:
            updates.append("image_path = ?")
            params.append(image_path)
        
        if updates:
            params.append(artwork_id)
            query = f"UPDATE artworks SET {', '.join(updates)} WHERE id = ?"
            self.db.execute(query, tuple(params))
    
    def delete(self, artwork_id: int):
        """Delete an artwork.
        
        Args:
            artwork_id: Artwork ID
        """
        self.db.execute("DELETE FROM artworks WHERE id = ?", (artwork_id,))
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search artworks by title.
        
        Args:
            query: Search query
            
        Returns:
            List of matching artwork dictionaries
        """
        rows = self.db.fetchall(
            "SELECT * FROM artworks WHERE title LIKE ? ORDER BY title",
            (f"%{query}%",)
        )
        return [dict(row) for row in rows]
    
    def get_with_artist(self, artwork_id: int) -> Optional[Dict[str, Any]]:
        """Get artwork with artist information.
        
        Args:
            artwork_id: Artwork ID
            
        Returns:
            Combined artwork and artist data or None
        """
        row = self.db.fetchone(
            """SELECT artworks.*, artists.name as artist_name
               FROM artworks
               JOIN artists ON artworks.artist_id = artists.id
               WHERE artworks.id = ?""",
            (artwork_id,)
        )
        return dict(row) if row else None
    
    def get_all_with_artists(self) -> List[Dict[str, Any]]:
        """Get all artworks with artist information.
        
        Returns:
            List of combined artwork and artist dictionaries
        """
        rows = self.db.fetchall(
            """SELECT artworks.*, artists.name as artist_name
               FROM artworks
               JOIN artists ON artworks.artist_id = artists.id
               ORDER BY artworks.title"""
        )
        return [dict(row) for row in rows]
