'''
Export CHARACTERs and CAMERA animation data from animation scene
CAMERA should meet naming convention E<sequenceNumber>_S<shotNumber>

Currently only builds cache network for ROMA character. Need to run file caching manually
'''
import os
import hou
from EVE.dna import dna
reload(dna)

# INITIALIZE DATA
sceneRoot = hou.node('/obj/')
scenePath = hou.hipFile.path()
pathMap = dna.analyzeFliePath(scenePath)
sequenceNumber = pathMap['sequenceNumber']
shotNumber = pathMap['shotNumber']
shotGenes = dna.getShotGenes(sequenceNumber, shotNumber)
characterData = shotGenes['charactersData']

def exportCamera():
    '''
    Export shot camera
    Two options avalable, ABC and HIP. Use HIP currently.
    :return:
    '''

    print '>> Exporting camera...'

    cameraName = dna.cameraName.format(sequenceNumber, shotNumber)
    camera = hou.node('obj/{}'.format(cameraName))
    pathCamera = dna.buildFilePath('001', dna.fileTypes['cacheCamera'], scenePath=scenePath)
    dna.createFolder(dna.convertPathCache(pathCamera))
    # Set camera parameters
    dna.setCameraParameters(camera)

    # HIP export
    listCameraNodes = dna.collectCamera(camera)
    # Export camera to a file
    sceneRoot.saveItemsToFile(listCameraNodes, pathCamera)

    """
    # ABC export
    # Get Camera parent nodes
    listCameraNodes = '{}'.format(camera.name())
    for i in camera.inputAncestors():
        listCameraNodes += ' {}'.format(i.name())


    # Create ROP network
    ROP = sceneRoot.createNode('ropnet')
    ABC = ROP.createNode('alembic')
    ABC.parm('trange').set(1)
    ABC.parm('filename').set(pathCamera)
    ABC.parm('objects').set(listCameraNodes)
    ABC.parm('execute').pressButton()
    ROP.destroy()
    """
    print '>> Exporting camera done: {}'.format(pathCamera)

def getRenderNode(container):
    '''
    Get and return node with render flag inside <container> node
    :param container:
    :return:
    '''

    for node in container.children():
        if node.isRenderFlagSet() == 1:
            return node

def createCacheNetwork():
    '''
    Create output character nodes for exporting cache from animation scene
    Expect each character node network exists in geometry container named as character (ROMA)
    :return:
    '''

    print '>> Create Character caches network ...'

    for character in characterData:
        characterName = character['code']
        charContainer = hou.node('/obj/{0}'.format(characterName))
        if charContainer is not None:
            renderNode = getRenderNode(charContainer)

            # Check if character has proper network:
            if renderNode.name() != 'OUT_{}'.format(characterName):
                # Create trail for Motion Blur
                trail = charContainer.createNode('trail', 'MB_{}'.format(characterName))
                trail.parm('result').set(3)

                # Create Cache node
                cache = charContainer.createNode('filecache', dna.fileCacheName.format(characterName))
                # Build path to a file cache
                pathCache = dna.buildFilePath('001',
                                              dna.fileTypes['cacheAnim'],
                                              scenePath=scenePath,
                                              characterName=characterName)

                cache.parm('file').set(pathCache)
                cache.parm('loadfromdisk').set(1)

                # Create OUT null
                null = charContainer.createNode('null', 'OUT_{}'.format(characterName))

                # Link nodes
                trail.setInput(0, renderNode)
                cache.setInput(0, trail)
                null.setInput(0, cache)

                # Layout and set render flag
                null.setDisplayFlag(1)
                null.setRenderFlag(1)
                charContainer.layoutChildren()

                print '>> Character caches network created!'

        else:
            print '>> There is no character node named {}'.format(characterName)



def exportCharacters():

    print '>> Exporting Characters...'

    for character in characterData:
        characterName = character['code']
        # Get Character File Cache node
        fileCacheName = dna.fileCacheName.format(characterName)
        FC = hou.node('/obj/{0}/{1}'.format(characterName, fileCacheName))
        FC.parm('execute').pressButton()

        # Need to check existing cache and ask user overwrite or save next version
        # pathCache = FC.parm('file').rawValue()

    print '>> Exporting Characters done!'

def ecxportAnimation():

    exportCamera()
    createCacheNetwork()
    exportCharacters()

def run():
    print '>> Exporting Animation...'
    ecxportAnimation()
    print '>> Done!'