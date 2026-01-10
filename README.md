# Art Gallery Management System

A comprehensive desktop application for managing art gallery operations including artists, artworks, exhibitions, and sales.

## Features

- **Artist Management**: Add, edit, delete, and search for artists with biographical information
- **Artwork Management**: Track artworks with images, medium, dimensions, and descriptions
- **Exhibition Management**: Organize exhibitions and associate artworks with them
- **Sales Tracking**: Record artwork sales with buyer information and pricing
- **Image Preview**: View artwork images directly in the application
- **Search & Filter**: Quickly find artists and artworks using search functionality

## Project Structure

```
./
├── main.py                          # Application entry point
├── core/                            # Core business logic
│   ├── database.py                  # Database connection management
│   ├── schema.py                    # Database schema definitions
│   ├── paths.py                     # Path utilities
│   └── repositories/                # Data access layer
│       ├── artist_repo.py           # Artist data operations
│       ├── artwork_repo.py          # Artwork data operations
│       ├── exhibition_repo.py       # Exhibition data operations
│       └── sale_repo.py             # Sale data operations
├── ui/                              # User interface components
│   ├── main_window.py               # Main application window
│   ├── dialogs/                     # Dialog windows
│   │   ├── add_artist.py            # Artist add/edit dialog
│   │   ├── add_artwork.py           # Artwork add/edit dialog
│   │   └── add_exhibition.py        # Exhibition add/edit dialog
│   └── widgets/                     # Reusable UI widgets
│       ├── artist_list.py           # Artist list display
│       ├── artwork_table.py         # Artwork table display
│       └── image_preview.py         # Image preview widget
├── assets/icons/                    # Application icons
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kr1-42/supreme-guacamole_tmp.git
   cd supreme-guacamole_tmp
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

### Basic Workflow

1. **Add Artists**: Start by adding artists through the "Artists" tab
2. **Add Artworks**: Create artwork entries and associate them with artists
3. **Create Exhibitions**: Organize artworks into exhibitions
4. **Track Sales**: Record sales information for sold artworks

### Features by Tab

#### Artists Tab
- View all artists in a searchable list
- Add new artists with biographical details
- Edit existing artist information
- Delete artists (warning: will affect associated artworks)
- View artist details including biography

#### Artworks Tab
- Browse artworks in a table view with sorting
- Add new artworks with images and metadata
- Edit artwork information
- Delete artworks
- Preview artwork images
- View artwork details

#### Exhibitions Tab
- Create and manage exhibitions
- Set exhibition dates and locations
- Add multiple artworks to exhibitions
- Track exhibition details

## Database

The application uses SQLite for data storage. The database file (`gallery.db`) is automatically created in the `data/` directory on first run.

### Schema

- **artists**: Artist information (name, birth year, nationality, biography)
- **artworks**: Artwork details (title, artist, year, medium, dimensions, image path)
- **exhibitions**: Exhibition information (title, dates, location, description)
- **exhibition_artworks**: Many-to-many relationship between exhibitions and artworks
- **sales**: Sales records (artwork, date, price, buyer information)

## Development

### Adding New Features

The application follows a repository pattern with separation between data access (repositories) and UI components:

1. **Data layer**: Add methods to appropriate repository in `core/repositories/`
2. **UI layer**: Create or modify widgets/dialogs in `ui/widgets/` or `ui/dialogs/`
3. **Main window**: Connect new features in `ui/main_window.py`

### Code Organization

- **Core**: Business logic, database operations, data models
- **UI**: PyQt6-based user interface components
- **Separation of concerns**: UI doesn't directly access database; uses repositories

## Requirements

- Python 3.7+
- PyQt6 6.4.0+

## License

This project is provided as-is for art gallery management purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

*Prezzario temporanea // progetto ui gestionale*
