'''
Export CHARACTER animation data from animation scene

Currently for ROMA only
'''

import hou
from EVE.dna import dna
reload(dna)

characterName = 'ROMA'

CHARACTERS = hou.node('/obj/CHARACTERS')


def getRenderNode(container):
    '''
    Get and return node with render flag inside <container> node
    :param container:
    :return:
    '''

    for node in container.children():
        if node.isRenderFlagSet() == 1:
            return node

renderNode = getRenderNode(CHARACTERS)

cache = CHARACTERS.createNode('filecache', 'CACHE_{}'.format(characterName))

pathCache = dna.buildFliePath('001',
                               dna.fileTypes['cacheAnim'],
                               scenePath=hou.hipFile.path(),
                               characterName=characterName)
cache.parm('file').set(pathCache)
null = CHARACTERS.createNode('null', 'OUT_{}'.format(characterName))
cache.setInput(0, renderNode)
null.setInput(0, cache)
# null.setDisplayFlag(1)
# null.setRenderFlag(1)
CHARACTERS.layoutChildren()
