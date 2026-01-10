"""
Sale repository - data access layer for sales and artist payments
"""

from pathlib import Path
from core.database import Database


class SaleRepository:
    """
    Repository for sale CRUD operations
    """

    def __init__(self, db: Database):
        self.db = db

    def get_all(self):
        """Get all sales"""
        cursor = self.db.execute(
            """
            SELECT s.*, a.title as artwork_title, ar.name as artist_name
            FROM sale s
            INNER JOIN artwork a ON s.artwork_id = a.id
            LEFT JOIN artist ar ON a.artist_id = ar.id
            ORDER BY s.sale_date DESC
            """
        )
        return cursor.fetchall()

    def get_by_id(self, sale_id: int):
        """Get sale by ID"""
        cursor = self.db.execute(
            """
            SELECT s.*, a.title as artwork_title, ar.name as artist_name
            FROM sale s
            INNER JOIN artwork a ON s.artwork_id = a.id
            LEFT JOIN artist ar ON a.artist_id = ar.id
            WHERE s.id = ?
            """,
            (sale_id,)
        )
        return cursor.fetchone()

    def create(self, artwork_id: int, sale_date: str, sale_price: float,
               buyer_name: str = "", payment_method: str = "", notes: str = ""):
        """Create new sale"""
        cursor = self.db.execute(
            """
            INSERT INTO sale 
            (artwork_id, sale_date, sale_price, buyer_name, payment_method, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (artwork_id, sale_date, sale_price, buyer_name, payment_method, notes)
        )
        return cursor.lastrowid

    def update(self, sale_id: int, artwork_id: int, sale_date: str,
               sale_price: float, buyer_name: str = "", payment_method: str = "",
               notes: str = ""):
        """Update sale"""
        self.db.execute(
            """
            UPDATE sale
            SET artwork_id = ?, sale_date = ?, sale_price = ?,
                buyer_name = ?, payment_method = ?, notes = ?
            WHERE id = ?
            """,
            (artwork_id, sale_date, sale_price, buyer_name, payment_method, 
             notes, sale_id)
        )

    def delete(self, sale_id: int):
        """Delete sale"""
        self.db.execute("DELETE FROM sale WHERE id = ?", (sale_id,))

    def add_artist_payment(self, sale_id: int, artist_id: int, 
                          percentage: float, amount: float):
        """Add artist payment for a sale"""
        cursor = self.db.execute(
            """
            INSERT INTO artist_payment (sale_id, artist_id, percentage, amount)
            VALUES (?, ?, ?, ?)
            """,
            (sale_id, artist_id, percentage, amount)
        )
        return cursor.lastrowid

    def mark_payment_paid(self, payment_id: int):
        """Mark artist payment as paid"""
        self.db.execute(
            "UPDATE artist_payment SET paid = 1 WHERE id = ?",
            (payment_id,)
        )

    def get_artist_payments(self, artist_id: int):
        """Get all payments for an artist"""
        cursor = self.db.execute(
            """
            SELECT ap.*, s.sale_date, a.title as artwork_title
            FROM artist_payment ap
            INNER JOIN sale s ON ap.sale_id = s.id
            INNER JOIN artwork a ON s.artwork_id = a.id
            WHERE ap.artist_id = ?
            ORDER BY s.sale_date DESC
            """,
            (artist_id,)
        )
        return cursor.fetchall()

    def get_unpaid_payments(self, artist_id: int = None):
        """Get unpaid artist payments"""
        if artist_id:
            cursor = self.db.execute(
                """
                SELECT ap.*, s.sale_date, a.title as artwork_title, ar.name as artist_name
                FROM artist_payment ap
                INNER JOIN sale s ON ap.sale_id = s.id
                INNER JOIN artwork a ON s.artwork_id = a.id
                INNER JOIN artist ar ON ap.artist_id = ar.id
                WHERE ap.paid = 0 AND ap.artist_id = ?
                ORDER BY s.sale_date
                """,
                (artist_id,)
            )
        else:
            cursor = self.db.execute(
                """
                SELECT ap.*, s.sale_date, a.title as artwork_title, ar.name as artist_name
                FROM artist_payment ap
                INNER JOIN sale s ON ap.sale_id = s.id
                INNER JOIN artwork a ON s.artwork_id = a.id
                INNER JOIN artist ar ON ap.artist_id = ar.id
                WHERE ap.paid = 0
                ORDER BY s.sale_date
                """
            )
        return cursor.fetchall()
