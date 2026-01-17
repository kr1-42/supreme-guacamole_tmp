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

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
source venv/bin/activate  # If not already activated
python main.py
```

On first run, the application will create the necessary directories and database:
- `data/` - Database storage
- `images/artworks/` - Artwork images
- `backups/` - Database backups

---

## 📱 Live Database via QR Code (Datasette)

You can share your database as a live spreadsheet accessible via QR code on any device connected to your network.

### Step-by-Step Instructions

**1. Activate the virtual environment:**
```bash
cd /home/tails/Documents/projects/supreme-guacamole_tmp
source venv/bin/activate
```

**2. Start the Datasette server:**
```bash
python scripts/serve_database.py
```

**3. You'll see output like this:**
```
============================================================
🎨 Art Catalog - Live Database Viewer
============================================================

📂 Database: /path/to/data/catalog.db

🌐 Access URLs:
   Local:   http://localhost:8001
   Network: http://192.168.1.X:8001

📱 Scan this QR code to access from your phone:
   [QR CODE displayed in terminal]

📱 QR code saved to: assets/qr_code.png
============================================================
```

**4. Access the database:**
- **On your computer:** Open http://localhost:8001 in your browser
- **On your phone/tablet:** Scan the QR code shown in the terminal (or saved at `assets/qr_code.png`)
- **Other devices on your network:** Use the Network URL (e.g., http://192.168.1.X:8001)

**5. What you can do in Datasette:**
- Browse all tables (artists, artworks, exhibitions, sales)
- Search and filter data
- Sort columns
- Export data as CSV or JSON
- Run custom SQL queries

**6. To stop the server:**
Press `Ctrl+C` in the terminal.

### Notes
- All devices must be on the **same WiFi network**
- The server runs as long as the terminal is open
- Changes made in the main app will appear immediately in Datasette (refresh the page)

---

## Requirements

- Python 3.8+
- PyQt5 5.15+
- datasette (for live database viewing)
- qrcode (for QR code generation)

## License

This project is for internal use.
