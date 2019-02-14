# 256 Pipeline Tools
# Import Character Caches to a render scene

import hou

from EVE.dna import dna
reload(dna)

# Get shot and sequence number from the scene name
scenePath = hou.hipFile.path()
pathMap = dna.analyzeFliePath(scenePath)
sequenceNumber = pathMap['sequenceNumber']
shotNumber = pathMap['shotNumber']
# Get shot data
shotGenes = dna.getShotGenes(sequenceNumber, shotNumber)
# Get scene root
sceneRoot = hou.node('/obj/')


def importCameraAnim():
    # Build camera path to the 001 version of ABC: '$JOB/geo/SHOTS/010/SHOT_010/CAM/E010_S010_001.abc'
    pathCamera = dna.buildFilePath('001', dna.fileTypes['cacheCamera'], scenePath=scenePath)
    # Build path latest version. TBD
    cameraName = dna.nameCamera.format(sequenceNumber, shotNumber)
    CAM = sceneRoot.createNode('alembicarchive', cameraName)
    CAM.parm('fileName').set(pathCamera)
    CAM.parm('buildSubnet').set(0)
    CAM.parm('buildHierarchy').pressButton()
    CAM.setPosition([0, -2*dna.nodeDistance_y])

def importCharacterAnim():
    '''
    Import character animation for the current render scene: set FileCache nodes paths.

    pathCache = $JOB/geo/SHOTS/010/SHOT_010/ROMA/GEO/001/E010_S010_ROMA_001.$F.bgeo.sc
    :return:
    '''
    # For each character in shot
    for character in shotGenes['charactersData']:
        characterName = character['code']
        # Get character container
        CHAR = hou.node('/obj/{0}'.format(characterName))
        # Create File Cache SOP
        CACHE = CHAR.createNode('filecache', dna.fileCacheName.format(characterName))

        # BUILD CACHE PATH (LATEST VERSION)
        # Build a path to the 001 version of cache
        pathCache = dna.buildFilePath('001',
                                      dna.fileTypes['cacheAnim'],
                                      scenePath=scenePath,
                                      characterName=characterName)

        # Check latest existing version, build new path if exists
        pathCacheFolder = dna.convertPathCache(pathCache)
        latestCacheVersion = dna.extractLatestVersionFolder(pathCacheFolder)
        if latestCacheVersion != '001':
            pathCache = dna.buildFilePath(latestCacheVersion,
                                          dna.fileTypes['cacheAnim'],
                                          scenePath=scenePath,
                                          characterName=characterName)

        CACHE.parm('file').set(pathCache)
        CACHE.parm('loadfromdisk').set(1)
        NULL = CHAR.createNode('null', 'OUT_{0}'.format(characterName))
        NULL.setInput(0, CACHE)
        NULL.setDisplayFlag(1)
        NULL.setRenderFlag(1)
        CHAR.layoutChildren()

def run():
    importCameraAnim()
    importCharacterAnim()
    print '>> Animation imported!'