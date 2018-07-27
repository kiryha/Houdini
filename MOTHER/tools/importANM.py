# 256 Pipeline Tools
# Import Character Caches to a render scene

import hou

from MOTHER.dna import dna
reload(dna)

# Hardcoded values
fileVersion = '001'
characterName = 'ROMA'

# Get shot and sequence number from scene name
codeSequense, codeShot = dna.analyzePath_HIP(hou.hipFile.path())

# Get scene root
OBJ = hou.node('/obj/')


def createCharacterCache(characterName):
    '''
    Create CHARACTERS container to hold character caches
    '''

    # Build cache path
    pathCache = '$JOB/geo/SHOTS/{0}/SHOT_{1}/{2}/GEO/{3}/E{0}_S{1}_{2}_{3}.bgeo.sc'.format(codeSequense, codeShot,
                                                                                           characterName, fileVersion)
    # Check if CHARACTERS node exists in scene
    chars = hou.node('/obj/{}'.format('CHARACTERS'))

    if not chars:
        # Create CHARACTERS node if its not exists in scene
        chars = OBJ.createNode('geo', run_init_scripts=False)
        chars.setName('CHARACTERS')

    # Create and setup File Cache SOP
    characterCache = chars.createNode('filecache')
    characterCache.setName('GEO_{}'.format(characterName))
    characterCache.parm('loadfromdisk').set(1)
    characterCache.parm('file').set(pathCache)

    # Create and setup OUT null SOP
    out = chars.createNode('null')
    out.setNextInput(characterCache)
    out.setName('OUT_{}'.format(characterName))

    # Set display flags
    out.setDisplayFlag(1)
    out.setRenderFlag(1)

    # Layout geometry content in Network View
    chars.layoutChildren()
    print '>> IMPORTED CACHES FOR {}'.format(characterName)

def run():
    createCharacterCache(characterName)