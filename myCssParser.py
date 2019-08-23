from .tinycss2 import *
from collections import OrderedDict
from aqt.utils import showInfo


def createRootDictFromFile(filePath):
    itemsInFile = getListOfItemsFromFile(filePath)

    rootDict = OrderedDict()
    rootList = []

    for item in itemsInFile:

        if item.type == 'whitespace' or item.type == 'comment':
            rootList.append(item)

        else:
            rule = item  # just for clarification and not needed
            ruleName = serialize(rule.prelude).strip(' ')
            newDict = convertRuleContentToOrderedDict(rule.content)
            rootList.append((ruleName, newDict))  # append the new rule as a tuple

    rootDict[items] = rootList

    return rootDict


def createRootListFromFile(filePath):

    itemsInFile = getListOfItemsFromFile(filePath)

    rootList = []

    for item in itemsInFile:

        if item.type == 'whitespace' or item.type == 'comment':
            rootList.append(item)

        else:
            rule = item  # just for clarification and not needed
            ruleName = serialize(rule.prelude).strip(' ')
            newDict = convertRuleContentToOrderedDict(rule.content)
            rootList.append((ruleName, newDict))  # append the new rule as a tuple

    return rootList


def createRootListFromCssString(cssString):

    itemsInFile = getListOfItemsFromCssString(cssString)
    # showInfo('after getListOfItemsFromCssString')


    rootList = []

    for item in itemsInFile:

        if item.type == 'whitespace' or item.type == 'comment':
            rootList.append(item)

        else:
            rule = item  # just for clarification and not needed
            ruleName = serialize(rule.prelude).strip(' ')
            newDict = convertRuleContentToOrderedDict(rule.content)
            if len(newDict) is not 0:  # may cause things to disappear
                rootList.append((ruleName, newDict))  # append the new rule as a tuple

    return rootList


def getListOfItemsFromFile(file, skip_whitespace_bool=False, skip_comments_bool=False):

    with open(file, 'r') as f:
        fileContent = f.read()
        return parse_stylesheet(fileContent, skip_whitespace=skip_whitespace_bool, skip_comments=skip_comments_bool)


def getListOfItemsFromCssString(string, skip_whitespace_bool=False, skip_comments_bool=False):
    fileContent = string
    return parse_stylesheet(fileContent, skip_whitespace=skip_whitespace_bool, skip_comments=skip_comments_bool)


def convertRuleContentToOrderedDict(ruleContent):
    '''
    This function converts a single rule.content for a single rule, which is a list of declarations
    into an actual dictionnary with key value data for css attributes.
    '''
    orderdRule = OrderedDict()
    a = parse_declaration_list(ruleContent, skip_comments=True, skip_whitespace=True)
    lastitem = None
    for dec in a:
        # print(dec)
        if dec.type == 'error':
            showInfo(dec.kind)
            showInfo('Some kind of error in CSS code (Last correct item was : ' + lastitem + ')\n' + dec.message)
        if dec.type == 'whitespace' or dec.type == 'comment':  # extra security
            continue
        else:
            orderdRule[dec.name] = str(serialize(dec.value)).strip(' ')
            lastitem = dec.name
    return orderdRule


def convertRootlistToCssStr(rootList):
    '''
    This function takes a rootList that is made of items and tries to comvert them into a string (masterStr) that is a readable css file.
    If the item is a comment or whitespace, it serializes it and then adds the actual string value to masterStr.
    If the item is a tuple it know its is a rule and first item in it is the name, second item is thr orderedDict of attributes.
    '''
    masterStr = ''
    # showInfo('makin babies')
    for item in rootList:

        if type(item) == tuple:
            masterStr = masterStr + item[0] + " {"

            if item[1] is None:
                continue
            for key, value in item[1].items():
                masterStr = masterStr + "\n    " + key + ": " + str(value).strip(' ') + ";"

            masterStr = masterStr + "\n" + "}\n"
            # masterStr = masterStr[:len(masterStr) - 2] + "\n" + "}"

            pass
        # This next part cleans the string so that there is only one empty line between classes.
        else:
            # masterStr = masterStr + serialize([item])
            if item.type == 'whitespace':
                # print('String : -' + masterStr[-2:] + '- end')
                if masterStr[-2:].strip() == '':
                    pass
                else:
                    masterStr = masterStr + '\n'
            else:
                masterStr = masterStr + serialize([item])

    return masterStr
