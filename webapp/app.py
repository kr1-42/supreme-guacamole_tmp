from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional

from flask import Flask, flash, g, redirect, render_template, request, send_from_directory, url_for

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.database import Database
from core.paths import DB_PATH, IMG_DIR, ensure_paths
from core.repositories.artist_repo import ArtistRepository
from core.repositories.artwork_repo import ArtworkRepository
from core.repositories.exhibition_repo import ExhibitionRepository
from core.repositories.sale_repo import SaleRepository
from core.schema import SCHEMA_SQL


STATUS_OPTIONS = ["available", "reserved", "sold"]


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-me"

    ensure_paths()
    init_database()

    @app.teardown_appcontext
    def close_db(exception: Exception | None = None):
        db: Optional[Database] = g.pop("db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        artist_repo, artwork_repo, exhibition_repo, sale_repo = get_repos()
        artist_count = len(artist_repo.get_all())
        artwork_count = len(artwork_repo.get_all())
        exhibition_count = len(exhibition_repo.get_all())
        sale_count = len(sale_repo.get_all())
        return render_template(
            "index.html",
            artist_count=artist_count,
            artwork_count=artwork_count,
            exhibition_count=exhibition_count,
            sale_count=sale_count,
        )

    @app.route("/artists", methods=["GET", "POST"])
    def artists():
        artist_repo, artwork_repo, _, _ = get_repos()
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            bio = request.form.get("bio", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            notes = request.form.get("notes", "").strip()
            if not name:
                flash("Name is required.", "error")
            else:
                artist_repo.create(name=name, bio=bio, email=email, phone=phone, notes=notes)
                flash("Artist created.", "success")
                return redirect(url_for("artists"))
        artists = artist_repo.get_all()
        return render_template("artists.html", artists=artists)

    @app.route("/artists/<int:artist_id>", methods=["GET", "POST"])
    def artist_detail(artist_id: int):
        artist_repo, artwork_repo, _, _ = get_repos()
        artist = artist_repo.get_by_id(artist_id)
        if artist is None:
            flash("Artist not found.", "error")
            return redirect(url_for("artists"))

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            bio = request.form.get("bio", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            notes = request.form.get("notes", "").strip()
            if not name:
                flash("Name is required.", "error")
            else:
                artist_repo.update(artist_id, name=name, bio=bio, email=email, phone=phone, notes=notes)
                flash("Artist updated.", "success")
                return redirect(url_for("artist_detail", artist_id=artist_id))

        artworks = artwork_repo.get_by_artist(artist_id)
        return render_template("artist_detail.html", artist=artist, artworks=artworks)

    @app.post("/artists/<int:artist_id>/delete")
    def artist_delete(artist_id: int):
        artist_repo, _, _, _ = get_repos()
        artist_repo.delete(artist_id)
        flash("Artist deleted.", "success")
        return redirect(url_for("artists"))

    @app.route("/artworks", methods=["GET", "POST"])
    def artworks():
        artist_repo, artwork_repo, _, _ = get_repos()
        if request.method == "POST":
            artist_id = to_int(request.form.get("artist_id"))
            code = request.form.get("code", "").strip() or None
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            art_type = request.form.get("type", "").strip()
            quantity = to_int(request.form.get("quantity")) or 1
            year = to_int(request.form.get("year"))
            price = to_float(request.form.get("price"))
            artist_cut_percent = to_float(request.form.get("artist_cut_percent")) or 10.0
            image = request.form.get("image", "").strip()
            status = request.form.get("status", "available")
            notes = request.form.get("notes", "").strip()

            if not title:
                flash("Title is required.", "error")
            else:
                artwork_repo.create(
                    artist_id=artist_id,
                    code=code,
                    title=title,
                    description=description,
                    type=art_type,
                    quantity=quantity,
                    year=year,
                    price=price,
                    artist_cut_percent=artist_cut_percent,
                    image=image,
                    status=status,
                    notes=notes,
                )
                flash("Artwork created.", "success")
                return redirect(url_for("artworks"))

        artworks = artwork_repo.get_all()
        artists = artist_repo.get_all()
        return render_template(
            "artworks.html",
            artworks=artworks,
            artists=artists,
            status_options=STATUS_OPTIONS,
        )

    @app.route("/artworks/<int:artwork_id>", methods=["GET", "POST"])
    def artwork_detail(artwork_id: int):
        artist_repo, artwork_repo, _, _ = get_repos()
        artwork = artwork_repo.get_by_id(artwork_id)
        if artwork is None:
            flash("Artwork not found.", "error")
            return redirect(url_for("artworks"))

        if request.method == "POST":
            artist_id = to_int(request.form.get("artist_id"))
            code = request.form.get("code", "").strip() or None
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            art_type = request.form.get("type", "").strip()
            quantity = to_int(request.form.get("quantity")) or 1
            year = to_int(request.form.get("year"))
            price = to_float(request.form.get("price"))
            artist_cut_percent = to_float(request.form.get("artist_cut_percent")) or 10.0
            image = request.form.get("image", "").strip()
            status = request.form.get("status", "available")
            notes = request.form.get("notes", "").strip()

            if not title:
                flash("Title is required.", "error")
            else:
                artwork_repo.update(
                    artwork_id=artwork_id,
                    artist_id=artist_id,
                    title=title,
                    code=code,
                    description=description,
                    type=art_type,
                    quantity=quantity,
                    year=year,
                    price=price,
                    artist_cut_percent=artist_cut_percent,
                    image=image,
                    status=status,
                    notes=notes,
                )
                flash("Artwork updated.", "success")
                return redirect(url_for("artwork_detail", artwork_id=artwork_id))

        artists = artist_repo.get_all()
        return render_template(
            "artwork_detail.html",
            artwork=artwork,
            artists=artists,
            status_options=STATUS_OPTIONS,
        )

    @app.post("/artworks/<int:artwork_id>/delete")
    def artwork_delete(artwork_id: int):
        _, artwork_repo, _, _ = get_repos()
        artwork_repo.delete(artwork_id)
        flash("Artwork deleted.", "success")
        return redirect(url_for("artworks"))

    @app.route("/exhibitions", methods=["GET", "POST"])
    def exhibitions():
        _, _, exhibition_repo, _ = get_repos()
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            location = request.form.get("location", "").strip()
            start_date = request.form.get("start_date", "").strip()
            end_date = request.form.get("end_date", "").strip()
            description = request.form.get("description", "").strip()
            if not name:
                flash("Name is required.", "error")
            else:
                exhibition_repo.create(
                    name=name,
                    location=location,
                    start_date=start_date,
                    end_date=end_date,
                    description=description,
                )
                flash("Exhibition created.", "success")
                return redirect(url_for("exhibitions"))

        exhibitions = exhibition_repo.get_all()
        return render_template("exhibitions.html", exhibitions=exhibitions)

    @app.route("/exhibitions/<int:exhibition_id>", methods=["GET", "POST"])
    def exhibition_detail(exhibition_id: int):
        _, artwork_repo, exhibition_repo, _ = get_repos()
        exhibition = exhibition_repo.get_by_id(exhibition_id)
        if exhibition is None:
            flash("Exhibition not found.", "error")
            return redirect(url_for("exhibitions"))

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            location = request.form.get("location", "").strip()
            start_date = request.form.get("start_date", "").strip()
            end_date = request.form.get("end_date", "").strip()
            description = request.form.get("description", "").strip()
            if not name:
                flash("Name is required.", "error")
            else:
                exhibition_repo.update(
                    exhibition_id=exhibition_id,
                    name=name,
                    location=location,
                    start_date=start_date,
                    end_date=end_date,
                    description=description,
                )
                flash("Exhibition updated.", "success")
                return redirect(url_for("exhibition_detail", exhibition_id=exhibition_id))

        exhibition_artworks = exhibition_repo.get_artworks(exhibition_id)
        artworks = artwork_repo.get_all()
        return render_template(
            "exhibition_detail.html",
            exhibition=exhibition,
            exhibition_artworks=exhibition_artworks,
            artworks=artworks,
        )

    @app.post("/exhibitions/<int:exhibition_id>/delete")
    def exhibition_delete(exhibition_id: int):
        _, _, exhibition_repo, _ = get_repos()
        exhibition_repo.delete(exhibition_id)
        flash("Exhibition deleted.", "success")
        return redirect(url_for("exhibitions"))

    @app.post("/exhibitions/<int:exhibition_id>/add_artwork")
    def exhibition_add_artwork(exhibition_id: int):
        _, _, exhibition_repo, _ = get_repos()
        artwork_id = to_int(request.form.get("artwork_id"))
        if artwork_id is None:
            flash("Select an artwork to add.", "error")
        else:
            exhibition_repo.add_artwork(exhibition_id, artwork_id)
            flash("Artwork added to exhibition.", "success")
        return redirect(url_for("exhibition_detail", exhibition_id=exhibition_id))

    @app.post("/exhibitions/<int:exhibition_id>/remove_artwork/<int:artwork_id>")
    def exhibition_remove_artwork(exhibition_id: int, artwork_id: int):
        _, _, exhibition_repo, _ = get_repos()
        exhibition_repo.remove_artwork(exhibition_id, artwork_id)
        flash("Artwork removed from exhibition.", "success")
        return redirect(url_for("exhibition_detail", exhibition_id=exhibition_id))

    @app.route("/sales", methods=["GET", "POST"])
    def sales():
        _, artwork_repo, _, sale_repo = get_repos()
        if request.method == "POST":
            artwork_id = to_int(request.form.get("artwork_id"))
            sale_date = request.form.get("sale_date", "").strip()
            sale_price = to_float(request.form.get("sale_price"))
            buyer_name = request.form.get("buyer_name", "").strip()
            payment_method = request.form.get("payment_method", "").strip()
            notes = request.form.get("notes", "").strip()
            if artwork_id is None or not sale_date or sale_price is None:
                flash("Artwork, sale date, and price are required.", "error")
            else:
                sale_repo.create(
                    artwork_id=artwork_id,
                    sale_date=sale_date,
                    sale_price=sale_price,
                    buyer_name=buyer_name,
                    payment_method=payment_method,
                    notes=notes,
                )
                flash("Sale created.", "success")
                return redirect(url_for("sales"))

        sales = sale_repo.get_all()
        artworks = artwork_repo.get_all()
        return render_template("sales.html", sales=sales, artworks=artworks)

    @app.route("/sales/<int:sale_id>", methods=["GET", "POST"])
    def sale_detail(sale_id: int):
        _, artwork_repo, _, sale_repo = get_repos()
        sale = sale_repo.get_by_id(sale_id)
        if sale is None:
            flash("Sale not found.", "error")
            return redirect(url_for("sales"))

        if request.method == "POST":
            artwork_id = to_int(request.form.get("artwork_id"))
            sale_date = request.form.get("sale_date", "").strip()
            sale_price = to_float(request.form.get("sale_price"))
            buyer_name = request.form.get("buyer_name", "").strip()
            payment_method = request.form.get("payment_method", "").strip()
            notes = request.form.get("notes", "").strip()
            if artwork_id is None or not sale_date or sale_price is None:
                flash("Artwork, sale date, and price are required.", "error")
            else:
                sale_repo.update(
                    sale_id=sale_id,
                    artwork_id=artwork_id,
                    sale_date=sale_date,
                    sale_price=sale_price,
                    buyer_name=buyer_name,
                    payment_method=payment_method,
                    notes=notes,
                )
                flash("Sale updated.", "success")
                return redirect(url_for("sale_detail", sale_id=sale_id))

        artworks = artwork_repo.get_all()
        return render_template("sale_detail.html", sale=sale, artworks=artworks)

    @app.post("/sales/<int:sale_id>/delete")
    def sale_delete(sale_id: int):
        _, _, _, sale_repo = get_repos()
        sale_repo.delete(sale_id)
        flash("Sale deleted.", "success")
        return redirect(url_for("sales"))

    @app.route("/images/<path:filename>")
    def artwork_image(filename: str):
        return send_from_directory(IMG_DIR, filename)

    return app


def init_database():
    if DB_PATH.exists():
        return
    db = Database(DB_PATH)
    db.executescript(SCHEMA_SQL)
    db.close()


def get_db() -> Database:
    db: Optional[Database] = g.get("db")
    if db is None:
        db = Database(DB_PATH)
        g.db = db
    return db


def get_repos():
    db = get_db()
    return (
        ArtistRepository(db),
        ArtworkRepository(db),
        ExhibitionRepository(db),
        SaleRepository(db),
    )


def to_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def to_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
