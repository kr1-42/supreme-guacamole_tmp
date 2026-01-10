# Art Catalog Manager

A desktop application for managing art catalogs, artists, artworks, exhibitions, and sales.

## Features

- **Artist Management**: Add, edit, and manage artist profiles with bio, contact info, and notes
- **Artwork Catalog**: Track artworks with images, descriptions, pricing, and status
- **Exhibition Planning**: Organize exhibitions and associate artworks
- **Sales Tracking**: Record sales transactions and artist payment splits
- **Image Gallery**: View artwork images with preview functionality

## Project Structure

```
./
├── main.py                  # Application entry point
├── core/                    # Core business logic
│   ├── database.py          # SQLite database wrapper
│   ├── schema.py            # Database schema definition
│   ├── paths.py             # Path configuration
│   └── repositories/        # Data access layer
│       ├── artist_repo.py
│       ├── artwork_repo.py
│       ├── exhibition_repo.py
│       └── sale_repo.py
├── ui/                      # User interface
│   ├── main_window.py       # Main application window
│   ├── dialogs/             # Dialog windows
│   │   ├── add_artist.py
│   │   ├── add_artwork.py
│   │   └── add_exhibition.py
│   └── widgets/             # Custom widgets
│       ├── artist_list.py
│       ├── artwork_table.py
│       └── image_preview.py
├── assets/icons/            # Application icons
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kr1-42/supreme-guacamole_tmp.git
cd supreme-guacamole_tmp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

On first run, the application will create the necessary directories and database:
- `~/ArtCatalog/data/` - Database storage
- `~/ArtCatalog/images/artworks/` - Artwork images
- `~/ArtCatalog/backups/` - Database backups

## Requirements

- Python 3.8+
- PySide6 6.5.0+

## License

This project is for internal use.
