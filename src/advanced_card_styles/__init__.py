from aqt.gui_hooks import card_layout_will_show
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .Buttons import Buttons


def add_buttons_to_layout(clayout):
    buttonsLayout = QHBoxLayout()
    buttons = Buttons(clayout)
    buttonsLayout.addWidget(buttons)

    clayout.buttons.insertLayout(1, buttonsLayout)


card_layout_will_show.append(add_buttons_to_layout)
