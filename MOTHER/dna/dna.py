# 256 Pipeline Tools
# DNA of MOTHER: common core to be used in misc modules

import os
import json


def analyzePath_HIP(path):
    '''
    Disassemble Houdini HIP file to get shot data from it
    '''
    pathParts = path.split('/')

    fileName = pathParts[-1]
    codeShot = pathParts[-2].replace('SHOT_', '')
    codeSequense = pathParts[-3]

    return codeSequense, codeShot

def getCharacterData(charcterName):
    # LOAD CHARACTER DATA FROM DATABASE
    rootMother = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')
    dataFile = '{0}/database/CHARACTERS.json'.format(rootMother)
    dataCharacters = json.load(open(dataFile))
    characterData = dataCharacters[charcterName]
    return characterData

def setupCharacterMaterials(material, characterData):
    '''
    Asign materials to a character (via groups)
    Param: mat - material SOP node
    '''
    n = 1
    groupLists = characterData['MAT'].keys()
    matNumber = len(groupLists)
    material.parm('num_materials').set(matNumber)
    for groupList in groupLists:
        material.parm('group{}'.format(n)).set(groupList)
        material.parm('shop_materialpath{}'.format(n)).set(characterData['MAT'][groupList])
        n += 1
