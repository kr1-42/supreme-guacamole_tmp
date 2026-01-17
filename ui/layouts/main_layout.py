from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
)

from ui.widgets.artist_list import ArtistListWidget
from ui.widgets.artwork_table import ArtworkTableWidget


def build_main_layout():
    """Build the main window layout and return (central_widget, refs_dict)."""
    central = QWidget()
    main_layout = QHBoxLayout()

    # Left: artists
    artist_list = ArtistListWidget()
    artist_list.setFixedWidth(250)
    artist_list.setMinimumHeight(150)

    # Middle/right: full-width artwork table + actions
    artwork_table = ArtworkTableWidget()
    artwork_count = QLabel("Artworks: 0")

    add_btn = QPushButton("aggiungi opera")
    edit_btn = QPushButton("Modifica")
    delete_btn = QPushButton("Elimina")
    
    # Make buttons larger
    for btn in [add_btn, edit_btn, delete_btn]:
        btn.setMinimumHeight(40)
        btn.setMinimumWidth(100)

    action_btns = QHBoxLayout()
    action_btns.addWidget(add_btn)
    action_btns.addWidget(edit_btn)
    action_btns.addWidget(delete_btn)

    center_panel = QVBoxLayout()
    center_panel.addWidget(artwork_count)
    center_panel.addLayout(action_btns)
    center_panel.addWidget(artwork_table, 1)
    center_panel.addStretch()

    main_layout.addWidget(artist_list)
    main_layout.addLayout(center_panel, 1)

    central.setLayout(main_layout)

    refs = {
        "artist_list": artist_list,
        "artwork_table": artwork_table,
        "artwork_count_label": artwork_count,
        "add_btn": add_btn,
        "edit_btn": edit_btn,
        "delete_btn": delete_btn,
    }
    return central, refs
