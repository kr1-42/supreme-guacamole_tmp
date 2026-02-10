<div align="center">

# 🎨 Art Catalog Manager

### Professional Desktop & Web Application for Art Gallery Management

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green.svg)](https://pypi.org/project/PyQt5/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey.svg)](https://flask.palletsprojects.com/)

A comprehensive solution for managing art catalogs, artists, artworks, exhibitions, and sales with both desktop and web interfaces.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## ✨ Features

### Core Functionality

- 👤 **Artist Management**: Comprehensive artist profiles with bio, contact information, and detailed notes
- 🖼️ **Artwork Catalog**: Complete artwork tracking with high-resolution images, descriptions, pricing, and status management
- 🎭 **Exhibition Planning**: Organize and manage exhibitions with artwork associations and timeline tracking
- 💰 **Sales Tracking**: Record sales transactions with automatic artist payment split calculations
- 📸 **Image Gallery**: Professional image preview and management system with zoom and navigation

### Technical Features

- 🖥️ **Desktop Application**: Native desktop interface built with PyQt5 for powerful local management
- 🌐 **Web Interface**: Modern Flask-based web UI for remote access and mobile compatibility
- 📊 **Live Database Viewer**: Real-time database access via Datasette with QR code sharing
- 💾 **SQLite Database**: Reliable, file-based database with automatic backup support
- 🎨 **Dark Theme**: Professional dark mode interface for reduced eye strain

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Desktop Application](#desktop-application)
  - [Web Application](#web-application)
- [Usage](#-usage)
  - [Desktop Application](#desktop-application-1)
  - [Web Application](#web-application-1)
  - [Live Database Viewer](#live-database-viewer-datasette)
- [Documentation](#-documentation)
- [Requirements](#-requirements)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🏗️ Project Structure

```
art-catalog-manager/
├── main.py                       # Desktop application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── webapp.md                     # Web application guide
│
├── core/                         # Core business logic
│   ├── database.py               # SQLite database wrapper
│   ├── schema.py                 # Database schema definition
│   ├── paths.py                  # Path configuration management
│   └── repositories/             # Data access layer
│       ├── artist_repo.py        # Artist data operations
│       ├── artwork_repo.py       # Artwork data operations
│       ├── exhibition_repo.py    # Exhibition data operations
│       └── sale_repo.py          # Sales data operations
│
├── ui/                           # Desktop user interface (PyQt5)
│   ├── main_window.py            # Main application window
│   ├── dialogs/                  # Dialog windows
│   │   ├── add_artist.py         # Artist creation dialog
│   │   ├── add_artwork.py        # Artwork creation dialog
│   │   └── add_exhibition.py     # Exhibition creation dialog
│   └── widgets/                  # Custom UI widgets
│       ├── artist_list.py        # Artist list widget
│       ├── artwork_table.py      # Artwork table widget
│       └── image_preview.py      # Image preview widget
│
├── webapp/                       # Web interface (Flask)
│   ├── app.py                    # Flask application
│   ├── templates/                # HTML templates
│   └── static/                   # Static assets (CSS, JS)
│
├── scripts/                      # Utility scripts
│   ├── serve_database.py         # Datasette server launcher
│   └── rename_images.py          # Image management utility
│
├── assets/                       # Application assets
│   └── icons/                    # Application icons
│
├── data/                         # Database storage (generated)
│   └── catalog.db                # SQLite database
│
├── images/                       # Image storage (generated)
│   └── artworks/                 # Artwork images
│
└── backups/                      # Database backups (generated)
```

## 📦 Installation

### Prerequisites

Before installing, ensure you have:

- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **pip** (Python package installer, included with Python)
- **Git** (for cloning the repository)

### Desktop Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kr1-42/supreme-guacamole_tmp.git
   cd supreme-guacamole_tmp
   ```

2. **Create and activate a virtual environment:**
   
   - On **Linux/macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   
   - On **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Web Application

The web application uses the same installation steps as above. See the [Web Application](#web-application-1) section for running instructions.

## 🚀 Usage

### Desktop Application

1. **Activate the virtual environment** (if not already activated):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **First-time setup:**
   - On first run, the application automatically creates:
     - `data/` directory for the database
     - `images/artworks/` directory for artwork images
     - `backups/` directory for database backups

### Web Application

1. **Start the Flask server:**
   ```bash
   python webapp/app.py
   ```

2. **Access the web interface:**
   - Open your browser and navigate to: `http://localhost:5000`

3. **Features available in web interface:**
   - Browse artists and artworks
   - View exhibitions and sales
   - Mobile-responsive design
   - Real-time data synchronization with desktop app

> **Note:** For detailed web application documentation, see [webapp.md](webapp.md)

### Live Database Viewer (Datasette)

You can share your database as a live, interactive spreadsheet accessible via QR code on any device connected to your network.

#### Quick Start

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Start the Datasette server:**
   ```bash
   python scripts/serve_database.py
   ```

3. **Server output example:**
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

4. **Access methods:**
   - **Local computer:** `http://localhost:8001`
   - **Mobile devices:** Scan the QR code (saved to `assets/qr_code.png`)
   - **Other devices:** Use the Network URL (e.g., `http://192.168.1.X:8001`)

#### Datasette Features

- 📊 Browse all tables (artists, artworks, exhibitions, sales)
- 🔍 Advanced search and filtering
- 📈 Sort and analyze data
- 💾 Export data as CSV or JSON
- 🔧 Run custom SQL queries
- 🔄 Real-time updates (refresh to see changes from main app)

#### Requirements

- All devices must be on the **same WiFi network**
- Server runs as long as the terminal is open
- Press `Ctrl+C` to stop the server

---

## 📚 Documentation

- **[webapp.md](webapp.md)** - Detailed web application setup and configuration
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing to the project
- **[LICENSE](LICENSE)** - Project license information

---

## 💻 Requirements

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Programming language |
| PyQt5 | 5.15+ | Desktop GUI framework |
| Flask | 2.3+ | Web framework |
| Datasette | 0.64.0+ | Database viewer |
| Pillow | 9.0.0+ | Image processing |
| qrcode | 7.4.0+ | QR code generation |

For a complete list of dependencies, see [requirements.txt](requirements.txt).

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: `ModuleNotFoundError` when running the application
**Solution:** Ensure the virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Issue: Port 5000 already in use (Web application)
**Solution:** Change the port in `webapp/app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

#### Issue: Database file not found
**Solution:** The database is created automatically on first run. If issues persist, manually create the `data/` directory:
```bash
mkdir -p data
```

#### Issue: PyQt5 installation fails
**Solution:** On Linux systems, you may need to install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebengine

# Fedora
sudo dnf install python3-qt5
```

### Getting Help

- 📝 Check existing [Issues](https://github.com/kr1-42/supreme-guacamole_tmp/issues)
- 💬 Open a [New Issue](https://github.com/kr1-42/supreme-guacamole_tmp/issues/new) for bug reports or feature requests
- 📧 Contact the maintainers for support

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code style and standards
- Submitting pull requests
- Reporting bugs
- Suggesting enhancements

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👏 Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the desktop interface
- Powered by [Flask](https://flask.palletsprojects.com/) for the web interface
- Database viewer using [Datasette](https://datasette.io/)
- Icons and assets from various open-source projects

---

<div align="center">

**[⬆ Back to Top](#-art-catalog-manager)**

Made with ❤️ for art enthusiasts and gallery managers

</div>
