"""Database schema definitions for the art gallery management system."""

# SQL schema for creating database tables

ARTISTS_TABLE = """
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_year INTEGER,
    nationality TEXT,
    biography TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

ARTWORKS_TABLE = """
CREATE TABLE IF NOT EXISTS artworks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist_id INTEGER NOT NULL,
    year INTEGER,
    medium TEXT,
    dimensions TEXT,
    description TEXT,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists (id)
)
"""

EXHIBITIONS_TABLE = """
CREATE TABLE IF NOT EXISTS exhibitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    location TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

EXHIBITION_ARTWORKS_TABLE = """
CREATE TABLE IF NOT EXISTS exhibition_artworks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exhibition_id INTEGER NOT NULL,
    artwork_id INTEGER NOT NULL,
    FOREIGN KEY (exhibition_id) REFERENCES exhibitions (id),
    FOREIGN KEY (artwork_id) REFERENCES artworks (id),
    UNIQUE(exhibition_id, artwork_id)
)
"""

SALES_TABLE = """
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artwork_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    price REAL NOT NULL,
    buyer_name TEXT,
    buyer_contact TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artwork_id) REFERENCES artworks (id)
)
"""

ALL_TABLES = [
    ARTISTS_TABLE,
    ARTWORKS_TABLE,
    EXHIBITIONS_TABLE,
    EXHIBITION_ARTWORKS_TABLE,
    SALES_TABLE
]
