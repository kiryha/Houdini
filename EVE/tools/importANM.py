# 256 Pipeline Tools
# Import Character Caches and camera animation to a render scene.

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
    '''
    Import camera to the render scene
    :return:
    '''

    print '>> Importing Camera...'

    # HIP format
    # Check if shot camera exists - skip import
    cameraName = dna.cameraName.format(sequenceNumber, shotNumber)
    camera = hou.node('/obj/{}'.format(cameraName))

    if camera:
        print '>>>> Camera exists in scene! Delete camera and import again to update animation.'
        # listCameraNodes = dna.collectCamera(camera)
    else:
        # Build camera path to the 001 version of ABC: '<root3D>/geo/SHOTS/010/SHOT_010/CAM/E010_S010_001.hiplc'
        pathCamera = dna.buildFilePath('001', dna.fileTypes['cacheCamera'], scenePath=scenePath)
        # Build path latest version. TBD
        sceneRoot.loadItemsFromFile(pathCamera)


    # ABC format
    """
    # Build camera path to the 001 version of ABC: '$JOB/geo/SHOTS/010/SHOT_010/CAM/E010_S010_001.abc'
    pathCamera = dna.buildFilePath('001', dna.fileTypes['cacheCamera'], scenePath=scenePath)
    # Build path latest version. TBD
    cameraName = dna.nameCamera.format(sequenceNumber, shotNumber)
    CAM = sceneRoot.createNode('alembicarchive', cameraName)
    CAM.parm('fileName').set(pathCamera)
    CAM.parm('buildSubnet').set(0)
    CAM.parm('buildHierarchy').pressButton()
    CAM.setPosition([0, -2*dna.nodeDistance_y])
    """

    print '>> Importing Camera done!'

def importCharacterAnim():
    '''
    Import character animation for the current render scene: set FileCache nodes paths.

    pathCache = $JOB/geo/SHOTS/010/SHOT_010/ROMA/GEO/001/E010_S010_ROMA_001.$F.bgeo.sc
    :return:
    '''

    # For each character in shot
    for characterData in shotGenes['charactersData']:
        characterName = characterData['code']
        fileCacheName = dna.fileCacheName.format(characterName)

        # Get character container or create if not exists
        characterContainer = hou.node('/obj/{0}'.format(characterName))
        if not characterContainer:
            characterContainer = dna.createContainer(sceneRoot, characterName, mb=1)


        # Get Character Cache node or create if not exists
        characterCache = hou.node('/obj/{0}/{1}'.format(characterName, fileCacheName))
        if not characterCache:
            # Create File Cache SOP
            characterCache = characterContainer.createNode('filecache', fileCacheName)
            characterNull = characterContainer.createNode('null', 'OUT_{0}'.format(characterName))
            characterNull.setInput(0, characterCache)
            characterNull.setDisplayFlag(1)
            characterNull.setRenderFlag(1)
            characterContainer.layoutChildren()
            print '>>>> Created Cache Network: {0}'.format(fileCacheName)

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

        # Set path to character cache
        characterCache.parm('file').set(pathCache)
        characterCache.parm('loadfromdisk').set(1)


def run():
    print '>> Importing animation...'
    importCameraAnim()
    importCharacterAnim()
    print '>> Animation imported!'