# supreme-guacamole_tmp
Prezzario temporanea // progetto ui gestionale

## Art Management System

A PySide6-based desktop application for managing art galleries, including artists, artworks, exhibitions, and sales.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

On first run, the application will:
1. Create the necessary directory structure under `data/`
2. Initialize the SQLite database with the required schema

## Directory Structure

```
data/
├── db.sqlite3              # SQLite database
├── images/
│   ├── artists/            # Artist profile images
│   ├── artworks/           # Artwork images
│   └── exhibitions/        # Exhibition images
├── documents/
│   ├── invoices/           # Sales invoices
│   ├── contracts/          # Artist contracts
│   └── certificates/       # Artwork certificates
└── backups/                # Database backups
```

## Database Schema

### Tables

- **artists**: Artist information (id, name, bio, contact, created_at)
- **exhibitions**: Exhibition details (id, title, location, start_date, end_date, created_at)
- **artworks**: Artwork records with foreign keys to artists and exhibitions
- **sales**: Sales transactions linked to artworks

### Features

- Foreign key constraints with CASCADE and SET NULL behaviors
- Indexes on foreign key columns for optimized queries
- Automatic timestamp tracking
