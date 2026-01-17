#!/usr/bin/env python3
"""
Serve the Art Catalog database via Datasette with QR code access.

Usage:
    python scripts/serve_database.py [--public]

Options:
    --public    Use ngrok to create a public URL (requires ngrok installed)
"""

import subprocess
import sys
import socket
import qrcode
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.paths import DB_PATH, APP_DIR


def get_local_ip():
    """Get the local IP address for LAN access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_qr_code(url: str, output_path: Path = None):
    """Generate and display a QR code for the given URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Print ASCII QR code to terminal
    qr.print_ascii(invert=True)
    
    # Save as image if path provided
    if output_path:
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        print(f"\n📱 QR code saved to: {output_path}")


def main():
    if not DB_PATH.exists():
        print(f"❌ Database not found at: {DB_PATH}")
        print("   Run the main application first to create the database.")
        sys.exit(1)
    
    host = "0.0.0.0"  # Listen on all interfaces
    port = 8001
    local_ip = get_local_ip()
    
    url = f"http://{local_ip}:{port}"
    
    print("=" * 60)
    print("🎨 Art Catalog - Live Database Viewer")
    print("=" * 60)
    print(f"\n📂 Database: {DB_PATH}")
    print(f"\n🌐 Access URLs:")
    print(f"   Local:   http://localhost:{port}")
    print(f"   Network: {url}")
    print(f"\n📱 Scan this QR code to access from your phone:\n")
    
    # Generate QR code
    qr_path = APP_DIR / "assets" / "qr_code.png"
    qr_path.parent.mkdir(parents=True, exist_ok=True)
    generate_qr_code(url, qr_path)
    
    print(f"\n🔗 URL: {url}")
    print("\n" + "=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    # Run datasette
    try:
        subprocess.run([
            sys.executable, "-m", "datasette",
            str(DB_PATH),
            "--host", host,
            "--port", str(port),
            "--setting", "sql_time_limit_ms", "5000",
            "--setting", "default_page_size", "50",
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped.")


if __name__ == "__main__":
    main()
