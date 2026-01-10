"""Path utilities for the art gallery management system."""

import os
from pathlib import Path


def get_app_dir():
    """Get the application root directory."""
    return Path(__file__).parent.parent


def get_data_dir():
    """Get the data directory for storing the database."""
    data_dir = get_app_dir() / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def get_database_path():
    """Get the path to the SQLite database file."""
    return get_data_dir() / "gallery.db"


def get_assets_dir():
    """Get the assets directory."""
    return get_app_dir() / "assets"


def get_icons_dir():
    """Get the icons directory."""
    icons_dir = get_assets_dir() / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    return icons_dir
