import os
import re
from functools import partial
from pathlib import Path

from aqt.clayout import CardLayout
from PyQt5.Qt import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from . import AdvancedStylerGui, ProfileManager


class Buttons(QWidget):

    def __init__(self, clayout: CardLayout):
        super().__init__()
        self.clayout = clayout
        self.initalizeUI()

    # initialize ui
    def initalizeUI(self):
        advancedEditorButton = QPushButton("Advanced Editor")
        saveButton = QPushButton("Save Style") 

        menuButton = QPushButton('...', self)
        menuButton.setFixedWidth(35)

        menu = QMenu(self)
        importAction = menu.addAction("Import")
        exportAction = menu.addAction("Export")
        menuButton.setMenu(menu)

        profileComboBox = self.profileComboBox = QComboBox()
        newLayout = QHBoxLayout()

        newLayout.addWidget(advancedEditorButton)
        newLayout.addWidget(profileComboBox)
        newLayout.addWidget(saveButton)
        newLayout.addWidget(menuButton)

        self.loadProfilesIntoCombobox()

        currentProfile, _ = self.getCurrentProfileNameAndSaveStatus()

        if profileComboBox.findText(currentProfile) != -1:
            profileComboBox.setCurrentText(currentProfile)
        else:
            profileComboBox.addItem(currentProfile)
            profileComboBox.setCurrentText(currentProfile)

        importAction.triggered.connect(self.getExportConfig)
        exportAction.triggered.connect(self.importAndUpdateProfile)
        advancedEditorButton.clicked.connect(self.advancedEditorButtonAction)
        saveButton.clicked.connect(self.getNameAndSave)
        profileComboBox.currentTextChanged.connect(
            lambda: self.loadSelectedProfile(ask_user=True))

        self.setLayout(newLayout)

    # importing / exporting / applying profiles
    def getNameAndSave(self):
        profilename, _ = self.getCurrentProfileNameAndSaveStatus()

        nameWindow = self.nameWindow = QWidget()
        nameText = self.nameText = QLineEdit()
        nameWindow.setWindowTitle('Profile Name')
        nameWindow.setWindowIcon(self.clayout.windowIcon())
        okButton = QPushButton('Save')
        label = QLabel('Please select a profile name :')
        vlayout = QVBoxLayout()

        labelLayout = QHBoxLayout()
        labelLayout.addWidget(label)
        labelLayout.addStretch()
        vlayout.addLayout(labelLayout)

        hlayout = QHBoxLayout()
        vlayout.addWidget(nameText)
        hlayout.addStretch()
        hlayout.addWidget(okButton)
        vlayout.addLayout(hlayout)

        nameWindow.setLayout(vlayout)
        nameWindow.setWindowModality(Qt.ApplicationModal)
        nameWindow.show()
        nameText.setText(profilename)
        nameText.setFocus()

        nameText.returnPressed.connect(
            partial(self.saveProfile, self.nameText))
        nameText.returnPressed.connect(nameWindow.close)
        okButton.clicked.connect(partial(self.saveProfile, self.nameText))
        okButton.clicked.connect(nameWindow.close)

    def saveProfile(self, nametxt, withFrontAndBack=True):
        print('-' + nametxt.text() + '-')
        cssTextWithConfigs = self.insertOrChangeConfigs(
            self.clayout.model['css'], nametxt.text(), self.Saved)

        ProfileManager.saveProfile(
            nametxt.text(), cssTextWithConfigs, self.front, self.back)
        self.updateComboBox(nametxt.text(), forceUpdate=True)

    def importAndUpdateProfile(self):
        a = ProfileManager.importProfile()
        self.updateComboBox(a)

    def loadSelectedProfile(self, ask_user=False):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        basepath = Path(dir_path) / 'user_files' / \
            self.profileComboBox.currentText()

        if (basepath / 'css.css').exists():
            with open(str(basepath / 'css.css'), 'r') as file:
                css = file.read()
                self.clayout.model['css'] = css

        if (basepath / 'front.txt').exists() or (basepath / 'back.txt').exists():
            if ask_user:
                reply = QMessageBox.question(self, 'CAUTION', 'The selected profile has \'Front\' and/or \'Back\' templates.\
                                                    \nAre you sure you want to import them?\
                                                    \nPlease make sure you are choosing the CORRECT CARD TYPE (basic/cloze)\
                                                    \n(Only do this if you know what you are doing)\
                                                    \n\
                                                    \nYes = Import CSS + Front + Back\
                                                    \nNo = Import CSS only.',
                                                   QMessageBox.Yes, QMessageBox.No)

            if not ask_user or reply == QMessageBox.Yes:
                if (basepath / 'front.txt').exists():
                    with open(str(basepath / 'front.txt'), 'r') as fileF:
                        self.front = fileF.read()
                if (basepath / 'back.txt').exists():
                    with open(str(basepath / 'back.txt'), 'r') as fileB:
                        self.back = fileB.read()

        self.clayout.change_tracker.mark_basic()
        self.clayout.update_current_ordinal_and_redraw(self.clayout.ord)

    def getCurrentProfileNameAndSaveStatus(self):
        cssText = self.clayout.model['css']

        signalString = cssText[:11]
        profileConfigs = None
        if signalString == '/* Profile:':
            endOfNameIndex = cssText.find('*/')
            if endOfNameIndex != -1:
                profileConfigs = cssText[2:2 + endOfNameIndex]

                configList = profileConfigs.split('||')

                profileName = configList[0].split(':')[1].strip()
                saveStatus = configList[1].split(':')[1].strip()

                return profileName, saveStatus

        else:
            return 'Custom Profile', 'Not saved'

    # configs
    def insertOrChangeConfigs(self, cssText, profileName, saveStatus):
        signalString = cssText[:11]
        if signalString == '/* Profile:':
            endOfNameIndex = cssText.find('*/')
            if endOfNameIndex != -1:
                newCss = cssText[endOfNameIndex + 3:]
                return '/* Profile: {} || Satus: {} */ \n'.format(profileName, saveStatus) + newCss

        else:
            return '/* Profile: {} || Satus: {} */ \n'.format(profileName, saveStatus) + cssText

    def getExportConfig(self):
        exportConfigWindow = self.exportConfigWindow = QWidget()

        okButton = QPushButton('Export')

        includeAllCBox = self.includeAllCBox = QCheckBox(
            'Include \'Front\' and \'Back\' html (USE WITH CAUTION!)')

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        vlayout.addWidget(includeAllCBox)
        hlayout.addStretch()
        hlayout.addWidget(okButton)
        vlayout.addLayout(hlayout)

        exportConfigWindow.setLayout(vlayout)
        exportConfigWindow.setWindowModality(Qt.ApplicationModal)
        exportConfigWindow.show()
        exportConfigWindow.setFocus()

        okButton.clicked.connect(partial(
            ProfileManager.exportProfile, self.profileComboBox, self.includeAllCBox))
        okButton.clicked.connect(exportConfigWindow.close)

    # profile combobox
    def updateComboBox(self, preferedProfile=None, forceUpdate=False):
        if preferedProfile != None:
            self.profileComboBox.addItem(preferedProfile)
            self.profileComboBox.setCurrentText(preferedProfile)
        else:
            selected = self.profileComboBox.currentText()
            self.profileComboBox.clear()
            self.loadProfilesIntoCombobox()
            self.profileComboBox.setCurrentText(selected)

        if forceUpdate:
            self.loadSelectedProfile()
            
    def loadProfilesIntoCombobox(self):
        available_profiles = ProfileManager.getAvailableProfiles()
        
        # sort by text in brackets (e.g. [Cloze])
        def sort(x):
            m = re.search('\[[a-zA-Z-_]+\]', x)
            if m:
                return m.group(0) + x
            else:
                return x

        available_profiles = sorted(available_profiles, key=sort)
        self.profileComboBox.addItems(available_profiles)

    # reading / writing current template front and back
    @property
    def front(self):
        return self.clayout.templates[self.clayout.ord]['qfmt']

    @front.setter
    def front(self, value):
        self.clayout.templates[self.clayout.ord]['qfmt'] = value

    @property
    def back(self):
        return self.clayout.templates[self.clayout.ord]['afmt']

    @back.setter
    def back(self, value):
        self.clayout.templates[self.clayout.ord]['afmt'] = value

    # launch advanced editor
    def advancedEditorButtonAction(self):
        a = AdvancedStylerGui.ASGUI()
        a.loadUI(self.clayout)

    @property
    def Saved(self):
        return 'Saved'

    @property
    def NotSaved(self):
        return 'Not Saved'
