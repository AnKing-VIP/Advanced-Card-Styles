from aqt.gui_hooks import card_layout_will_show
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .Buttons import Buttons


def add_buttons_to_layout(clayout):
    buttons = Buttons(clayout)

    buttonsLayout = QHBoxLayout()
    buttonsLayout.addWidget(buttons)
    buttonsLayout.setContentsMargins(0, 0, 0, 0)

    groupbox = QGroupBox()
    groupbox.setLayout(buttonsLayout)
    groupbox.setContentsMargins(0, 0, 0, 0)

    clayout.buttons.insertWidget(1, groupbox)


card_layout_will_show.append(add_buttons_to_layout)
