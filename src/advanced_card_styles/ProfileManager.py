import os
from pathlib import Path
from zipfile import ZipFile

from aqt.qt import *

dir_path = os.path.dirname(os.path.realpath(__file__))
basepath = Path(dir_path) / 'user_files'


def getAvailableProfiles():
    result = []
    for directory in (entry for entry in basepath.iterdir() if entry.is_dir()):
        listOfFiles = [x.name for x in directory.iterdir() if x.is_file()]
        if 'css.css' in listOfFiles:
            result.append(directory.name)

    return result


def saveProfile(profileName, cssText, frontText=None, backText=None):
    saveFilePath = basepath / profileName
    saveFilePath.mkdir(exist_ok=True)
    cssFile = saveFilePath / 'css.css'
    fontFile = saveFilePath / 'front.txt'
    backFile = saveFilePath / 'back.txt'

    with open(cssFile, 'w+') as savefile:
        savefile.write(cssText)

    if frontText is not None:
        with open(fontFile, 'w+') as savefile:
            savefile.write(frontText)

    if backText is not None:
        with open(backFile, 'w+') as savefile:
            savefile.write(backText)


def exportProfile(profileComboBox, includeAllCBox):
    profileNameDir = profileComboBox.currentText()
    exportPath, _ = QFileDialog.getSaveFileName(
        None, 
        'Export Profile :',
        directory=str(Path.home() / "Desktop"), 
        filter='Advanced Card Style Profile (*.acs);;All Files (*)'
    )
    print(exportPath)
    os.chdir(basepath)
    listOfFiles = [x for x in Path(profileNameDir).iterdir() if x.is_file()]

    if exportPath != '':
        with ZipFile(exportPath, 'w') as zipped:
            # writing each file one by one
            for file in listOfFiles:
                if 'front' in file.name or 'back' in file.name:
                    # zip the file
                    if includeAllCBox.isChecked():
                        zipped.write(file)

                else:
                    zipped.write(file)

    os.chdir('..')


def importProfile():
    beforeImportList = getAvailableProfiles()
    importPath, _ = QFileDialog.getOpenFileName(None, 'Import Profile :', directory=str(
        Path.home() / "Desktop"), filter='Advanced Card Style Profile (*.acs);;All Files (*)')
    print(importPath)
    if importPath != '':
        with ZipFile(importPath, 'r') as zipped:
            zipped.extractall(basepath)

    afterImportList = getAvailableProfiles()

    for x in afterImportList:
        if x in beforeImportList:
            pass
        else:
            return x
    else:
        return None


class ProfileFolder():
    """ProfileFolder"""

    def __init__(self, arg):
        pass
