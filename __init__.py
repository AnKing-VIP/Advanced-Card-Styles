from aqt import mw, clayout
from aqt.clayout import CardLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# import the "show info" tool from utils.py
from aqt.utils import showInfo, downArrow
from anki.hooks import addHook, wrap
from functools import partial
from . import AdvancedStylerGui
from . import ProfileManager
from .Buttons import Buttons


class ProfileSelector():

    topCardLayout = QWidget()

    def afterInit(self, mw, note, ord=0, parent=None, addMode=False):
        global topCardLayout
        topCardLayout = self


        # advancedEditorButton = QPushButton(_("Advanced Editor"))
        # advancedEditorButton.setAutoDefault(False)
        # profileComboBox = QComboBox()
        # newLayout = QHBoxLayout()
        # newLayout.addWidget(advancedEditorButton)
        # newLayout.addStretch()
        # newLayout.addWidget(profileComboBox)
        buttons = Buttons(topCardLayout)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(buttons)

        self.tform.groupBox_3.layout().insertLayout(0, buttonsLayout)
        # advancedEditorButton.clicked.connect(partial(ProfileSelector.advancedEditorButtonAction, advancedEditorButton))

        pass

    # def advancedEditorButtonAction(button):

    #     cssBox = topCardLayout.findChild(QTextEdit, "css")
    #     a = AdvancedStylerGui.ASGUI()
    #     a.loadUI(cssBox, topCardLayout)

    #     pass

    pass


clayout.CardLayout.__init__ = wrap(clayout.CardLayout.__init__, ProfileSelector.afterInit)
