'''
256 Pipeline Tools
DNA of EVE: common core to be used in misc modules

# TBD! Need to fix JSON file changes (CHARACTERS.json >> ASSETS.json)

General notes.
Versions and publishing. Before we implement Shotgun and develop a publishing mechanizm with it
we will consider LATEST version of file published (which needs to be used).

'''

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
fileTypes = {'animationScene': 'ANM',
             'renderScene': 'RND',
             'renderFile': 'EXR',
             'flipbook': 'FBK',
             'cacheAnim': 'CAN'}
# Common variables
frameStart = 1
resolution = (1280, 540)

# TEMP HARDCODE TO RUN DNA IN PYCHARM!!!
# ++++++++++++++++++++++++++++++++++++++++++++
os.environ['ROOT'] = 'P:/PROJECTS/NSI'
os.environ['JOB'] = 'P:/PROJECTS/NSI/PROD/3D'
# ++++++++++++++++++++++++++++++++++++++++++++

# PATHS
# Get project root folder, defined in runHoudini.py  <P:/PROJECTS/NSI/>
rootProject = os.environ['ROOT']
# Get root for Houdini project ($JOB variable), defined in runHoudini.py <P:/PROJECTS/NSI/PROD/3D>
root3D = os.environ['JOB']
# Get pipeline root folder <P:/PROJECTS/NSI/PREP/PIPELINE>
rootPipe = '{}/PREP/PIPELINE'.format(rootProject)
# Get path to *.UI files <P:/PROJECTS/NSI/PREP/PIPELINE/EVE/ui/ui>
folderUI = '{0}/{1}/ui/ui'.format(rootPipe, pipelineName)

# Database files
databaseASSETS = '{0}/{1}/database/ASSETS.json'.format(rootPipe, pipelineName)
databaseSHOTS = '{0}/{1}/database/SHOTS.json'.format(rootPipe, pipelineName)
genesFile = '{0}/EVE/genes/genes.json'.format(rootPipe)
genes = json.load(open(genesFile))

# Houdini scene content
# Distance between nodes in scene view
nodeDistance_x = 4.0
nodeDistance_y = 0.8
# Geometry container names
nameChars = 'CHARACTERS'
nameEnv = 'ENVIRONMENT'
nameEnvAnim = 'ENVIRONMENT_ANM'
nameEnvProxy = 'ENVIRONMENT_PRX'
nameMats = 'MATERIALS'
nameCrowds = 'CROWDS'

# SETTINGS
renderSettings = {
    'common': {
            'trange': 1,                     # Frame range
            'vm_dof': 1,                     # Enable DOF
            'allowmotionblur': 1,            # Enable MB
            'vm_reflectlimit': 1,            # Reflection limit
            'vm_refractlimit': 1,            # Refraction limit
            'vm_diffuselimit': 1,            # Diffuse limit
            'vm_ssslimit': 1,                # SSS limit
            'vm_volumelimit': 1              # Volume limit
    },
    'draft': {
            'vm_samplesx': 3,                # Pixel samples X
            'vm_samplesy': 3,                # Pixel samples Y
            'vm_maxraysamples': 1            # Max Ray Samples
    },
    'production': {}
}

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
    sequenceCode = 010
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
                     'sequenceCode': outputMapName['sequenceCode'],
                     'shotCode': outputMapName['shotCode'],
                     'fileVersion': outputMapName['fileVersion'],
                     'fileCode': outputMapName['fileCode'],
                     'fileExtension': outputMapName['fileExtension']}

    return outputMapPath

def analyzeFileName(fileName):
    '''
    Disassemble <fileName> string
    Example naming conventions:
        <fileName> = ANM_E010_S010_001.hipnc
        <fileName> = CITY_001.hipnc,  CITY_ANM_001.hipnc
    '''

    fileExtension = fileName.split('.')[-1]
    fileCodeVersion = fileName.split('.')[0]

    parts = fileCodeVersion.split('_')

    # Handle different naming conventions:
    if len(parts) == 4:
        # ANM_E010_S010_001.hipnc
        fileVersion = parts[-1]
        shotCode = parts[-2][-3:]
        sequenceCode = parts[-3][-3:]
        print shotCode
        fileType = parts[0]
        fileCode = fileCodeVersion.replace('_{0}'.format(fileVersion), '')

    else:
        # CITY_001.hipnc
        fileVersion = parts[-1]
        shotCode = ''
        sequenceCode = ''
        fileType = ''
        fileCode = parts[0]

    # Return dictionary: sequenceCode, shotCode
    outputMap = {'fileType': fileType,
                 'sequenceCode': sequenceCode,
                 'shotCode': shotCode,
                 'fileVersion': fileVersion,
                 'fileCode': fileCode,
                 'fileExtension': fileExtension}

    return outputMap

