"""Database connection and management for the art gallery management system."""

import sqlite3
from typing import Optional
from pathlib import Path

from .schema import ALL_TABLES
from .paths import get_database_path


class Database:
    """Database connection manager."""
    
    _instance: Optional['Database'] = None
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection.
        
        Args:
            db_path: Path to the database file. If None, uses default path.
        """
        self.db_path = db_path or get_database_path()
        self.connection: Optional[sqlite3.Connection] = None
    
    @classmethod
    def get_instance(cls) -> 'Database':
        """Get singleton instance of the database."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def connect(self) -> sqlite3.Connection:
        """Establish database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_schema(self):
        """Create all database tables if they don't exist."""
        conn = self.connect()
        cursor = conn.cursor()
        
        for table_sql in ALL_TABLES:
            cursor.execute(table_sql)
        
        conn.commit()
    
    def execute(self, query: str, params: tuple = ()):
        """Execute a SQL query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Cursor with query results
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    
    def fetchall(self, query: str, params: tuple = ()):
        """Execute a query and fetch all results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of rows
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def fetchone(self, query: str, params: tuple = ()):
        """Execute a query and fetch one result.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Single row or None
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
