# 256 Pipeline Tools
# DNA of EVE: common core to be used in misc modules
# TBD! Need to fix JSON file changes (CHARACTERS.json >> ASSETS.json)

import os
import json
import glob

# DEFINE COMMON VARIABLES AND PATHS
# Pipeline items
extensionHoudini = 'hipnc'
extensionRender = 'exr'
extensionFlipbook = 'jpg'
extensionCacheAnim = 'bgeo.sc'

pipelineName = 'EVE'
# cacheFolder = 'geo'
fileTypes = {'animation':'ANM', 'render':'RND', 'flipbook':'FB', 'cacheAnim':'CAN'}
# Common variables
frameStart = 1
resolution = (1280, 540)

# PATHS
# Get project root folder, defined in runHoudini.py  <P:/PROJECTS/NSI/>
rootProject = os.environ['ROOT']
# Get pipeline root folder <P:/PROJECTS/NSI/PREP/PIPELINE>
rootPipe = '{}/PREP/PIPELINE'.format(rootProject)
# Get root for Houdini project ($JOB variable), defined in runHoudini.py <P:/PROJECTS/NSI/PROD/3D>
root3D = os.environ['JOB']
# Get path to *.UI files <P:/PROJECTS/NSI/PREP/PIPELINE/EVE/ui/ui>
folderUI = '{0}/{1}/ui/ui'.format(rootPipe, pipelineName)
# Database files
databaseASSETS = '{0}/{1}/database/ASSETS.json'.format(rootPipe, pipelineName)
databaseSHOTS = '{0}/{1}/database/SHOTS.json'.format(rootPipe, pipelineName)
# Render 3D and FlipBook
rootRender3D = '{}/render'.format(root3D)


# FILE PATH (STRING) MANIPULATIONS
# File Naming convention for filePath:
# <filePath> = <fileLocation>/<fileNme>
# <fileName> = <fileCode>_<fileVersion>.<fileExtension>
# filePathExample = 'P:/PROJECTS/NSI/PROD/3D/scenes/ANIMATION/ANM_E010_S010_001.hipnc'
# folderPathExample = 'P:/PROJECTS/NSI/PROD/3D/render/010/SHOT_010/001/'

def analyzeFliePath(filePath):
    '''
    Disassemble full path (string) into components
    Example filePath: 'P:/PROJECTS/NSI/PROD/3D/scenes/ANIMATION/ANM_E010_S010_001.hipnc'

    fileLocation = P:/PROJECTS/NSI/PROD/3D/scenes/ANIMATION/
    fileName = ANM_E010_S010_001.hipnc
    fileType = ANM
    episodeCode = 010
    shotCode = 010
    fileVersion = 001
    fileCode = ANM_E010_S010
    fileExtension = hipncw
    '''

    fileName = filePath.split('/')[-1]
    fileLocation = filePath.replace('{}'.format(fileName), '')
    outputMapName = analyzeFileName(fileName)

    # File elements dictionary
    outputMapPath = {'fileLocation': fileLocation,
                     'fileName': fileName,
                     'fileType': outputMapName['fileType'],
                     'episodeCode': outputMapName['episodeCode'],
                     'shotCode': outputMapName['shotCode'],
                     'fileVersion': outputMapName['fileVersion'],
                     'fileCode': outputMapName['fileCode'],
                     'fileExtension': outputMapName['fileExtension']}

    return outputMapPath

def analyzeFileName(fileName):
    '''
    Disassemble <fileName> string
    Example <fileName> = ANM_E010_S010_001.hipnc
    '''

    fileExtension = fileName.split('.')[-1]
    fileCodeVersion = fileName.split('.')[0]

    parts = fileCodeVersion.split('_')


    fileVersion = parts[-1]
    shotCode = parts[-2][-3:]
    episodeCode = parts[-3][-3:]
    fileType = parts[0]
    fileCode = fileCodeVersion.replace('_{0}'.format(fileVersion), '')

    # Return dictionary: episodeCode, shotCode
    outputMap = {'fileType': fileType,
                 'episodeCode': episodeCode,
                 'shotCode': shotCode,
                 'fileVersion': fileVersion,
                 'fileCode': fileCode,
                 'fileExtension': fileExtension}

    return outputMap

