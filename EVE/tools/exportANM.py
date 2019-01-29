'''
Export CHARACTER animation data from animation scene

Currently only builds cache network for  ROMA character. Need to run file caching manually
'''
import os
import hou
from EVE.dna import dna
reload(dna)

characterName = 'ROMA'
CHARACTERS = hou.node('/obj/{0}'.format(dna.nameChars))

# INITIALIZE DATA
sceneRoot = hou.node('/obj/')
scenePath = hou.hipFile.path()
scenePathData = dna.analyzeFliePath(scenePath)


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

    :return:
    '''

    # Build path to a file cache
    pathCache = dna.buildFilePath('001',
                                  dna.fileTypes['cacheAnim'],
                                  scenePath= scenePath,
                                  characterName=characterName)

    renderNode = getRenderNode(CHARACTERS)

    # Create trail for Motion Blur
    trail = CHARACTERS.createNode('trail', 'MB_{}'.format(characterName))
    trail.parm('result').set(3)

    # Create Cache node
    cache = CHARACTERS.createNode('filecache', 'CACHE_{}'.format(characterName))
    cache.parm('file').set(pathCache)
    cache.parm('loadfromdisk').set(1)

    # Create OUT null
    null = CHARACTERS.createNode('null', 'OUT_{}'.format(characterName))

    # Link nodes
    trail.setInput(0, renderNode)
    cache.setInput(0, trail)
    null.setInput(0, cache)

    # Layout and set render flag
    null.setDisplayFlag(1)
    null.setRenderFlag(1)
    CHARACTERS.layoutChildren()

def ecxportAnimation():

    # Create nodes network for export character data
    createCacheNetwork()

    # Export camera
    listExport = [] # All camera nodes (if camera parented to nulls)
    camera = sceneRoot.node(dna.nameCamera.format(scenePathData['sequenceCode'], scenePathData['shotCode']))
    listExport.extend(camera.inputAncestors())
    listExport.append(camera)
    cameraPath = dna.buildFilePath('001', dna.fileTypes['camera'], scenePath=scenePath)
    # Create camera folder
    dna.createFolder(cameraPath)
    # Export camera to a file
    sceneRoot.saveItemsToFile(listExport, cameraPath)



def run():
    ecxportAnimation()