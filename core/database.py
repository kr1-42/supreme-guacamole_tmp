# core/database.py
import sqlite3
from pathlib import Path


def get_db_path():
    """Get the path to the database file."""
    base = Path(__file__).parent.parent
    return base / "data" / "db.sqlite3"


def init_db():
    """Initialize the database with the required schema."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create artists table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT,
            contact TEXT,
            created_at TEXT NOT NULL
        );
    """)
    
    # Create exhibitions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exhibitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            location TEXT,
            start_date TEXT,
            end_date TEXT,
            created_at TEXT NOT NULL
        );
    """)
    
    # Create artworks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artworks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER NOT NULL,
            exhibition_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            price REAL,
            image_path TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
            FOREIGN KEY (exhibition_id) REFERENCES exhibitions(id) ON DELETE SET NULL
        );
    """)
    
    # Create sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artwork_id INTEGER NOT NULL,
            buyer_name TEXT,
            sale_price REAL NOT NULL,
            sale_date TEXT NOT NULL,
            FOREIGN KEY (artwork_id) REFERENCES artworks(id) ON DELETE CASCADE
        );
    """)
    
    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_artworks_artist ON artworks(artist_id);
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_artworks_exhibition ON artworks(exhibition_id);
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sales_artwork ON sales(artwork_id);
    """)
    
    conn.commit()
    conn.close()
