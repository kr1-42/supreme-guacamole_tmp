# Webapp (Local Run Guide)

## Overview
The webapp is a Flask UI that uses the same database and image folders as the Python app. It runs on port 5000 by default and serves the templates and static assets from the `webapp/` folder.

## Prerequisites
- Python 3.10+ recommended
- pip

## Setup
From the project root:

1) Create and activate a virtual environment
- Linux/macOS:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
- Windows (PowerShell):
  - `python -m venv .venv`
  - `.venv\Scripts\Activate.ps1`

2) Install dependencies
- `pip install -r requirements.txt`

## Run the webapp
From the project root:

- `python webapp/app.py`

Then open:
- `http://localhost:5000`

## What happens on first run
- The database path and image folders are created if missing.
- The schema is initialized automatically.

## Data locations
- Database file: `data/` (created via `core/paths.py`)
- Artwork images: `images/artworks/`

## Notes
- The Flask `SECRET_KEY` is currently set in `webapp/app.py`. Change it if you expose the app outside your machine.
- If port 5000 is in use, edit the port in `webapp/app.py` and restart.
