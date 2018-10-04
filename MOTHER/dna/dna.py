# 256 Pipeline Tools
# DNA of MOTHER: common core to be used in misc modules
# TBD! Need to fix JSON file changes (CHARACTERS.json >> ASSETS.json)

import os
import json

# Get Mother root folder
rootMother = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')
# Database file
filePath = '{0}/database/ASSETS.json'.format(rootMother)

def analyzePath(filePath):
    '''
    Disassemble string path into components
    File Naming convention:
    <filePath> =
    <filePath> = <fileLocation>/<fileNme>
    <fileName> = <fileCode>_<fileVersion>.<fileExtenstion>
    '''

    fileName = filePath.split('/')[-1]
    fileExtenstion = fileName.split('.')[-1]
    fileVersion = fileName.split('.')[0].split('_')[-1]
    fileCode = fileName.replace('_{0}.{1}'.format(fileVersion, fileExtenstion), '')
    fileLocation = filePath.replace('{}'.format(fileName), '')

    return fileLocation, fileName, fileCode, fileVersion, fileExtenstion

def analyzePath_HIP(path):
    '''
    Disassemble Houdini HIP file path string to get shot data from it
    '''
    pathParts = path.split('/')

    fileName = pathParts[-1]
    codeShot = pathParts[-2].replace('SHOT_', '')
    codeSequense = pathParts[-3]

    return codeSequense, codeShot

def getCharacterData(charcterName):
    '''
    Load character data from database
    :param charcterName: Name of Character
    :return: Character data dictionary
    '''

    dataCharacters = json.load(open(filePath))
    characterData = dataCharacters['CHARACTERS'][charcterName]
    return characterData

def setCharacterData(characterName, section, characterData):
    with open(filePath, 'r+') as fileData:
        data = json.load(fileData)
        data['CHARACTERS'][characterName][section] = characterData
        fileData.seek(0)  # reset file position to the beginning
        json.dump(data, fileData, indent=4)
        fileData.truncate()  # remove remaining part
        print '>> Materials data saved to {}'.format(filePath)

def setupCharacterMaterials(materialNode, characterData):
    '''
    Assign materials to a character (via groups) for conversion FBX to Geometry caches
    Param: materialNode - material SOP node
    '''
    n = 1
    # Get list of materials for the CHARACTER
    listMaterials = characterData['materials'].keys()
    materialNode.parm('num_materials').set(len(listMaterials))
    for material in listMaterials:
        materialPath = '/obj/MATERIALS/GENERAL/{}'.format(material) # Path to materials in Houdini scene
        materialNode.parm('group{}'.format(n)).set(characterData['materials'][material]) # Set groups
        materialNode.parm('shop_materialpath{}'.format(n)).set(materialPath) # Set materials
        n += 1