def extractLatestVersionFile(listExisted):
    '''
    Get list of files paths (listExisted), return latest existing version + 1 (<###> string)
    '''

    listVersions = []
    for filePath in listExisted:
        listVersions.append(int(analyzeFliePath(filePath)['fileVersion']))
    latestVersion = '{:03}'.format(max(listVersions))
    return latestVersion

def extractLatestVersionFolder(filePath):
    '''
    Get FOLDER filePath, return string: latest (by number) available version ("002")
    Assume that last folder in filePath is a version (P:/<...>/.../<...>/<version>)
    '''

    # Strip last slash from path
    if filePath.endswith('/'):
        filePath = filePath[:-1]

    # Get list of folders
    version = filePath.split('/')[-1]
    pathVersions = filePath.replace(version, '')
    listVersions = os.listdir(pathVersions)
    listVersionsInt = []

    # Build list of Integer folder names
    for i in listVersions:
        if len(i) == 3:
            listVersionsInt.append(int(i))

    # Find highest folder number
    maxInt = max(listVersionsInt)
    # Build a string ('002') from highest number
    latestVersion = '{:03d}'.format(maxInt)

    return latestVersion

def buildPathNextVersion(filePath):
    '''
    Build next version of input path
    Get filePath, create new full filePath with a next version in fileName (P:/.../ANM_E010_S010_002.hipnc)
    '''

    # Disassemble file path
    fileLocation = analyzeFliePath(filePath)['fileLocation']
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
    fileVersionLatest = extractLatestVersionFile(listExisted)
    filePathLatestVersion = '{0}{1}_{2}.{3}'.format(fileLocation, fileCode, fileVersionLatest, fileExtension)

    return filePathLatestVersion

def buildFliePath(version, fileType, scenePath=None, characterName=None,  episodeCode=None, shotCode=None):
    '''
    Generate and return a full path to a file string <filePath>

    :param version: version of the file
    :param fileType: type of file to generate, eg. animation Houdini scene, geometry cache, etc
    :param scenePath: Houdini scene name (if <filePath> is generated based on the name of current scene)
    :param characterName: name of character asset
    :param episodeCode: Episode number (010)
    :param shotCode: Shot number (010)
    :return filePath: generated full path (string)
    '''

    if scenePath != None:
        filePathMap = analyzeFliePath(scenePath)

    # Render scene path
    if fileType == fileTypes['render']:
        filePath = '{0}/scenes/RENDER/{1}/SHOT_{2}/RND_E{1}_S{2}_{3}.{4}'.format(root3D,
                                                                                 episodeCode,
                                                                                 shotCode,
                                                                                 version,
                                                                                 extensionHoudini)

    # Flipbook sequence path
    elif fileType == fileTypes['flipbook']:
        fileName = 'E{0}_S{1}_{2}.$F.{3}'.format(filePathMap['episodeCode'],
                                                 filePathMap['shotCode'],
                                                 version,
                                                 extensionFlipbook)
        filePath = '{0}/{1}/SHOT_{2}/{3}/{4}'.format(rootRender3D,
                                                     filePathMap['episodeCode'],
                                                     filePathMap['shotCode'],
                                                     version,
                                                     fileName)

    # Character animation cache path
    elif fileType == fileTypes['cacheAnim']:
        filePath = '$JOB/geo/SHOTS/{0}/SHOT_{1}/{2}/GEO/{3}/E{0}_S{1}_{2}_{3}.$F.{4}'.format(
                    filePathMap['episodeCode'],
                    filePathMap['shotCode'],
                    characterName,
                    version,
                    extensionCacheAnim)

    # print filePath
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
