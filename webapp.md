# 🌐 Web Application Guide

## Overview

The Art Catalog Manager Web Application is a Flask-based interface that provides remote access to your art catalog database. It uses the same SQLite database and image folders as the desktop application, ensuring seamless data synchronization between both interfaces.

### Key Features

- 📱 **Mobile-Responsive Design**: Access your catalog from any device
- 🔄 **Real-Time Synchronization**: Shares data with the desktop application
- 🌐 **Network Access**: Available to all devices on your local network
- 🎨 **Modern Interface**: Clean and intuitive web UI
- 💾 **Same Database**: Uses the same SQLite database as the desktop app

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before running the web application, ensure you have:

- **Python 3.8+** (Python 3.10+ recommended for best compatibility)
- **pip** (Python package installer)
- A virtual environment (recommended)

---

## Setup

### 1. Create and Activate Virtual Environment

Choose your operating system:

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### Windows (PowerShell)
```powershell
python -m venv venv
.venv\Scripts\Activate.ps1
```

> **Note:** If you encounter a PowerShell execution policy error, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 2. Install Dependencies

From the project root directory:

```bash
pip install -r requirements.txt
```

This will install:
- Flask 2.3+
- PyQt5 (for desktop app compatibility)
- Pillow (image processing)
- Other required dependencies

---

## Running the Application

### Quick Start

1. **Ensure you're in the project root directory:**
   ```bash
   cd /path/to/supreme-guacamole_tmp
   ```

2. **Activate the virtual environment** (if not already activated):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Start the Flask server:**
   ```bash
   python webapp/app.py
   ```

4. **Access the application:**
   - Open your browser and navigate to: **`http://localhost:5000`**
   - Or use your computer's IP address for network access: **`http://YOUR_IP:5000`**

### What Happens on First Run

On the first run, the application automatically:

1. ✅ Creates the `data/` directory for the database
2. ✅ Creates the `images/artworks/` directory for artwork images
3. ✅ Initializes the SQLite database with the required schema
4. ✅ Sets up all necessary database tables

### Server Output

You should see output similar to:

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.X:5000
Press CTRL+C to quit
```

---

## Configuration

### Port Configuration

By default, the web application runs on **port 5000**. To change the port:

1. Open `webapp/app.py`
2. Locate the following line at the bottom of the file:
   ```python
   app.run(host='0.0.0.0', port=5000, debug=True)
   ```
3. Change the port number:
   ```python
   app.run(host='0.0.0.0', port=8080, debug=True)  # Changed to 8080
   ```
4. Save and restart the server

### Security Configuration

#### Secret Key

The Flask application uses a `SECRET_KEY` for session management. The default key is set in `webapp/app.py`:

```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

⚠️ **Important Security Note:**
- The default secret key is for development only
- **Change this key** if you plan to expose the application outside your local machine
- Use a strong, random secret key in production

To generate a secure secret key:

```python
import secrets
print(secrets.token_hex(32))
```

#### Debug Mode

Debug mode is enabled by default for development:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

⚠️ **For production use:**
- Set `debug=False`
- Use a proper WSGI server (e.g., Gunicorn, uWSGI)
- Configure a reverse proxy (e.g., Nginx, Apache)

---

## Architecture

### File Structure

```
webapp/
├── app.py              # Main Flask application
├── templates/          # HTML templates (Jinja2)
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── artists.html    # Artist list
│   ├── artworks.html   # Artwork catalog
│   └── ...
└── static/             # Static assets
    ├── css/            # Stylesheets
    ├── js/             # JavaScript files
    └── images/         # Static images
```

### Data Locations

The web application accesses the same data as the desktop application:

| Data Type | Location | Purpose |
|-----------|----------|---------|
| Database | `data/catalog.db` | SQLite database file |
| Artwork Images | `images/artworks/` | Uploaded artwork images |
| Backups | `backups/` | Automatic database backups |

### Database Schema

The application uses the same schema as the desktop app, defined in `core/schema.py`:

- **artists** - Artist profiles and information
- **artworks** - Artwork catalog and metadata
- **exhibitions** - Exhibition planning and tracking
- **sales** - Sales transactions and payments

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Port 5000 Already in Use

**Error Message:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
1. Change the port in `webapp/app.py` (see [Port Configuration](#port-configuration))
2. Or stop the process using port 5000:
   ```bash
   # Find the process
   lsof -i :5000  # On macOS/Linux
   netstat -ano | findstr :5000  # On Windows
   
   # Kill the process
   kill -9 <PID>  # On macOS/Linux
   taskkill /PID <PID> /F  # On Windows
   ```

#### Issue: ModuleNotFoundError

**Error Message:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
Ensure the virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Issue: Database Not Found

**Error Message:**
```
Database file not found at data/catalog.db
```

**Solution:**
The database is created automatically on first run. If the issue persists:
```bash
# Ensure you're in the project root directory
pwd  # Should show .../supreme-guacamole_tmp

# Create the data directory manually if needed
mkdir -p data

# Run the desktop app first to initialize the database
python main.py
```

#### Issue: Cannot Access from Other Devices

**Symptoms:**
- Can access via `localhost:5000` but not from other devices
- Network URL not working

**Solution:**
1. Ensure `host='0.0.0.0'` in `app.run()` (already set by default)
2. Check your firewall settings:
   - Allow incoming connections on port 5000
   - On Windows: Windows Defender Firewall → Allow an app
   - On macOS: System Preferences → Security & Privacy → Firewall
3. Ensure all devices are on the same network
4. Find your IP address:
   ```bash
   # Linux/macOS
   ifconfig | grep inet
   
   # Windows
   ipconfig
   ```

#### Issue: Images Not Displaying

**Symptoms:**
- Artwork images show broken image icons
- Images work in desktop app but not web app

**Solution:**
1. Check that images are in the correct directory: `images/artworks/`
2. Verify file permissions:
   ```bash
   chmod -R 755 images/  # On Linux/macOS
   ```
3. Check the image file paths in the database
4. Ensure image files have supported extensions (`.jpg`, `.png`, `.gif`)

---

## Production Deployment

For production deployment, consider:

### Using a Production WSGI Server

Replace the development server with Gunicorn or uWSGI:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 webapp.app:app
```

### Using a Reverse Proxy

Configure Nginx or Apache as a reverse proxy:

**Nginx Example:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Security Checklist

- [ ] Change the `SECRET_KEY` to a secure random value
- [ ] Set `debug=False` in production
- [ ] Use HTTPS with SSL certificates
- [ ] Implement user authentication if needed
- [ ] Configure proper firewall rules
- [ ] Regular security updates for dependencies

---

## Additional Resources

- **Flask Documentation**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **Flask Security Best Practices**: [https://flask.palletsprojects.com/en/latest/security/](https://flask.palletsprojects.com/en/latest/security/)
- **Deployment Options**: [https://flask.palletsprojects.com/en/latest/deploying/](https://flask.palletsprojects.com/en/latest/deploying/)

---

## Getting Help

If you encounter issues not covered here:

1. 📝 Check the main [README.md](README.md) for general troubleshooting
2. 🔍 Search existing [GitHub Issues](https://github.com/kr1-42/supreme-guacamole_tmp/issues)
3. 💬 Open a [New Issue](https://github.com/kr1-42/supreme-guacamole_tmp/issues/new) with:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages or logs
   - Your environment (OS, Python version, etc.)

---

<div align="center">

**[⬆ Back to Main Documentation](README.md)**

</div>
