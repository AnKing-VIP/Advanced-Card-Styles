# from tinycss2 import *
from .myCssParser import *
from pathlib import Path
from aqt.utils import showInfo


class CssProfile():

    '''
    This is a class for the css profile.
    It is used in conjunction with the Css Parser to facilitate changing stuff inside of a css file.

    The user should at first create an instance of the object
    eg. new_profile = CssProfile()

    Then initailize it from a file or a Css String
    eg. new_profile.initializeFromFile('test.css')

    To be able to edit attributes (declarations) inside a class (rule):
    1- The user should first get the list of rules.
    eg. new_profile.ruleNamesList <-- this is a list that contains all rule Names as strings

    2- We use the get function to get the ordered dictionnary of the declarations for a specified rule, then we edit it.
    eg. new_dict = new_profile.getDeclarationsDictFromRule('.testRule ') <-- new_dict is a new ordered dictionnary created locally
        new_dict['color'] = 'red' <-- assuming we know there is a key named 'color'

    3- set the new_dict as the one for the specified rule.
    eg. profile.setDeclarationsDictForRule('.testRule ', new_dict)

    -- At-rules have not been tested.

    '''

    def __init__(self):
        self.initialized = False
        self.name = 'NOT YET INITIALIZED'
        self.rootList = []
        self.ruleNamesList = []
        pass

    # Initializing functions :

    def initializeFromFile(self, filePath):
        self.rootList = createRootListFromFile(filePath)
        self.__createRuleNamesList()
        self.name = Path(filePath).name.split('.')[0]
        self.initialized = True
        pass

    def initializeFromCssString(self, cssString, profileName):
        self.rootList = createRootListFromCssString(cssString)
        # showInfo('Rootlist : \n' + str(self.rootList))
        self.__createRuleNamesList()
        self.name = profileName
        self.initialized = True
        pass


    # Changing stuff functions :

    def __createRuleNamesList(self):
        self.ruleNamesList = [x[0] for x in self.rootList if type(x) == tuple]

    def getDeclarationsDictFromRule(self, ruleName):
        if self.rootList is None:
            showInfo('Weird Shit Happenin, profile rootList has 0 elements.')
        a = []

        for x in self.rootList:
            # showInfo(str(x))
            if (type(x) == tuple and x[0] == ruleName):
                a.append(x[1])
        # a = [x[1] for x in self.rootList if (type(x) == tuple and x[0] == ruleName)]

        if len(a) != 0:  # this is a failsafe to keep program running but can lead to disappearing stuff
            return a[0]

    def setNewDeclarationsDictOrDeleteRule(self, ruleName, newOrderedDict):

        # First we get the index of the tuple of the requested rule
        # Then we create a new tuple with same ruleName
        # Then we overwrite the item at the same index

        # showInfo('setNewDeclarationsDictOrDeleteRule starting for rule : ' + ruleName)

        index = None

        for item in self.rootList:
            if type(item) == tuple:
                if item[0] == ruleName:
                    index = self.rootList.index(item)
                    break
                else:
                    continue
            pass

        if index != None:
            if newOrderedDict != None:
                self.rootList[index] = (ruleName, newOrderedDict)
            else:
                del self.rootList[index]
        else:
            if newOrderedDict != None:
                self.rootList.append((ruleName, newOrderedDict))
        pass

    # Accessing functions :

    # This is a property for the cssString attribute. No setter is included.
    @property
    def cssString(self):
        return convertRootlistToCssStr(self.rootList)


    # Saving Functions :
    def saveToFile(self, filePath):

        if not self.initialized:
            print('Object != initialized yet !')
            return None

        self.newCssString = convertRootlistToCssStr(self.rootList)
        with open(filePath, 'w+') as saveFile:
            saveFile.write(self.newCssString)
        pass
