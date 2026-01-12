from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)

from ui.widgets.artist_list import ArtistListWidget
from ui.widgets.artwork_table import ArtworkTableWidget
from ui.widgets.image_carousel import ImageCarousel


def build_main_layout():
    """Build the main window layout and return (central_widget, refs_dict)."""
    central = QWidget()
    main_layout = QHBoxLayout()

    # Left: artists
    artist_list = ArtistListWidget()
    artist_list.setFixedWidth(250)

    # Middle/right: table + preview + actions
    artwork_table = ArtworkTableWidget()
    preview = ImageCarousel()

    add_btn = QPushButton("Add")
    edit_btn = QPushButton("Edit")
    delete_btn = QPushButton("Delete")

    action_btns = QHBoxLayout()
    action_btns.addWidget(add_btn)
    action_btns.addWidget(edit_btn)
    action_btns.addWidget(delete_btn)

    center_panel = QVBoxLayout()
    center_panel.addWidget(artwork_table, 1)
    center_panel.addWidget(preview, 3)
    center_panel.addLayout(action_btns)
    center_panel.addStretch()

    main_layout.addWidget(artist_list)
    main_layout.addLayout(center_panel, 1)

    central.setLayout(main_layout)

    refs = {
        "artist_list": artist_list,
        "artwork_table": artwork_table,
        "preview": preview,
        "add_btn": add_btn,
        "edit_btn": edit_btn,
        "delete_btn": delete_btn,
    }
    return central, refs
