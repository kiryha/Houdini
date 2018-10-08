# 256 Pipeline Tools
# DNA of MOTHER: common core to be used in misc modules
# TBD! Need to fix JSON file changes (CHARACTERS.json >> ASSETS.json)

import os
import json
import glob

# DEFINE COMMON VARIABLES AND PATHS
# Pipeline items
extensionHoudini = 'hipnc'
pipelineName = 'MOTHER'

# Get project root folder, defined in runHoudini.py  <P:/PROJECTS/NSI/>
rootProject = os.environ['ROOT']
# Get pipeline root folder <P:/PROJECTS/NSI/PREP/PIPELINE>
rootPipe = '{}/PREP/PIPELINE'.format(rootProject)
# Get root for Houdini project ($JOB variable), defined in runHoudini.py <P:/PROJECTS/NSI/PROD/3D>
root3D = os.environ['JOB']
# Get path to *.UI files <P:/PROJECTS/NSI/PREP/PIPELINE/MOTHER/ui/ui>
folderUI = '{0}/{1}/ui/ui'.format(rootPipe, pipelineName)
# Database files
databaseASSETS = '{0}/{1}/database/ASSETS.json'.format(rootPipe, pipelineName)
databaseSHOTS = '{0}/{1}/database/SHOTS.json'.format(rootPipe, pipelineName)


# FILE PATH (STRING) MANIPULATIONS
# File Naming convention for filePath:
# <filePath> = <fileLocation>/<fileNme>
# <fileName> = <fileCode>_<fileVersion>.<fileExtension>
# filePathExample = 'P:/PROJECTS/NSI/PROD/3D/scenes/ANIMATION/ANM_E010_S010_001.hipnc'

def analyzeFliePath(filePath):
    '''
    Disassemble string path into components
    '''

    fileName = filePath.split('/')[-1]
    fileExtension = fileName.split('.')[-1]
    fileVersion = fileName.split('.')[0].split('_')[-1]
    fileCode = fileName.replace('_{0}.{1}'.format(fileVersion, fileExtension), '')
    fileLocation = filePath.replace('{}'.format(fileName), '')

    # Return dictionary: fileLocation, fileName, fileCode, fileVersion, fileExtension
    outputMap = {'fileLocation': fileLocation,
                 'fileName': fileName,
                 'fileCode': fileCode,
                 'fileVersion': fileVersion,
                 'fileExtension': fileExtension}

    return outputMap

def analyzeFileCode(fileCode):
    '''
    Disassemble <fileCode> part of the <fileName> to get shot data from it
    fileCodeExample = ANM_E010_S010
    '''

    shotCode = fileCode.split('_')[-1]
    episodeCode = fileCode.split('_')[-2]

    # Return dictionary: episodeCode, shotCode
    outputMap = {'episodeCode': episodeCode,
                 'shotCode': shotCode}

    return outputMap

def extractLatestVersion(listExisted):
    '''
    Get list of files paths (listExisted), return latest existing version + 1 (<###> string)
    '''

    listVersions = []
    for filePath in listExisted:
        listVersions.append(int(analyzeFliePath(filePath)['fileVersion']))
    latestVersion = '{:03}'.format(max(listVersions) + 1)
    return latestVersion

def buildPathNextVersion(filePath):
    '''
    Get filePath, create new filePath with a next version in fileName
    '''

    # Disassemble file path
    fileLocation= analyzeFliePath(filePath)['fileLocation']
    fileCode = analyzeFliePath(filePath)['fileCode']
    fileVersion = analyzeFliePath(filePath)['fileVersion']
    fileExtension = analyzeFliePath(filePath)['fileExtension']

    fileVersionNext = '{:03}'.format(int(fileVersion) + 1)
    filePathNextVersion = '{0}{1}_{2}.{3}'.format(fileLocation, fileCode, fileVersionNext, fileExtension)

    return filePathNextVersion

def buildPathLatestVersion(filePath):
    '''
    Get filePath, create new filePath with a latest available version in fileName
    '''

    # Disassemble file path
    fileLocation= analyzeFliePath(filePath)['fileLocation']
    fileCode = analyzeFliePath(filePath)['fileCode']
    fileExtension = analyzeFliePath(filePath)['fileExtension']

    listExisted = glob.glob('{0}{1}_*.{2}'.format(fileLocation, fileCode, fileExtension))
    fileVersionLatest = extractLatestVersion(listExisted)
    filePathLatestVersion = '{0}{1}_{2}.{3}'.format(fileLocation, fileCode, fileVersionLatest, fileExtension)

    return filePathLatestVersion

def buildFliePath(episode, shot, sceneType):
    '''
    Build a File Path
    :param episode: String episode number <###>
    :param shot: String shot number <###>
    :param sceneType: String file type (animation, render, fx etc)
    :return:
    '''

    filePath = None

    if sceneType == 'RND':
        filePath = '{0}/scenes/RENDER/{1}/SHOT_{2}/RND_E{1}_S{2}_001.{3}'.format(root3D, episode, shot, extensionHoudini)
        #print filePath

    return filePath

def getCharacterData(charcterName):
    '''
    Load character data from database
    :param charcterName: Name of Character
    :return: Character data dictionary
    '''

    dataCharacters = json.load(open(databaseASSETS))
    characterData = dataCharacters['CHARACTERS'][charcterName]
    return characterData

def setCharacterData(characterName, section, characterData):
    with open(databaseASSETS, 'r+') as fileData:
        data = json.load(fileData)
        data['CHARACTERS'][characterName][section] = characterData
        fileData.seek(0)  # reset file position to the beginning
        json.dump(data, fileData, indent=4)
        fileData.truncate()  # remove remaining part
        print '>> Materials data saved to {}'.format(databaseASSETS)

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
