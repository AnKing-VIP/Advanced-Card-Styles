import sys
from aqt import mw, clayout
from aqt.utils import showInfo, downArrow
from .myCssParser import *
from . import AdvancedStylerUI
from .CssProfile import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from functools import partial


# Next Steps:
# 1 - Fix messagebox
# 2 - Add Profile Detection

class ASGUI():

    profile = clayout.profile = CssProfile()
    memoryBackedUpCssProfileText = ''
    # memoryBackedUpCssProfileText = clayout.memoryBackedUpCssProfileText = ''
    window = clayout.window = AdvancedStylerUI.Ui_Form()
    # cssBoxx = clayout.cssBoxx = QTextEdit()
    # topCardLayout = QWidget()
    some = clayout.some = QWidget()


    def loadUI(self, cssBox, parentUI):
        self.window.setupUi(self.some)
        # someB = QPushButton('Test')
        # someL = QVBoxLayout()
        # someL.addWidget(some)
        # someL.addWidget(someB)

        self.topCardLayout = parentUI

        self.cardWidthButtonGroup = clayout.cardWidthButtonGroup = QButtonGroup()
        self.cardWidthButtonGroup.addButton(self.window.cardWidthPercetRadioButton)
        self.cardWidthButtonGroup.addButton(self.window.cardWidthPixelRadioButton)


        self.cardMarginButtonGroup = clayout.cardMarginButtonGroup = QButtonGroup()
        self.cardMarginButtonGroup.addButton(self.window.cardMarginCenterRadio)
        self.cardMarginButtonGroup.addButton(self.window.cardMarginCustomRadio)


        self.imgWidthButtonGroup = clayout.imgWidthButtonGroup = QButtonGroup()
        self.imgWidthButtonGroup.addButton(self.window.imgWidthPercetRadioButton)
        self.imgWidthButtonGroup.addButton(self.window.imgWidthPixelRadioButton)

        self.imgHeightButtonGroup = clayout.imgHeightButtonGroup = QButtonGroup()
        self.imgHeightButtonGroup.addButton(self.window.imgHeightPercetRadioButton)
        self.imgHeightButtonGroup.addButton(self.window.imgHeightPixelRadioButton)

        self.imgShadowButtonGroup = clayout.imgShadowButtonGroup = QButtonGroup()
        self.imgShadowButtonGroup.addButton(self.window.imgShadowDropRadioButton)
        self.imgShadowButtonGroup.addButton(self.window.imgShadowGlowRadioButton)

        self.some.setWindowIcon(self.topCardLayout.windowIcon())

        self.some.setWindowModality(Qt.ApplicationModal)
        self.some.show()
        # take the focus away from the first input area when starting up,
        # as users tend to accidentally type into the template
        self.cssBoxx = cssBox
        text = self.cssBoxx.toPlainText()
        self.loadSettingsFromCss(text)
        self.memoryBackedUpCssProfileText = text

        self.connectButtonsAndTextboxes()
        self.unifiedUpdateAction()

        self.some.setFocus()
        pass


    def loadSettingsFromCss(self, filePath):

        self.profile.initializeFromCssString(filePath, "Custom")
        # showInfo('after initializeFromCssString')
        for rule in self.profile.ruleNamesList:
            attributes = self.profile.getDeclarationsDictFromRule(rule)

            # showInfo('rule = ' + rule)
            # showInfo('After getDeclarationsDictFromRule')

            if attributes is None:
                continue

            if rule.strip(' ') == '.card':
                if 'font-family' in attributes:
                    self.window.fontComboBox.setCurrentText(attributes['font-family'])
                if 'font-size' in attributes:
                    self.window.sizeSpinBox.setValue(int(str(attributes['font-size'])[:len(attributes['font-size']) - 2]))
                if 'text-align' in attributes:
                    if attributes['text-align'] == 'left':
                        self.window.alignLeft.setChecked(True)
                    if attributes['text-align'] == 'center':
                        self.window.alignCenter.setChecked(True)
                    if attributes['text-align'] == 'right':
                        self.window.alignRight.setChecked(True)
                if 'color' in attributes:
                    self.window.cardTextColor.setText(attributes['color'])
                    self.window.cardTextColor.setStyleSheet("QWidget { background-color: " + attributes['color'] + '}')

                if 'background-color' in attributes:
                    self.window.cardBGColor.setText(attributes['background-color'])
                    self.window.cardBGColor.setStyleSheet("QWidget { background-color: " + attributes['background-color'] + '}')

                if 'max-width' in attributes and attributes['max-width'] is not 'none':
                    att = attributes['max-width'].strip(' ')
                    self.window.enableCardMaxWidth.setChecked(True)
                    if '%' in att:
                        self.window.cardWidthPerectSpinBox.setValue(int(att[:len(att) - 1]))
                        self.window.cardWidthPercetRadioButton.setChecked(True)
                    if 'px' in att:
                        self.window.cardWidthPixelSpinBox.setValue(int(att[:len(att) - 2]))
                        self.window.cardWidthPixelRadioButton.setChecked(True)

                if 'margin' in attributes and attributes['margin'] is not 'none':
                    self.window.enableCardMargin.setChecked(True)
                    att = attributes['margin'].strip(' ')
                    if att == '20px auto':
                        self.window.cardMarginCenterRadio.setChecked(True)
                    else:
                        self.window.cardMarginCustomRadio.setChecked(True)
                        self.window.cardMarginCustom.setText(att)

                if 'word-wrap' in attributes and attributes['word-wrap'] is 'break-word':
                    self.window.cardWordWrapCheckBox.setChecked(True)

            if rule.strip(' ') == 'b':
                self.window.enableBold.setChecked(True)
                if 'color' in attributes:
                    self.window.boldTextColor.setText(attributes['color'])
                    self.window.boldTextColor.setStyleSheet("QWidget { background-color: " + attributes['color'] + '}')

                # because bold already has bold, boldBoldCBOX will be checked by default unless font-weight is normal   font-weight: bold;
                if 'font-weight' not in attributes or attributes['font-weight'] != 'normal':
                    self.window.boldBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] == 'italic':
                    self.window.boldItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.window.boldUnderlinedBox.setChecked(True)

            if rule.strip(' ') == 'i':
                self.window.enableItalics.setChecked(True)
                if 'color' in attributes:
                    self.window.italicsTextColor.setText(attributes['color'])
                    self.window.italicsTextColor.setStyleSheet("QWidget { background-color: " + attributes['color'] + '}')

                # because bold already has bold, boldBoldCBOX will be checked by default unless font-weight is normal   font-weight: bold;
                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.window.italicsBoldCBOX.setChecked(True)
                if 'font-style' not in attributes or attributes['font-style'] != 'normal':
                    self.window.italicsItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.window.italicsUnderlinedBox.setChecked(True)

            if rule.strip(' ') == 'u':
                self.window.enableUnderlined.setChecked(True)
                if 'color' in attributes:
                    self.window.underlinedTextColor.setText(attributes['color'])
                    self.window.underlinedTextColor.setStyleSheet("QWidget { background-color: " + attributes['color'] + '}')

                # because bold already has bold, boldBoldCBOX will be checked by default unless font-weight is normal   font-weight: bold;
                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.window.underlinedBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] != 'italic':
                    self.window.underlinedItalicBox.setChecked(True)
                if 'text-decoration' not in attributes or attributes['text-decoration'] != 'none':
                    self.window.underlinedUnderlinedBox.setChecked(True)


            if rule.strip(' ') == 'a':
                self.window.enableLinks.setChecked(True)
                if 'color' in attributes:
                    self.window.linksTextColor.setText(attributes['color'])
                    self.window.linksTextColor.setStyleSheet("QWidget { background-color: " + attributes['color'] + '}')

                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.window.linksBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] == 'italic':
                    self.window.linksItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.window.linksUnderlinedBox.setChecked(True)

            if rule.strip(' ') == '.cloze':
                self.window.clozeGroupBox.setChecked(True)
                if 'color' in attributes:
                    self.window.clozeTextColor.setText(attributes['color'])
                    self.window.clozeTextColor.setStyleSheet("QWidget { background-color: " + attributes['color'] + '}')

                if 'background-color' in attributes:
                    self.window.clozeBGColor.setText(attributes['background-color'])
                    self.window.clozeBGColor.setStyleSheet("QWidget { background-color: " + attributes['background-color'] + '}')

                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.window.clozeBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] == 'italic':
                    self.window.clozeItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.window.clozeUnderlinedBox.setChecked(True)
                if 'font-size' in attributes:
                    self.window.clozeSizeSpinBox.setValue(int(str(attributes['font-size'])[:len(attributes['font-size']) - 2]))

            if rule.strip(' ') == '#extra':
                self.window.extraGroupBox.setChecked(True)
                if 'color' in attributes:
                    self.window.extraTextColor.setText(attributes['color'])
                    self.window.extraTextColor.setStyleSheet("QWidget { background-color: " + attributes['color'] + '}')

                if 'background-color' in attributes:
                    self.window.extraBGColor.setText(attributes['background-color'])
                    self.window.extraBGColor.setStyleSheet("QWidget { background-color: " + attributes['background-color'] + '}')

                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.window.extraBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] == 'italic':
                    self.window.extraItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.window.extraUnderlinedBox.setChecked(True)
                if 'font-size' in attributes:
                    self.window.extraSizeSpinBox.setValue(int(str(attributes['font-size'])[:len(attributes['font-size']) - 2]))

            if rule.strip(' ') == 'img':

                if 'display' in attributes:
                    if attributes['display'] == 'none':
                        self.window.noneDisplayRadioButton.setChecked(True)
                    if attributes['display'] == 'block':
                        self.window.imgBlockDisplayRadioButton.setChecked(True)
                    if attributes['display'] == 'block-inline':
                        self.window.imgInlineDisplayRadioButton.setChecked(True)

                if 'max-width' in attributes and attributes['max-width'] is not 'none':
                    att = attributes['max-width'].strip(' ')
                    self.window.enableImgMaxWidth.setChecked(True)
                    if '%' in att:
                        self.window.imgWidthPerectSpinBox.setValue(int(att[:len(att) - 1]))
                        self.window.imgWidthPercetRadioButton.setChecked(True)
                    if 'px' in att:
                        self.window.imgWidthPixelSpinBox.setValue(int(att[:len(att) - 2]))
                        self.window.imgWidthPixelRadioButton.setChecked(True)

                if 'max-height' in attributes and attributes['max-height'] is not 'none':
                    att = attributes['max-height'].strip(' ')
                    self.window.enableImgMaxHeight.setChecked(True)
                    if '%' in att:
                        self.window.imgHeightPerectSpinBox.setValue(int(att[:len(att) - 1]))
                        self.window.imgHeightPercetRadioButton.setChecked(True)
                    if 'px' in att:
                        self.window.imgHeightPerectSpinBox.setValue(int(att[:len(att) - 2]))
                        self.window.imgHeightPercetRadioButton.setChecked(True)


                if 'border' in attributes:
                    # imgBorderPixelSpinBox  imgBorderColor
                    self.window.enableImgBorder.setChecked(True)
                    att = attributes['border'].strip(' ')
                    attWords = att.split()
                    pix = attWords[0]
                    self.window.imgHeightPerectSpinBox.setValue(int(pix[:len(pix) - 2]))
                    self.window.imgBorderColor.setText(attWords[len(attWords) - 1])


                if 'box-shadow' in attributes:
                    self.window.enableImgShadow.setChecked(True)
                    att = attributes['box-shadow'].strip(' ')
                    attWords = att.split()
                    if len(attWords) == 4:
                        self.window.imgShadowColor.setText(attWords[len(attWords) - 1])
                        self.window.imgShadowDropRadioButton.setChecked(True)
                    else:
                        self.window.imgShadowColor.setText(attWords[len(attWords) - 1])
                        self.window.imgShadowGlowRadioButton.setChecked(True)


    def showColorPicker(self, textField):
        colorDialig = QColorDialog()
        if textField.text() is not '':
            oldColor = QColor()
            oldColor.setNamedColor(textField.text())
            color = colorDialig.getColor(initial=oldColor)
        else:
            color = colorDialig.getColor()
        if color.isValid():
            textField.setText(color.name())
            textField.setStyleSheet("QWidget { background-color: " + color.name() + '}')


    def disableElements(self, checkbox, listOfElements):

        for element in listOfElements:
            element.setEnabled(checkbox.isChecked())

        pass


    def connectButtonsAndTextboxes(self):
        # connect buttons and textboxes
        self.window.cardTextColorButton.clicked.connect(partial(self.showColorPicker, self.window.cardTextColor))
        self.window.cardBGColorbutton.clicked.connect(partial(self.showColorPicker, self.window.cardBGColor))
        self.window.boldTextColorButton.clicked.connect(partial(self.showColorPicker, self.window.boldTextColor))
        self.window.italicsTextColorButton.clicked.connect(partial(self.showColorPicker, self.window.italicsTextColor))
        self.window.underlinedTextColorButton.clicked.connect(partial(self.showColorPicker, self.window.underlinedTextColor))
        self.window.linksTextColorButton.clicked.connect(partial(self.showColorPicker, self.window.linksTextColor))
        self.window.saveButton.clicked.connect(self.updateProfile)
        self.window.clozeTextColorButton.clicked.connect(partial(self.showColorPicker, self.window.clozeTextColor))
        self.window.clozeBGColorButton.clicked.connect(partial(self.showColorPicker, self.window.clozeBGColor))
        self.window.extraTextColorButton.clicked.connect(partial(self.showColorPicker, self.window.extraTextColor))
        self.window.extraBGColorButton.clicked.connect(partial(self.showColorPicker, self.window.extraBGColor))
        self.window.imgBorderColorButton.clicked.connect(partial(self.showColorPicker, self.window.imgBorderColor))
        self.window.imgShadowColorButton.clicked.connect(partial(self.showColorPicker, self.window.imgShadowColor))
        self.window.saveButton.clicked.connect(self.updateProfile)
        self.window.undoAllButton.clicked.connect(self.undoAll)
        self.window.cancelButton.clicked.connect(self.cancelButtonFunc)
        self.window.addTimerButton.clicked.connect(self.addTimer)
        self.window.removeTimerButton.clicked.connect(self.removeTimer)
        self.window.extraTagButton.clicked.connect(self.addExtraTag)

        boldList = [self.window.boldBoldCBOX, self.window.boldItalicBox, self.window.boldUnderlinedBox, self.window.boldTextColor, self.window.boldTextColorButton]
        self.window.enableBold.stateChanged.connect(partial(self.disableElements, self.window.enableBold, boldList))

        italicsList = [self.window.italicsBoldCBOX, self.window.italicsItalicBox, self.window.italicsUnderlinedBox, self.window.italicsTextColor, self.window.italicsTextColorButton]
        self.window.enableItalics.stateChanged.connect(partial(self.disableElements, self.window.enableItalics, italicsList))

        underlinedList = [self.window.underlinedBoldCBOX, self.window.underlinedItalicBox, self.window.underlinedUnderlinedBox, self.window.underlinedTextColor, self.window.underlinedTextColorButton]
        self.window.enableUnderlined.stateChanged.connect(partial(self.disableElements, self.window.enableUnderlined, underlinedList))

        linksList = [self.window.linksBoldCBOX, self.window.linksItalicBox, self.window.linksUnderlinedBox, self.window.linksTextColor, self.window.linksTextColorButton]
        self.window.enableLinks.stateChanged.connect(partial(self.disableElements, self.window.enableLinks, linksList))


        pass


    def unifiedUpdateAction(self):

        lineEdits = self.some.findChildren(QLineEdit)
        for ledit in lineEdits:
            ledit.textChanged.connect(self.updateProfile)

        checkBoxes = self.some.findChildren(QCheckBox)
        for cbox in checkBoxes:
            cbox.stateChanged.connect(self.updateProfile)

        spinBoxes = self.some.findChildren(QSpinBox)
        for spbox in spinBoxes:
            spbox.valueChanged.connect(self.updateProfile)
        self.window.timerSpinBox.valueChanged.disconnect()

        radioButtons = self.some.findChildren(QRadioButton)
        for rbutton in radioButtons:
            rbutton.toggled.connect(self.updateProfile)

        fontComboBox = self.some.findChild(QFontComboBox, 'fontComboBox')
        fontComboBox.currentFontChanged.connect(self.updateProfile)

        pass

    def makeRuleDictionnaryFromUI(self):

        ruleDictFromSettings = {}

        # make .Card
        if self.window.cardGroupBox.isChecked():
            cardDict = OrderedDict()

            if self.window.fontComboBox.currentText() is not '':
                cardDict['font-family'] = self.window.fontComboBox.currentText()

            if self.window.sizeSpinBox.value() is not 0:
                cardDict['font-size'] = str(self.window.sizeSpinBox.value()) + 'px'

            if self.window.alignLeft.isChecked():
                cardDict['text-align'] = 'left'
            if self.window.alignCenter.isChecked():
                cardDict['text-align'] = 'center'
            if self.window.alignRight.isChecked():
                cardDict['text-align'] = 'right'

            if self.window.cardTextColor.text() is not '':
                cardDict['color'] = self.window.cardTextColor.text()
            if self.window.cardBGColor.text() is not '':
                cardDict['background-color'] = self.window.cardBGColor.text()

            if self.window.enableCardMaxWidth.isChecked():
                if self.window.cardWidthPercetRadioButton.isChecked():
                    if self.window.cardWidthPerectSpinBox.value() is not 0:
                        cardDict['max-width'] = str(self.window.cardWidthPerectSpinBox.value()) + '%'
                if self.window.cardWidthPixelRadioButton.isChecked():
                    if self.window.cardWidthPixelSpinBox.value() is not 0:
                        cardDict['max-width'] = str(self.window.cardWidthPixelSpinBox.value()) + 'px'

            if self.window.enableCardMargin.isChecked():
                if self.window.cardMarginCenterRadio.isChecked():
                    cardDict['margin'] = '20px auto'
                if self.window.cardMarginCustomRadio.isChecked():
                    if self.window.cardMarginCustom.text() is not '':
                        cardDict['margin'] = self.window.cardMarginCustom.text()

            if self.window.cardWordWrapCheckBox.isChecked():
                cardDict['word-wrap'] = 'break-word'

            ruleDictFromSettings['.card'] = cardDict
        else:
            ruleDictFromSettings['.card'] = None


        # make .cloze
        if self.window.clozeGroupBox.isChecked():
            clozeDict = OrderedDict()

            if self.window.clozeBoldCBOX.isChecked():
                clozeDict['font-weight'] = 'bold'
            if self.window.clozeItalicBox.isChecked():
                clozeDict['font-style'] = 'italic'
            if self.window.clozeUnderlinedBox.isChecked():
                clozeDict['text-decoration'] = 'underline'


            if self.window.clozeSizeSpinBox.value() is not 0:
                clozeDict['font-size'] = str(self.window.clozeSizeSpinBox.value()) + 'px'

            if self.window.clozeTextColor.text() is not None and self.window.clozeTextColor.text() is not '':
                clozeDict['color'] = self.window.clozeTextColor.text()
            if self.window.clozeBGColor.text() is not None and self.window.clozeBGColor.text() is not '':
                clozeDict['background-color'] = self.window.clozeBGColor.text()

            if len(clozeDict) is not 0:
                ruleDictFromSettings['.cloze'] = clozeDict
            else:
                ruleDictFromSettings['.cloze'] = None
        else:
            ruleDictFromSettings['.cloze'] = None

        # make #extra
        if self.window.extraGroupBox.isChecked():
            extraDict = OrderedDict()

            if self.window.extraBoldCBOX.isChecked():
                extraDict['font-weight'] = 'bold'
            if self.window.extraItalicBox.isChecked():
                extraDict['font-styleextra'] = 'italic'
            if self.window.extraUnderlinedBox.isChecked():
                extraDict['text-decoration'] = 'underline'


            if self.window.extraSizeSpinBox.value() is not 0:
                extraDict['font-size'] = str(self.window.extraSizeSpinBox.value()) + 'px'

            if self.window.extraTextColor.text() is not None and self.window.extraTextColor.text() is not '':
                extraDict['color'] = self.window.extraTextColor.text()
            if self.window.extraBGColor.text() is not None and self.window.extraBGColor.text() is not '':
                extraDict['background-color'] = self.window.extraBGColor.text()


            if len(extraDict) is not 0:
                ruleDictFromSettings['#extra'] = extraDict
            else:
                ruleDictFromSettings['#extra'] = None

        else:
            ruleDictFromSettings['#extra'] = None

        # make img
        if self.window.imageGroupBox.isChecked():
            imgDict = OrderedDict()

            if self.window.noneDisplayRadioButton.isChecked():
                imgDict['display'] = 'none'
            if self.window.imgBlockDisplayRadioButton.isChecked():
                imgDict['display'] = 'block'
            if self.window.imgInlineDisplayRadioButton.isChecked():
                imgDict['display'] = 'block-inline'

            if self.window.enableImgMaxWidth.isChecked():
                if self.window.imgWidthPercetRadioButton.isChecked():
                    if self.window.imgWidthPerectSpinBox.value() is not 0:
                        imgDict['max-width'] = str(self.window.imgWidthPerectSpinBox.value()) + '%'
                if self.window.imgWidthPixelRadioButton.isChecked():
                    if self.window.imgWidthPixelSpinBox.value() is not 0:
                        imgDict['max-width'] = str(self.window.imgWidthPixelSpinBox.value()) + 'px'

            if self.window.enableImgMaxHeight.isChecked():
                if self.window.imgHeightPercetRadioButton.isChecked():
                    if self.window.imgHeightPerectSpinBox.value() is not 0:
                        imgDict['max-height'] = str(self.window.imgHeightPerectSpinBox.value()) + '%'
                if self.window.imgHeightPixelRadioButton.isChecked():
                    if self.window.imgHeightPixelSpinBox.value() is not 0:
                        imgDict['max-height'] = str(self.window.imgHeightPixelSpinBox.value()) + 'px'

            if self.window.enableImgBorder.isChecked():
                if self.window.imgBorderColor.text() is not None and self.window.imgBorderPixelSpinBox.value() is not 0:
                    imgDict['border'] = str.format("{}px solid {}".format(self.window.imgBorderPixelSpinBox.value(), self.window.imgBorderColor.text()))

            if self.window.enableImgShadow.isChecked():
                styleofshadow1 = styleofshadow2 = ''
                if self.window.imgShadowDropRadioButton.isChecked():
                    styleofshadow1 = '2px 2px'
                    styleofshadow2 = '5px'
                if self.window.imgShadowGlowRadioButton.isChecked():
                    styleofshadow1 = '0px 0px'
                    styleofshadow2 = '8px 3px'
                if self.window.imgShadowColor.text() is not None:
                    imgDict['box-shadow'] = str.format("{} {} {}".format(styleofshadow1, styleofshadow2, self.window.imgShadowColor.text()))

            if len(imgDict) is not 0:
                ruleDictFromSettings['img'] = imgDict
            else:
                ruleDictFromSettings['img'] = None

        else:
            ruleDictFromSettings['img'] = None

        # make text style
        if self.window.generalGroupBox.isChecked():

            if self.window.enableBold.isChecked():
                # make bold
                boldDict = OrderedDict()

                if self.window.boldBoldCBOX.isChecked():
                    boldDict['font-weight'] = 'bold'
                else:
                    boldDict['font-weight'] = 'normal'

                if self.window.boldItalicBox.isChecked():
                    boldDict['font-style'] = 'italic'
                if self.window.boldUnderlinedBox.isChecked():
                    boldDict['text-decoration'] = 'underline'
                if self.window.boldTextColor.text() is not '':
                    boldDict['color'] = self.window.boldTextColor.text()

                ruleDictFromSettings['b'] = boldDict
            else:
                ruleDictFromSettings['b'] = None

            if self.window.enableItalics.isChecked():
                # make italics
                italicsDict = OrderedDict()

                if self.window.italicsBoldCBOX.isChecked():
                    italicsDict['font-weight'] = 'bold'
                else:
                    italicsDict['font-weight'] = 'normal'
                if self.window.italicsItalicBox.isChecked():
                    italicsDict['font-style'] = 'italic'
                else:
                    italicsDict['font-style'] = 'normal'
                if self.window.italicsUnderlinedBox.isChecked():
                    italicsDict['text-decoration'] = 'underline'
                else:
                    italicsDict['text-decoration'] = 'none'
                if self.window.italicsTextColor.text() is not '':
                    italicsDict['color'] = self.window.italicsTextColor.text()

                ruleDictFromSettings['i'] = italicsDict
            else:
                ruleDictFromSettings['i'] = None

            if self.window.enableUnderlined.isChecked():
                # make underlined
                underlinedDict = OrderedDict()

                if self.window.underlinedBoldCBOX.isChecked():
                    underlinedDict['font-weight'] = 'bold'
                if self.window.underlinedItalicBox.isChecked():
                    underlinedDict['font-style'] = 'italic'
                if self.window.underlinedUnderlinedBox.isChecked():
                    underlinedDict['text-decoration'] = 'underline'
                else:
                    underlinedDict['text-decoration'] = 'none'
                if self.window.underlinedTextColor.text() is not '':
                    underlinedDict['color'] = self.window.underlinedTextColor.text()

                ruleDictFromSettings['u'] = underlinedDict
            else:
                ruleDictFromSettings['u'] = None

            if self.window.enableLinks.isChecked():
                # make links
                linksDict = OrderedDict()

                if self.window.linksBoldCBOX.isChecked():
                    linksDict['font-weight'] = 'bold'
                if self.window.linksItalicBox.isChecked():
                    linksDict['font-style'] = 'italic'
                if self.window.linksUnderlinedBox.isChecked():
                    linksDict['text-decoration'] = 'underline'
                if self.window.linksTextColor.text() is not '':
                    linksDict['color'] = self.window.linksTextColor.text()

                ruleDictFromSettings['a'] = linksDict
            else:
                ruleDictFromSettings['a'] = None

        else:
            ruleDictFromSettings['b'] = None
            ruleDictFromSettings['i'] = None
            ruleDictFromSettings['u'] = None
            ruleDictFromSettings['a'] = None

        return ruleDictFromSettings


    def updateProfile(self):

        for ruleName, ruleDict in self.makeRuleDictionnaryFromUI().items():

            self.profile.setNewDeclarationsDictOrDeleteRule(ruleName, ruleDict)

        cssTextWithConfigs = self.insertorChangeConfigs(self.profile.cssString, 'Not Saved')

        self.cssBoxx.setText(cssTextWithConfigs)

        pass


    def undoAll(self):
        self.cssBoxx.setText(self.memoryBackedUpCssProfileText)
        self.loadSettingsFromCss(self.memoryBackedUpCssProfileText)
        pass


    def cancelButtonFunc(self):

        clayout.some.close()

        pass

    def insertorChangeConfigs(self, cssText, saveStatus):
        signalString = cssText[:11]
        if signalString == '/* Profile:':
            endOfNameIndex = cssText.find('*/')
            if endOfNameIndex != -1:
                profileConfigs = cssText[2:11 + endOfNameIndex]

                configList = profileConfigs.split('||')

                profileName = configList[0].split(':')[1].strip()

                newCss = cssText[endOfNameIndex + 3:]
                return '/* Profile: {} || Satus: {} */ \n\n'.format(profileName, saveStatus) + newCss

        else:
            return '/* Profile: {} || Satus: {} */ \n\n'.format('Custom Profile', saveStatus) + cssText


    def addExtraTag(self):
        backBox = self.topCardLayout.findChild(QTextEdit, "back")
        signalString = backBox.toPlainText()
        extraIndex = signalString.find(r'''{{Extra}}''')
        newExtraString = r'''<div id="extra">{{Extra}}</div>'''
        if extraIndex != -1:
            firstPart = signalString[:extraIndex]
            secondPart = signalString[extraIndex + 9:]
            backBox.setPlainText(firstPart + newExtraString + secondPart)

        else:
            pass


    def addTimer(self):
        duration = self.window.timerSpinBox.value()
        if duration is not 0:
            timerText = r'''<!-- Timer Code Start-->
<br>
<span class="timer" id="s2" style='font-size:20px; color: #A6ABB9; opacity: 0.95;'></span>
<script>
function countdown( elementName, minutes, seconds )
{
    var element, endTime, hours, mins, msLeft, time;
    function twoDigits( n )
    {
        return (n <= 9 ? "0" + n : n);
    }
    function updateTimer()
    {
        msLeft = endTime - (+new Date);
        if ( msLeft < 1000 ) {
            element.innerHTML = "<span style='color:#CC5B5B'>Time's up !</span>";
        } else {
            time = new Date( msLeft );
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits( mins ) : mins) + ':' + twoDigits( time.getUTCSeconds() );
            setTimeout( updateTimer, time.getUTCMilliseconds() + 500 );
        }
    }
    element = document.getElementById( elementName );
    endTime = (+new Date) + 1000 * (60*minutes + seconds) + 500;
    updateTimer();
}
countdown("s2", 0, ''' + str(duration) + '''); //2nd value is the minute, 3rd is the seconds
</script>
<!-- Timer Code End-->'''
            frontBox = self.topCardLayout.findChild(QTextEdit, "front")
            frontBox.setPlainText(frontBox.toPlainText() + "\n" + timerText)
            pass

        else:
            showInfo('Duration cannot be zero!')
            pass

        pass

    def removeTimer(self):

        frontBox = self.topCardLayout.findChild(QTextEdit, "front")
        signalString = frontBox.toPlainText()
        timerStartIndex = signalString.find(r'''<!-- Timer Code Start-->''')
        if timerStartIndex is not -1:
            timerEndIndex = signalString.find(r'''<!-- Timer Code End-->''')

            firstPart = signalString[:timerStartIndex]
            secondPart = signalString[timerEndIndex + 22:]

            frontBox.setPlainText(firstPart + " " + secondPart)
            pass
        else:
            showInfo('No Timer Detected!')
            pass

        pass
