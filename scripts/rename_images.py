#!/usr/bin/env python3
"""
Script to rename artwork images to match their titles.
Run this script to rename all images in the images/artworks folder
to match the artwork title in the database.
"""

import re
import sqlite3
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "catalog.db"
IMG_DIR = PROJECT_ROOT / "images" / "artworks"


def sanitize_filename(name: str) -> str:
    """Convert a title to a safe filename."""
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Remove multiple underscores
    name = re.sub(r'_+', '_', name)
    # Limit length
    name = name[:100]
    return name.strip('_')


def rename_images():
    """Rename all artwork images to match their titles."""
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all artworks with images
    cursor.execute("SELECT id, title, image FROM artwork WHERE image IS NOT NULL AND image != ''")
    artworks = cursor.fetchall()

    renamed_count = 0
    skipped_count = 0
    error_count = 0

    for artwork in artworks:
        artwork_id = artwork['id']
        title = artwork['title'] or f"artwork_{artwork_id}"
        old_image = artwork['image']

        if not old_image:
            continue

        old_path = IMG_DIR / old_image
        if not old_path.exists():
            print(f"[SKIP] Image not found: {old_image}")
            skipped_count += 1
            continue

        # Get file extension
        extension = old_path.suffix.lower()

        # Create new filename from title
        safe_title = sanitize_filename(title)
        new_filename = f"{safe_title}{extension}"
        new_path = IMG_DIR / new_filename

        # Handle duplicates by adding a number
        counter = 1
        while new_path.exists() and new_path != old_path:
            new_filename = f"{safe_title}_{counter}{extension}"
            new_path = IMG_DIR / new_filename
            counter += 1

        if new_path == old_path:
            print(f"[SKIP] Already named correctly: {old_image}")
            skipped_count += 1
            continue

        try:
            # Rename the file
            old_path.rename(new_path)
            
            # Update the database
            cursor.execute(
                "UPDATE artwork SET image = ? WHERE id = ?",
                (new_filename, artwork_id)
            )
            conn.commit()
            
            print(f"[OK] Renamed: {old_image} -> {new_filename}")
            renamed_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to rename {old_image}: {e}")
            error_count += 1

    conn.close()

    print("\n" + "=" * 50)
    print(f"Renamed: {renamed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print("=" * 50)


if __name__ == "__main__":
    print("Renaming artwork images to match titles...")
    print(f"Database: {DB_PATH}")
    print(f"Images directory: {IMG_DIR}")
    print("=" * 50)
    rename_images()
