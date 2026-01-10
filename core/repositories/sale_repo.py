"""Repository for sale data access."""

from typing import List, Optional, Dict, Any
from ..database import Database


class SaleRepository:
    """Repository for managing sale data."""
    
    def __init__(self, db: Optional[Database] = None):
        """Initialize sale repository.
        
        Args:
            db: Database instance. If None, uses singleton instance.
        """
        self.db = db or Database.get_instance()
    
    def create(self, artwork_id: int, sale_date: str, price: float,
               buyer_name: Optional[str] = None, buyer_contact: Optional[str] = None,
               notes: Optional[str] = None) -> int:
        """Create a new sale record.
        
        Args:
            artwork_id: ID of the artwork sold
            sale_date: Date of sale (YYYY-MM-DD)
            price: Sale price
            buyer_name: Name of buyer
            buyer_contact: Contact information for buyer
            notes: Additional notes
            
        Returns:
            ID of created sale
        """
        cursor = self.db.execute(
            """INSERT INTO sales (artwork_id, sale_date, price, buyer_name, buyer_contact, notes)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (artwork_id, sale_date, price, buyer_name, buyer_contact, notes)
        )
        return cursor.lastrowid
    
    def get_by_id(self, sale_id: int) -> Optional[Dict[str, Any]]:
        """Get sale by ID.
        
        Args:
            sale_id: Sale ID
            
        Returns:
            Sale data as dictionary or None
        """
        row = self.db.fetchone("SELECT * FROM sales WHERE id = ?", (sale_id,))
        return dict(row) if row else None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all sales.
        
        Returns:
            List of sale dictionaries
        """
        rows = self.db.fetchall("SELECT * FROM sales ORDER BY sale_date DESC")
        return [dict(row) for row in rows]
    
    def get_by_artwork(self, artwork_id: int) -> List[Dict[str, Any]]:
        """Get all sales for an artwork.
        
        Args:
            artwork_id: Artwork ID
            
        Returns:
            List of sale dictionaries
        """
        rows = self.db.fetchall(
            "SELECT * FROM sales WHERE artwork_id = ? ORDER BY sale_date DESC",
            (artwork_id,)
        )
        return [dict(row) for row in rows]
    
    def update(self, sale_id: int, artwork_id: Optional[int] = None,
               sale_date: Optional[str] = None, price: Optional[float] = None,
               buyer_name: Optional[str] = None, buyer_contact: Optional[str] = None,
               notes: Optional[str] = None):
        """Update a sale record.
        
        Args:
            sale_id: Sale ID
            artwork_id: New artwork ID (if provided)
            sale_date: New sale date (if provided)
            price: New price (if provided)
            buyer_name: New buyer name (if provided)
            buyer_contact: New buyer contact (if provided)
            notes: New notes (if provided)
        """
        sale = self.get_by_id(sale_id)
        if not sale:
            raise ValueError(f"Sale with id {sale_id} not found")
        
        updates = []
        params = []
        
        if artwork_id is not None:
            updates.append("artwork_id = ?")
            params.append(artwork_id)
        if sale_date is not None:
            updates.append("sale_date = ?")
            params.append(sale_date)
        if price is not None:
            updates.append("price = ?")
            params.append(price)
        if buyer_name is not None:
            updates.append("buyer_name = ?")
            params.append(buyer_name)
        if buyer_contact is not None:
            updates.append("buyer_contact = ?")
            params.append(buyer_contact)
        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)
        
        if updates:
            params.append(sale_id)
            query = f"UPDATE sales SET {', '.join(updates)} WHERE id = ?"
            self.db.execute(query, tuple(params))
    
    def delete(self, sale_id: int):
        """Delete a sale record.
        
        Args:
            sale_id: Sale ID
        """
        self.db.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
    
    def get_with_artwork(self, sale_id: int) -> Optional[Dict[str, Any]]:
        """Get sale with artwork and artist information.
        
        Args:
            sale_id: Sale ID
            
        Returns:
            Combined sale, artwork, and artist data or None
        """
        row = self.db.fetchone(
            """SELECT sales.*, artworks.title as artwork_title, artists.name as artist_name
               FROM sales
               JOIN artworks ON sales.artwork_id = artworks.id
               JOIN artists ON artworks.artist_id = artists.id
               WHERE sales.id = ?""",
            (sale_id,)
        )
        return dict(row) if row else None
    
    def get_all_with_artworks(self) -> List[Dict[str, Any]]:
        """Get all sales with artwork and artist information.
        
        Returns:
            List of combined sale, artwork, and artist dictionaries
        """
        rows = self.db.fetchall(
            """SELECT sales.*, artworks.title as artwork_title, artists.name as artist_name
               FROM sales
               JOIN artworks ON sales.artwork_id = artworks.id
               JOIN artists ON artworks.artist_id = artists.id
               ORDER BY sales.sale_date DESC"""
        )
        return [dict(row) for row in rows]
    
    def get_total_sales(self) -> float:
        """Get total sales amount.
        
        Returns:
            Total sales amount
        """
        row = self.db.fetchone("SELECT SUM(price) as total FROM sales")
        return row['total'] if row and row['total'] else 0.0
