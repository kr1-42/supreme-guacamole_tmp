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
    sell_btn = QPushButton("💰 VENDI")
    
    # Make buttons larger
    for btn in [add_btn, edit_btn, delete_btn]:
        btn.setMinimumHeight(40)
        btn.setMinimumWidth(100)
    
    # Sell button is bigger and styled
    sell_btn.setMinimumHeight(55)
    sell_btn.setMinimumWidth(150)
    sell_btn.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            border: none;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
    """)

    action_btns = QHBoxLayout()
    action_btns.addWidget(add_btn)
    action_btns.addWidget(edit_btn)
    action_btns.addWidget(delete_btn)
    action_btns.addWidget(sell_btn)

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
        "sell_btn": sell_btn,
    }
    return central, refs
