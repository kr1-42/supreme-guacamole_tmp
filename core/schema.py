"""
Database schema for Art Catalog Manager
"""

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

-- =========================
-- ARTISTS
-- =========================
CREATE TABLE IF NOT EXISTS artist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    bio TEXT,
    email TEXT,
    phone TEXT,
    notes TEXT
);

-- =========================
-- ARTWORKS / ARTICLES
-- =========================
CREATE TABLE IF NOT EXISTS artwork (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    type TEXT,
    year INTEGER,
    price REAL,
    image TEXT,
    status TEXT DEFAULT 'available',
    notes TEXT,
    FOREIGN KEY (artist_id)
        REFERENCES artist(id)
        ON DELETE SET NULL
);

-- =========================
-- EXHIBITIONS
-- =========================
CREATE TABLE IF NOT EXISTS exhibition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT,
    start_date TEXT,
    end_date TEXT,
    description TEXT
);

-- =========================
-- EXHIBITION <-> ARTWORK
-- =========================
CREATE TABLE IF NOT EXISTS exhibition_artwork (
    exhibition_id INTEGER NOT NULL,
    artwork_id INTEGER NOT NULL,
    PRIMARY KEY (exhibition_id, artwork_id),
    FOREIGN KEY (exhibition_id)
        REFERENCES exhibition(id)
        ON DELETE CASCADE,
    FOREIGN KEY (artwork_id)
        REFERENCES artwork(id)
        ON DELETE CASCADE
);

-- =========================
-- SALES
-- =========================
CREATE TABLE IF NOT EXISTS sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artwork_id INTEGER NOT NULL,
    sale_date TEXT NOT NULL,
    sale_price REAL NOT NULL,
    buyer_name TEXT,
    payment_method TEXT,
    notes TEXT,
    FOREIGN KEY (artwork_id)
        REFERENCES artwork(id)
);

-- =========================
-- ARTIST PAYMENTS
-- =========================
CREATE TABLE IF NOT EXISTS artist_payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    artist_id INTEGER NOT NULL,
    percentage REAL NOT NULL,
    amount REAL NOT NULL,
    paid INTEGER DEFAULT 0,
    FOREIGN KEY (sale_id)
        REFERENCES sale(id),
    FOREIGN KEY (artist_id)
        REFERENCES artist(id)
);

-- =========================
-- USERS (OPTIONAL)
-- =========================
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    pin TEXT
);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX IF NOT EXISTS idx_artwork_artist
    ON artwork(artist_id);

CREATE INDEX IF NOT EXISTS idx_artwork_status
    ON artwork(status);

CREATE INDEX IF NOT EXISTS idx_sale_date
    ON sale(sale_date);
"""
