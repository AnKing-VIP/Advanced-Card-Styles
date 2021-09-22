from functools import partial

from aqt import clayout, mw
from aqt.utils import showInfo
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from . import AdvancedStylerUI
from .CssProfile import *
from .myCssParser import *

# Next Steps:
# 1 - Fix messagebox
# 2 - Add Profile Detection


class ASGUI(QDialog):

    def __init__(self, clayout):
        QDialog.__init__(self, clayout, Qt.Window)
        mw.setupDialogGC(self)
        self.mw = mw
        self.clayout = clayout

        self.profile = CssProfile()
        self.memoryBackedUpCssProfileText = ''

        self.form = AdvancedStylerUI.Ui_Form()
        self.form.setupUi(self)
        self.loadUI()

        self.show()

    def loadUI(self):
        self.setWindowIcon(self.clayout.windowIcon())

        self.setWindowModality(Qt.ApplicationModal)

        text = self.clayout.model['css']
        self.loadSettingsFromCss(text)
        self.memoryBackedUpCssProfileText = text

        self.connectButtonsAndTextboxes()
        self.unifiedUpdateAction()

        # take the focus away from the first input area when starting up,
        # as users tend to accidentally type into the template

    def connectButtonsAndTextboxes(self):
        # connect buttons and textboxes
        self.form.cardTextColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.cardTextColor))
        self.form.cardBGColorbutton.clicked.connect(
            partial(self.showColorPicker, self.form.cardBGColor))
        self.form.boldTextColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.boldTextColor))
        self.form.italicsTextColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.italicsTextColor))
        self.form.underlinedTextColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.underlinedTextColor))
        self.form.linksTextColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.linksTextColor))
        self.form.clozeTextColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.clozeTextColor))
        self.form.clozeBGColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.clozeBGColor))
        self.form.extraTextColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.extraTextColor))
        self.form.extraBGColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.extraBGColor))
        self.form.imgBorderColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.imgBorderColor))
        self.form.imgShadowColorButton.clicked.connect(
            partial(self.showColorPicker, self.form.imgShadowColor))
        self.form.undoAllButton.clicked.connect(self.undoAll)
        self.form.cancelButton.clicked.connect(self.onCancelButtonPress)
        self.form.addTimerButton.clicked.connect(self.addTimer)
        self.form.removeTimerButton.clicked.connect(self.removeTimer)
        self.form.extraTagButton.clicked.connect(self.addExtraTag)

        boldList = [self.form.boldBoldCBOX, self.form.boldItalicBox,
                    self.form.boldUnderlinedBox, self.form.boldTextColor, self.form.boldTextColorButton]
        self.form.enableBold.stateChanged.connect(
            partial(self.disableElements, self.form.enableBold, boldList))

        italicsList = [self.form.italicsBoldCBOX, self.form.italicsItalicBox,
                       self.form.italicsUnderlinedBox, self.form.italicsTextColor, self.form.italicsTextColorButton]
        self.form.enableItalics.stateChanged.connect(
            partial(self.disableElements, self.form.enableItalics, italicsList))

        underlinedList = [self.form.underlinedBoldCBOX, self.form.underlinedItalicBox,
                          self.form.underlinedUnderlinedBox, self.form.underlinedTextColor, self.form.underlinedTextColorButton]
        self.form.enableUnderlined.stateChanged.connect(
            partial(self.disableElements, self.form.enableUnderlined, underlinedList))

        linksList = [self.form.linksBoldCBOX, self.form.linksItalicBox,
                     self.form.linksUnderlinedBox, self.form.linksTextColor, self.form.linksTextColorButton]
        self.form.enableLinks.stateChanged.connect(
            partial(self.disableElements, self.form.enableLinks, linksList))

    def onCancelButtonPress(self):
        self.close()

    # read / write css from ui widgets
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
                    self.form.fontComboBox.setCurrentText(
                        attributes['font-family'])
                if 'font-size' in attributes:
                    self.form.sizeSpinBox.setValue(
                        int(str(attributes['font-size'])[:len(attributes['font-size']) - 2]))
                if 'text-align' in attributes:
                    if attributes['text-align'] == 'left':
                        self.form.alignLeft.setChecked(True)
                    if attributes['text-align'] == 'center':
                        self.form.alignCenter.setChecked(True)
                    if attributes['text-align'] == 'right':
                        self.form.alignRight.setChecked(True)
                if 'color' in attributes:
                    self.form.cardTextColor.setText(attributes['color'])
                    self.form.cardTextColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['color'] + '}')

                if 'background-color' in attributes:
                    self.form.cardBGColor.setText(
                        attributes['background-color'])
                    self.form.cardBGColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['background-color'] + '}')

                if 'max-width' in attributes and attributes['max-width'] != 'none':
                    att = attributes['max-width'].strip(' ')
                    self.form.enableCardMaxWidth.setChecked(True)
                    if '%' in att:
                        self.form.cardWidthPerectSpinBox.setValue(
                            int(att[:len(att) - 1]))
                        self.form.cardWidthPercetRadioButton.setChecked(True)
                    if 'px' in att:
                        self.form.cardWidthPixelSpinBox.setValue(
                            int(att[:len(att) - 2]))
                        self.form.cardWidthPixelRadioButton.setChecked(True)

                if 'margin' in attributes and attributes['margin'] != 'none':
                    self.form.enableCardMargin.setChecked(True)
                    att = attributes['margin'].strip(' ')
                    if att == '20px auto':
                        self.form.cardMarginCenterRadio.setChecked(True)
                    else:
                        self.form.cardMarginCustomRadio.setChecked(True)
                        self.form.cardMarginCustom.setText(att)

                if 'word-wrap' in attributes and attributes['word-wrap'] == 'break-word':
                    self.form.cardWordWrapCheckBox.setChecked(True)

            if rule.strip(' ') == 'b':
                self.form.enableBold.setChecked(True)
                if 'color' in attributes:
                    self.form.boldTextColor.setText(attributes['color'])
                    self.form.boldTextColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['color'] + '}')

                # because bold already has bold, boldBoldCBOX will be checked by default unless font-weight is normal   font-weight: bold;
                if 'font-weight' not in attributes or attributes['font-weight'] != 'normal':
                    self.form.boldBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] == 'italic':
                    self.form.boldItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.form.boldUnderlinedBox.setChecked(True)

            if rule.strip(' ') == 'i':
                self.form.enableItalics.setChecked(True)
                if 'color' in attributes:
                    self.form.italicsTextColor.setText(attributes['color'])
                    self.form.italicsTextColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['color'] + '}')

                # because bold already has bold, boldBoldCBOX will be checked by default unless font-weight is normal   font-weight: bold;
                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.form.italicsBoldCBOX.setChecked(True)
                if 'font-style' not in attributes or attributes['font-style'] != 'normal':
                    self.form.italicsItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.form.italicsUnderlinedBox.setChecked(True)

            if rule.strip(' ') == 'u':
                self.form.enableUnderlined.setChecked(True)
                if 'color' in attributes:
                    self.form.underlinedTextColor.setText(
                        attributes['color'])
                    self.form.underlinedTextColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['color'] + '}')

                # because bold already has bold, boldBoldCBOX will be checked by default unless font-weight is normal   font-weight: bold;
                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.form.underlinedBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] != 'italic':
                    self.form.underlinedItalicBox.setChecked(True)
                if 'text-decoration' not in attributes or attributes['text-decoration'] != 'none':
                    self.form.underlinedUnderlinedBox.setChecked(True)

            if rule.strip(' ') == 'a':
                self.form.enableLinks.setChecked(True)
                if 'color' in attributes:
                    self.form.linksTextColor.setText(attributes['color'])
                    self.form.linksTextColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['color'] + '}')

                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.form.linksBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] == 'italic':
                    self.form.linksItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.form.linksUnderlinedBox.setChecked(True)

            if rule.strip(' ') == '.cloze':
                self.form.clozeGroupBox.setChecked(True)
                if 'color' in attributes:
                    self.form.clozeTextColor.setText(attributes['color'])
                    self.form.clozeTextColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['color'] + '}')

                if 'background-color' in attributes:
                    self.form.clozeBGColor.setText(
                        attributes['background-color'])
                    self.form.clozeBGColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['background-color'] + '}')

                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.form.clozeBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] == 'italic':
                    self.form.clozeItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.form.clozeUnderlinedBox.setChecked(True)
                if 'font-size' in attributes:
                    self.form.clozeSizeSpinBox.setValue(
                        int(str(attributes['font-size'])[:len(attributes['font-size']) - 2]))

            if rule.strip(' ') == '#extra':
                self.form.extraGroupBox.setChecked(True)
                if 'color' in attributes:
                    self.form.extraTextColor.setText(attributes['color'])
                    self.form.extraTextColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['color'] + '}')

                if 'background-color' in attributes:
                    self.form.extraBGColor.setText(
                        attributes['background-color'])
                    self.form.extraBGColor.setStyleSheet(
                        "QWidget { background-color: " + attributes['background-color'] + '}')

                if 'font-weight' in attributes and attributes['font-weight'] == 'bold':
                    self.form.extraBoldCBOX.setChecked(True)
                if 'font-style' in attributes and attributes['font-style'] == 'italic':
                    self.form.extraItalicBox.setChecked(True)
                if 'text-decoration' in attributes and attributes['text-decoration'] == 'underline':
                    self.form.extraUnderlinedBox.setChecked(True)
                if 'font-size' in attributes:
                    self.form.extraSizeSpinBox.setValue(
                        int(str(attributes['font-size'])[:len(attributes['font-size']) - 2]))

            if rule.strip(' ') == 'img':

                if 'display' in attributes:
                    if attributes['display'] == 'none':
                        self.form.noneDisplayRadioButton.setChecked(True)
                    if attributes['display'] == 'block':
                        self.form.imgBlockDisplayRadioButton.setChecked(True)
                    if attributes['display'] == 'block-inline':
                        self.form.imgInlineDisplayRadioButton.setChecked(
                            True)

                if 'max-width' in attributes and attributes['max-width'] != 'none':
                    att = attributes['max-width'].strip(' ')
                    self.form.enableImgMaxWidth.setChecked(True)
                    if '%' in att:
                        self.form.imgWidthPerectSpinBox.setValue(
                            int(att[:len(att) - 1]))
                        self.form.imgWidthPercetRadioButton.setChecked(True)
                    if 'px' in att:
                        self.form.imgWidthPixelSpinBox.setValue(
                            int(att[:len(att) - 2]))
                        self.form.imgWidthPixelRadioButton.setChecked(True)

                if 'max-height' in attributes and attributes['max-height'] != 'none':
                    att = attributes['max-height'].strip(' ')
                    self.form.enableImgMaxHeight.setChecked(True)
                    if '%' in att:
                        self.form.imgHeightPerectSpinBox.setValue(
                            int(att[:len(att) - 1]))
                        self.form.imgHeightPercetRadioButton.setChecked(True)
                    if 'px' in att:
                        self.form.imgHeightPerectSpinBox.setValue(
                            int(att[:len(att) - 2]))
                        self.form.imgHeightPercetRadioButton.setChecked(True)

                if 'border' in attributes:
                    # imgBorderPixelSpinBox  imgBorderColor
                    self.form.enableImgBorder.setChecked(True)
                    att = attributes['border'].strip(' ')
                    attWords = att.split()
                    pix = attWords[0]
                    self.form.imgHeightPerectSpinBox.setValue(
                        int(pix[:len(pix) - 2]))
                    self.form.imgBorderColor.setText(
                        attWords[len(attWords) - 1])

                if 'box-shadow' in attributes:
                    self.form.enableImgShadow.setChecked(True)
                    att = attributes['box-shadow'].strip(' ')
                    attWords = att.split()
                    if len(attWords) == 4:
                        self.form.imgShadowColor.setText(
                            attWords[len(attWords) - 1])
                        self.form.imgShadowDropRadioButton.setChecked(True)
                    else:
                        self.form.imgShadowColor.setText(
                            attWords[len(attWords) - 1])
                        self.form.imgShadowGlowRadioButton.setChecked(True)

    def unifiedUpdateAction(self):
        lineEdits = self.findChildren(QLineEdit)
        for ledit in lineEdits:
            ledit.textChanged.connect(self.updateProfile)

        checkBoxes = self.findChildren(QCheckBox)
        for cbox in checkBoxes:
            cbox.stateChanged.connect(self.updateProfile)

        spinBoxes = self.findChildren(QSpinBox)
        for spbox in spinBoxes:
            spbox.valueChanged.connect(self.updateProfile)
        self.form.timerSpinBox.valueChanged.disconnect()

        radioButtons = self.findChildren(QRadioButton)
        for rbutton in radioButtons:
            rbutton.toggled.connect(self.updateProfile)

        fontComboBox = self.findChild(QFontComboBox, 'fontComboBox')
        fontComboBox.currentFontChanged.connect(self.updateProfile)

    def makeRuleDictionnaryFromUI(self):
        ruleDictFromSettings = {}

        # make .Card
        if self.form.cardGroupBox.isChecked():
            cardDict = OrderedDict()

            if self.form.fontComboBox.currentText() != '':
                cardDict['font-family'] = self.form.fontComboBox.currentText()

            if self.form.sizeSpinBox.value() != 0:
                cardDict['font-size'] = str(
                    self.form.sizeSpinBox.value()) + 'px'

            if self.form.alignLeft.isChecked():
                cardDict['text-align'] = 'left'
            if self.form.alignCenter.isChecked():
                cardDict['text-align'] = 'center'
            if self.form.alignRight.isChecked():
                cardDict['text-align'] = 'right'

            if self.form.cardTextColor.text() != '':
                if self.form.cardTextColor.text() in ('black', '#000000'):
                    cardDict['color'] = 'black'
                else:
                    cardDict['color'] = self.form.cardTextColor.text() + \
                        ' !important'
            if self.form.cardBGColor.text() != '':
                if self.form.cardBGColor.text() in ('white', '#ffffff'):
                    cardDict['background-color'] = 'white'
                else:
                    cardDict['background-color'] = self.form.cardBGColor.text() + \
                        ' !important'

            if self.form.enableCardMaxWidth.isChecked():
                if self.form.cardWidthPercetRadioButton.isChecked():
                    if self.form.cardWidthPerectSpinBox.value() != 0:
                        cardDict['max-width'] = str(
                            self.form.cardWidthPerectSpinBox.value()) + '%'
                if self.form.cardWidthPixelRadioButton.isChecked():
                    if self.form.cardWidthPixelSpinBox.value() != 0:
                        cardDict['max-width'] = str(
                            self.form.cardWidthPixelSpinBox.value()) + 'px'

            if self.form.enableCardMargin.isChecked():
                if self.form.cardMarginCenterRadio.isChecked():
                    cardDict['margin'] = '20px auto'
                if self.form.cardMarginCustomRadio.isChecked():
                    if self.form.cardMarginCustom.text() != '':
                        cardDict['margin'] = self.form.cardMarginCustom.text()

            if self.form.cardWordWrapCheckBox.isChecked():
                cardDict['word-wrap'] = 'break-word'

            ruleDictFromSettings['.card'] = cardDict
        else:
            ruleDictFromSettings['.card'] = None

        # make .cloze
        if self.form.clozeGroupBox.isChecked():
            clozeDict = OrderedDict()

            if self.form.clozeBoldCBOX.isChecked():
                clozeDict['font-weight'] = 'bold'
            if self.form.clozeItalicBox.isChecked():
                clozeDict['font-style'] = 'italic'
            if self.form.clozeUnderlinedBox.isChecked():
                clozeDict['text-decoration'] = 'underline'

            if self.form.clozeSizeSpinBox.value() != 0:
                clozeDict['font-size'] = str(
                    self.form.clozeSizeSpinBox.value()) + 'px'

            if self.form.clozeTextColor.text() != None and self.form.clozeTextColor.text() != '':
                clozeDict['color'] = self.form.clozeTextColor.text()
            if self.form.clozeBGColor.text() != None and self.form.clozeBGColor.text() != '':
                clozeDict['background-color'] = self.form.clozeBGColor.text()

            if len(clozeDict) != 0:
                ruleDictFromSettings['.cloze'] = clozeDict
            else:
                ruleDictFromSettings['.cloze'] = None
        else:
            ruleDictFromSettings['.cloze'] = None

        # make #extra
        if self.form.extraGroupBox.isChecked():
            extraDict = OrderedDict()

            if self.form.extraBoldCBOX.isChecked():
                extraDict['font-weight'] = 'bold'
            if self.form.extraItalicBox.isChecked():
                extraDict['font-styleextra'] = 'italic'
            if self.form.extraUnderlinedBox.isChecked():
                extraDict['text-decoration'] = 'underline'

            if self.form.extraSizeSpinBox.value() != 0:
                extraDict['font-size'] = str(
                    self.form.extraSizeSpinBox.value()) + 'px'

            if self.form.extraTextColor.text() != None and self.form.extraTextColor.text() != '':
                extraDict['color'] = self.form.extraTextColor.text()
            if self.form.extraBGColor.text() != None and self.form.extraBGColor.text() != '':
                extraDict['background-color'] = self.form.extraBGColor.text()

            if len(extraDict) != 0:
                ruleDictFromSettings['#extra'] = extraDict
            else:
                ruleDictFromSettings['#extra'] = None

        else:
            ruleDictFromSettings['#extra'] = None

        # make img
        if self.form.imageGroupBox.isChecked():
            imgDict = OrderedDict()

            if self.form.noneDisplayRadioButton.isChecked():
                imgDict['display'] = 'none'
            if self.form.imgBlockDisplayRadioButton.isChecked():
                imgDict['display'] = 'block'
            if self.form.imgInlineDisplayRadioButton.isChecked():
                imgDict['display'] = 'block-inline'

            if self.form.enableImgMaxWidth.isChecked():
                if self.form.imgWidthPercetRadioButton.isChecked():
                    if self.form.imgWidthPerectSpinBox.value() != 0:
                        imgDict['max-width'] = str(
                            self.form.imgWidthPerectSpinBox.value()) + '%'
                if self.form.imgWidthPixelRadioButton.isChecked():
                    if self.form.imgWidthPixelSpinBox.value() != 0:
                        imgDict['max-width'] = str(
                            self.form.imgWidthPixelSpinBox.value()) + 'px'

            if self.form.enableImgMaxHeight.isChecked():
                if self.form.imgHeightPercetRadioButton.isChecked():
                    if self.form.imgHeightPerectSpinBox.value() != 0:
                        imgDict['max-height'] = str(
                            self.form.imgHeightPerectSpinBox.value()) + '%'
                if self.form.imgHeightPixelRadioButton.isChecked():
                    if self.form.imgHeightPixelSpinBox.value() != 0:
                        imgDict['max-height'] = str(
                            self.form.imgHeightPixelSpinBox.value()) + 'px'

            if self.form.enableImgBorder.isChecked():
                if self.form.imgBorderColor.text() != None and self.form.imgBorderPixelSpinBox.value() != 0:
                    imgDict['border'] = str.format("{}px solid {}".format(
                        self.form.imgBorderPixelSpinBox.value(), self.form.imgBorderColor.text()))

            if self.form.enableImgShadow.isChecked():
                styleofshadow1 = styleofshadow2 = ''
                if self.form.imgShadowDropRadioButton.isChecked():
                    styleofshadow1 = '2px 2px'
                    styleofshadow2 = '5px'
                if self.form.imgShadowGlowRadioButton.isChecked():
                    styleofshadow1 = '0px 0px'
                    styleofshadow2 = '8px 3px'
                if self.form.imgShadowColor.text() != None:
                    imgDict['box-shadow'] = str.format("{} {} {}".format(
                        styleofshadow1, styleofshadow2, self.form.imgShadowColor.text()))

            if len(imgDict) != 0:
                ruleDictFromSettings['img'] = imgDict
            else:
                ruleDictFromSettings['img'] = None

        else:
            ruleDictFromSettings['img'] = None

        # make text style
        if self.form.generalGroupBox.isChecked():

            if self.form.enableBold.isChecked():
                # make bold
                boldDict = OrderedDict()

                if self.form.boldBoldCBOX.isChecked():
                    boldDict['font-weight'] = 'bold'
                else:
                    boldDict['font-weight'] = 'normal'

                if self.form.boldItalicBox.isChecked():
                    boldDict['font-style'] = 'italic'
                if self.form.boldUnderlinedBox.isChecked():
                    boldDict['text-decoration'] = 'underline'
                if self.form.boldTextColor.text() != '':
                    boldDict['color'] = self.form.boldTextColor.text()

                ruleDictFromSettings['b'] = boldDict
            else:
                ruleDictFromSettings['b'] = None

            if self.form.enableItalics.isChecked():
                # make italics
                italicsDict = OrderedDict()

                if self.form.italicsBoldCBOX.isChecked():
                    italicsDict['font-weight'] = 'bold'
                else:
                    italicsDict['font-weight'] = 'normal'
                if self.form.italicsItalicBox.isChecked():
                    italicsDict['font-style'] = 'italic'
                else:
                    italicsDict['font-style'] = 'normal'
                if self.form.italicsUnderlinedBox.isChecked():
                    italicsDict['text-decoration'] = 'underline'
                else:
                    italicsDict['text-decoration'] = 'none'
                if self.form.italicsTextColor.text() != '':
                    italicsDict['color'] = self.form.italicsTextColor.text()

                ruleDictFromSettings['i'] = italicsDict
            else:
                ruleDictFromSettings['i'] = None

            if self.form.enableUnderlined.isChecked():
                # make underlined
                underlinedDict = OrderedDict()

                if self.form.underlinedBoldCBOX.isChecked():
                    underlinedDict['font-weight'] = 'bold'
                if self.form.underlinedItalicBox.isChecked():
                    underlinedDict['font-style'] = 'italic'
                if self.form.underlinedUnderlinedBox.isChecked():
                    underlinedDict['text-decoration'] = 'underline'
                else:
                    underlinedDict['text-decoration'] = 'none'
                if self.form.underlinedTextColor.text() != '':
                    underlinedDict['color'] = self.form.underlinedTextColor.text()

                ruleDictFromSettings['u'] = underlinedDict
            else:
                ruleDictFromSettings['u'] = None

            if self.form.enableLinks.isChecked():
                # make links
                linksDict = OrderedDict()

                if self.form.linksBoldCBOX.isChecked():
                    linksDict['font-weight'] = 'bold'
                if self.form.linksItalicBox.isChecked():
                    linksDict['font-style'] = 'italic'
                if self.form.linksUnderlinedBox.isChecked():
                    linksDict['text-decoration'] = 'underline'
                if self.form.linksTextColor.text() != '':
                    linksDict['color'] = self.form.linksTextColor.text()

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

        cssTextWithConfigs = self.insertorChangeConfigs(
            self.profile.cssString, 'Not Saved')

        self.clayout.model['css'] = cssTextWithConfigs
        self.clayout.change_tracker.mark_basic()
        self.clayout.update_current_ordinal_and_redraw(self.clayout.ord)

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

    # read / write front and back of current card template
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

    # misc
    def undoAll(self):
        self.clayout.model['css'] = self.memoryBackedUpCssProfileText
        self.loadSettingsFromCss(self.memoryBackedUpCssProfileText)
        self.clayout.change_tracker.mark_basic()
        self.clayout.update_current_ordinal_and_redraw(self.clayout.ord)

    def addExtraTag(self):
        signalString = self.front
        extraIndex = signalString.find(r'{{Extra}}')
        newExtraString = r'<div id="extra">{{Extra}}</div>'
        if extraIndex != -1:
            firstPart = signalString[:extraIndex]
            secondPart = signalString[extraIndex + 9:]
            self.back = firstPart + newExtraString + secondPart
            self.clayout.change_tracker.mark_basic()
            self.clayout.update_current_ordinal_and_redraw(self.clayout.ord)

    def addTimer(self):
        duration = self.form.timerSpinBox.value()
        if duration != 0:
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
            self.front = self.front + "\n" + timerText
            self.clayout.update_current_ordinal_and_redraw(self.clayout.ord)
            self.clayout.change_tracker.mark_basic()
        else:
            showInfo('Duration cannot be zero!')

    def removeTimer(self):
        signalString = self.front
        timerStartIndex = signalString.find(r'''<!-- Timer Code Start-->''')
        if timerStartIndex != -1:
            timerEndIndex = signalString.find(r'''<!-- Timer Code End-->''')

            firstPart = signalString[:timerStartIndex]
            secondPart = signalString[timerEndIndex + 22:]
            self.front = firstPart + " " + secondPart
            self.clayout.update_current_ordinal_and_redraw(self.clayout.ord)
            self.clayout.change_tracker.mark_basic()
        else:
            showInfo('No Timer Detected!')

    # ui utils
    def showColorPicker(self, textField):
        colorDialig = QColorDialog()
        if textField.text() != '':
            oldColor = QColor()
            oldColor.setNamedColor(textField.text())
            color = colorDialig.getColor(initial=oldColor)
        else:
            color = colorDialig.getColor()
        if color.isValid():
            textField.setText(color.name())
            textField.setStyleSheet(
                "QWidget { background-color: " + color.name() + '}')

    def disableElements(self, checkbox, listOfElements):
        for element in listOfElements:
            element.setEnabled(checkbox.isChecked())