def extractLatestVersionFile(listExisted):
    '''
    Get list of files paths (listExisted), return latest existing version (<###> string)
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
    :param filePath:
    :return: string latest existing version ('001')
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

def buildFliePath(version, fileType, scenePath=None, characterName=None, sequenceNumber=None, shotNumber=None):
    '''
    Generate and return a full path to a file <filePath> (string)

    :param version: version of the file
    :param fileType: type of file to generate, eg. animation Houdini scene, geometry cache, etc
    :param scenePath: Full path to Houdini scene
    :param characterName: name of character asset
    :param sequenceNumber: Episode number (sequence number = sequence code) (010)
    :param shotNumber: Shot number (010)
    :return filePath: generated full path (string)
    '''


    if scenePath != None:
        filePathMap = analyzeFliePath(scenePath)

    # Render scene path
    if fileType == fileTypes['renderScene']:
        filePath = '{0}/scenes/RENDER/{1}/SHOT_{2}/RND_E{1}_S{2}_{3}.{4}'.format(root3D,
                                                                                 sequenceNumber,
                                                                                 shotNumber,
                                                                                 version,
                                                                                 extensionHoudini)

    # Flipbook sequence path
    elif fileType == fileTypes['flipbook'] or fileType == fileTypes['renderFile']:
        # Set file extension for RENDER or FLIPBOOK
        if fileType == fileTypes['flipbook']:
            extension = extensionFlipbook
        else:
            extension = extensionRender

        fileName = 'E{0}_S{1}_{2}.$F.{3}'.format(filePathMap['sequenceCode'],
                                                 filePathMap['shotCode'],
                                                 version,
                                                 extension)
        filePath = '{0}/render/{1}/SHOT_{2}/{3}/{4}'.format(root3D,
                                                     filePathMap['sequenceCode'],
                                                     filePathMap['shotCode'],
                                                     version,
                                                     fileName)

    # Character animation cache path
    elif fileType == fileTypes['cacheAnim']:
        filePath = '$JOB/geo/SHOTS/{0}/SHOT_{1}/{2}/GEO/{3}/E{0}_S{1}_{2}_{3}.$F.{4}'.format(
                    filePathMap['sequenceCode'],
                    filePathMap['shotCode'],
                    characterName,
                    version,
                    extensionCacheAnim)

    # print 'dna.buildFilePath() [filePath] = {}'.format(filePath)
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

# DATABASE COMMUNICATIONS
# sequenceCode = sequenceNumber = '010'
# shotNumber = '010'
# shotCode = 'SHOT_010'

def getShotData(sequenceNumber, shotNumber):
    '''
    Get shot dictionary via sequence and shot numbers (010 > 010)

    To reduce database file (genes.json) before using Shotgun we don`t store sequences data there.
    So we looking for shots iterating shots dict, getting linked sequence, getting proper shot (shot > sequence > shot)
    Having Shotgun in place will allow to iterAte sequences and then find proper shot (sequence > shot)
    :param sequenceNumber: string '010'
    :param shotNumber: string '010'
    :return shot: shot dictionary
    {'code': 'SHOT_010', 'sg_cut_out': 200, 'sg_sequence': {'name': '010'}, 'assets': [{'name': 'CITY'}, {'name': 'ROMA'}]}
    '''

    shotCode = 'SHOT_{0}'.format(shotNumber)

    for shot in genes['SHOTS']:
        # Get shot > sequence data
        if shot['sg_sequence']['name'] == sequenceNumber:
            # Get shot data
            if shot['code'] == shotCode:
                return shot
            else:
                print 'dna.getStotData(): There is no data for shot E{0}_S{1}'.format(sequenceNumber, shotNumber)

def getAssetsDataByShot(assetData_short):
    '''
    Get full dictionaries of assets LINKED TO SHOT

    :param assetData_short: asset data dictionaries from the shot entity
    :return assetsData_full: list of full dictionaries of assets linked to shot
    '''

    # assetsData = [{'name': 'CITY'}, {'name': 'ROMA'}]

    assetsData_full = []

    for asset in assetData_short:
        for assetData_full in genes['ASSETS']:
            if assetData_full['code'] == asset['name']:
                assetsData_full.append(assetData_full)

    return assetsData_full

def getAssetDataByType(assetsData, assetType):
    '''
    Get data of particular type (char, env, prop) for the shot from input asset data dictionary (all shot assets).

    :param assetsData: list of all assets dictionaries linked to shot
    :param assetType: 'Environment', 'Character', 'Prop'
    :return:
    '''

    # assetsData = list of assets dictionaries linked to shot
    # assetType = 'Environment', 'Character', 'Prop'

    if assetType == 'Environment':
        for assetData in assetsData:
            if assetData['sg_asset_type'] == assetType:
                return assetData

    if assetType == 'Character':
        listCharacters = []
        for assetData in assetsData:
            if assetData['sg_asset_type'] == assetType:
                listCharacters.append(assetData)
        return listCharacters

def getShotGenes(sequenceNumber, shotNumber):
    '''
    Pull asset and shot data from the database:
       - Get data for the current shot
       - Get assets linked to shot
       - Organize assets by types (characters, env, props)

    shotData = {
           'sg_sequence': {'name': '010'},
           'code': 'SHOT_010', 'sg_cut_out': 200,
           'assets': [{'name': 'CITY'}, {'name': 'ROMA'}]}

    environmentData = {
           'code': 'CITY',
           'sg_asset_type': 'Environment'
           'hda_name': 'city',
           'light_hda': {'hda_name': 'city_lights', 'name': 'CITY_LIT'},
           'animation_hda': {'hda_name': 'city_anm', 'name': 'CITY_ANM'},
           'crowds_hda': {'hda_name': 'city_crowds', 'name': 'CROWDS'},
           'proxy_hda': {'hda_name': 'city_prx', 'name': 'CITY_PRX'}}

    charactersData = [
           {'code': 'ROMA',
           'sg_asset_type': 'Character'}]

    :param sequenceNumber:
    :param shotNumber:
    :return:
    '''

    shotData = getShotData(sequenceNumber, shotNumber)
    assetsData = getAssetsDataByShot(shotData['assets'])
    environmentData = getAssetDataByType(assetsData, 'Environment')
    charactersData = getAssetDataByType(assetsData, 'Character')

    return shotData, assetsData, environmentData, charactersData

# shotData = getShotData('010', '010')
# assetsData = getAssetsDataByShot(shotData['assets'])
# envData = getAssetDataByType(assetsData,  'Environment')
# charData = getAssetDataByType(assetsData,  'Character')

# analyzeFileName(' ANM_E010_S010_001.hipnc')