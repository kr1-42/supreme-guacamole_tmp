"""
Database schema for Art Catalog Manager
"""

SCHEMA_SQL = """
-- =========================================================
-- ART CATALOG MANAGEMENT DATABASE
-- =========================================================
-- Target:
--  - Azienda che organizza mostre d'arte
--  - Artisti che vendono opere e articoli
--  - Uso locale su macOS
--  - SQLite (file singolo, backup facile)
--
-- NOTE IMPORTANTI:
--  - Tutte le date sono in formato ISO (YYYY-MM-DD o ISO datetime)
--  - Le immagini NON sono salvate nel DB
--    -> solo il nome del file
--  - Le foreign key sono attive
-- =========================================================

PRAGMA foreign_keys = ON;

-- =========================================================
-- TABLE: artist
-- =========================================================
-- Contiene gli artisti che partecipano alle mostre
-- e vendono opere / articoli tramite l'azienda
-- =========================================================
CREATE TABLE IF NOT EXISTS artist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,          -- Nome artista / collettivo
    bio TEXT,                    -- Biografia
    email TEXT,                  -- Contatto
    phone TEXT,                  -- Contatto
    notes TEXT                   -- Note interne (non pubbliche)
);

-- =========================================================
-- TABLE: artwork
-- =========================================================
-- Contiene TUTTE le opere e gli articoli vendibili
-- Può essere:
--  - opera d'arte (quadro, scultura, foto)
--  - articolo (stampe, merch, libri)
--
-- status:
--  - available : disponibile
--  - sold      : venduto
--  - reserved  : riservato
-- =========================================================
CREATE TABLE IF NOT EXISTS artwork (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artist_id INTEGER,           -- FK verso artist (puo essere NULL)
    title TEXT NOT NULL,         -- Titolo opera / articolo
    description TEXT,            -- Descrizione estesa
    type TEXT,                   -- painting, sculpture, print, merch, ecc.
    year INTEGER,                -- Anno di produzione
    price REAL,                  -- Prezzo di listino
    artist_cut_percent REAL DEFAULT 10, -- Percentuale riconosciuta all'artista
    image TEXT,                  -- Nome file immagine (NO path)
    status TEXT DEFAULT 'available',
    notes TEXT,                  -- Note interne

    FOREIGN KEY (artist_id)
        REFERENCES artist(id)
        ON DELETE SET NULL
);

-- =========================================================
-- TABLE: exhibition
-- =========================================================
-- Rappresenta una mostra organizzata dall'azienda
-- Una mostra puo contenere molte opere
-- =========================================================
CREATE TABLE IF NOT EXISTS exhibition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,          -- Nome mostra
    location TEXT,               -- Luogo
    start_date TEXT,             -- YYYY-MM-DD
    end_date TEXT,               -- YYYY-MM-DD
    description TEXT             -- Testo curatoriale
);

-- =========================================================
-- TABLE: exhibition_artwork
-- =========================================================
-- Tabella di relazione MANY-TO-MANY
-- Un'opera puo apparire in piu mostre
-- Una mostra contiene piu opere
-- =========================================================
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

-- =========================================================
-- TABLE: sale
-- =========================================================
-- Registra una vendita effettiva
-- Ogni opera venduta genera UNA riga qui
-- =========================================================
CREATE TABLE IF NOT EXISTS sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    artwork_id INTEGER NOT NULL,
    sale_date TEXT NOT NULL,     -- ISO datetime
    sale_price REAL NOT NULL,    -- Prezzo finale
    buyer_name TEXT,             -- Cliente
    payment_method TEXT,         -- cash, card, bank, crypto, ecc.
    notes TEXT,

    FOREIGN KEY (artwork_id)
        REFERENCES artwork(id)
);

-- =========================================================
-- TABLE: artist_payment
-- =========================================================
-- Serve per tracciare quanto spetta all'artista
-- dopo una vendita
--
-- paid:
--  - 0 = non ancora pagato
--  - 1 = pagato
-- =========================================================
CREATE TABLE IF NOT EXISTS artist_payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sale_id INTEGER NOT NULL,
    artist_id INTEGER NOT NULL,
    percentage REAL NOT NULL,    -- % concordata
    amount REAL NOT NULL,        -- Importo calcolato
    paid INTEGER DEFAULT 0,

    FOREIGN KEY (sale_id)
        REFERENCES sale(id),

    FOREIGN KEY (artist_id)
        REFERENCES artist(id)
);

-- =========================================================
-- TABLE: user (OPZIONALE)
-- =========================================================
-- Per accesso interno al gestionale
-- (PIN semplice, non sicurezza bancaria)
-- =========================================================
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    pin TEXT
);

-- =========================================================
-- INDEXES
-- =========================================================
-- Migliorano prestazioni su liste e filtri
-- =========================================================
CREATE INDEX IF NOT EXISTS idx_artwork_artist
    ON artwork(artist_id);

CREATE INDEX IF NOT EXISTS idx_artwork_status
    ON artwork(status);

CREATE INDEX IF NOT EXISTS idx_sale_date
    ON sale(sale_date);
"""
