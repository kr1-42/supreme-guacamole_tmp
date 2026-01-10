"""Core package for the art gallery management system."""

from .database import Database
from .schema import ALL_TABLES
from .paths import get_app_dir, get_data_dir, get_database_path, get_assets_dir, get_icons_dir

__all__ = [
    'Database',
    'ALL_TABLES',
    'get_app_dir',
    'get_data_dir',
    'get_database_path',
    'get_assets_dir',
    'get_icons_dir',
]
