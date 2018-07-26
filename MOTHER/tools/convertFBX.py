# 256 Pipeline tools
# Convert animated mixamo FBX subnetwork to Geometry cache
# Import FBX into Houdini, select FBX subnetworks, run script in Python Source Editor
# Cache geometry in GEO_<FBX name> subnetworks

import hou

# DATABASE DRAFT

# CHARACTERS DICTIONARY
# Materials dictionary (MAT):
# KEY = groups string (list of group names divided by space), VALUE = path to material in scene (from MATLIB HDA) for that list of groups
CHARACTERS = {'ROMA': {
    'MAT': {
        'ROMA_EYE_L_OUT ROMA_EYE_R_OUT': '/obj/MATERIALS/GENERAL/GEN_EYE',
        'ROMA_EYE_L_BLACK ROMA_EYE_R_BLACK': '/obj/MATERIALS/GENERAL/GEN_PUPIL',
        'ROMA_ARMS ROMA_BEARD ROMA_HEAD ROMA_IRON ROMA_PENS ROMA_SHOES ROMA_TSHIRT': '/obj/MATERIALS/GENERAL/GEN_BASE'
    }
}}

# Define common variables
fileVersion = '001'
characterName = 'ROMA'

# Get selected FBX container and scene root
FBXS = hou.selectedNodes()
OBJ = hou.node('/obj/')


def checkConditions():
    '''
    Check if environment conditions allows to run script without errors
    '''
    if not FBXS:  # If user select anything
        print '>> Nothing selected! Select FBX subnetwork!'
        return 0


def setupCharacterMaterials(mat, characterName):
    '''
    Asign materials to a character (via groups)
    Param: mat - material SOP node
    '''
    n = 1
    groupLists = CHARACTERS[characterName]['MAT'].keys()
    matNumber = len(groupLists)
    mat.parm('num_materials').set(matNumber)
    for groupList in groupLists:
        mat.parm('group{}'.format(n)).set(groupList)
        mat.parm('shop_materialpath{}'.format(n)).set(CHARACTERS[characterName]['MAT'][groupList])
        n += 1


def getLastFrame(node):
    '''
    Return last frame of translate X animation from input node
    '''
    for i in node:
        keys = i.parm('tx').keyframes()
        listKeys = []
        for key in keys:
            listKeys.append(key.frame())
        lastFrame = int(sorted(listKeys)[-1])
        return lastFrame


def convert_FBX(FBX):
    '''
    Create Geometry node and import all FBX part inside
    '''
    # Create Geometry node to store FBX parts
    geometry = OBJ.createNode('geo', run_init_scripts=False)
    nameGEO = 'GEO_{}'.format(FBX.name())

    # Check if converted geometry exists
    if hou.node('/obj/{}'.format(nameGEO)) == None:
        geometry.setName(nameGEO)
        geometry.moveToGoodPosition()
        # Get all paerts inside FBX container
        geometry_FBX = [node for node in FBX.children() if node.type().name() == 'geo']
        mixamoRoot = [node for node in FBX.children() if node.name() == 'mixamorig_Hips']
        lastFrame = getLastFrame(mixamoRoot)

        # Create merge node for parts
        merge = geometry.createNode('merge')
        merge.setName('merge_parts')

        # Replicate FBX structure in Geometry node
        for geo in geometry_FBX:
            # Create Object Merge node
            objectMerge = geometry.createNode('object_merge')
            objectMerge.setName('GEO_{}'.format(geo.name()))
            # Set path to FBX part object
            objectMerge.parm('objpath1').set(geo.path())
            objectMerge.parm('xformtype').set(1)
            # Create Group node
            group = geometry.createNode('groupcreate')
            group.setName('{}'.format(geo.name()))
            group.parm('groupname').set('$OS')
            # Link Group to Object Merge
            group.setNextInput(objectMerge)
            # Link part to Merge
            merge.setNextInput(group)

        # Create Material Node
        mat = geometry.createNode('material')
        mat.setNextInput(merge)
        mat.setName('MATERIAL')
        # Asign Materials to a character
        setupCharacterMaterials(mat, characterName)

        # Create groupdelete node
        gdel = geometry.createNode('groupdelete')
        gdel.setNextInput(mat)
        gdel.setName('CLEAN')
        gdel.parm('group1').set('*')

        # Create FileCache
        fileName = FBX.name().split('_')[0]
        cache = geometry.createNode('filecache')
        cache.parm('file').set(
            '$JOB/lib/ANIMATION/CHARACTERS/{2}/GEO/{0}/{1}/{0}_{1}.$F.bgeo.sc'.format(fileName, fileVersion,
                                                                                      characterName))
        cache.parm('f2').deleteAllKeyframes()  # Delete expression on end frame
        cache.parm('f2').set(lastFrame)  # Sete end frame
        cache.setNextInput(gdel)
        cache.setName('CACHE_ANIM')

        # Set File CacheNode flags to Render
        cache.setDisplayFlag(1)
        cache.setRenderFlag(1)
        # Layout geometry content in Nwtwork View
        geometry.layoutChildren()
    else:
        # If the converted node exists
        print '>> NETWORK <{}> EXISTS! SKIP CONVERSION.'.format(nameGEO)


# Check if everything is fine and run script
if checkConditions() != 0:
    # Get FBX network
    for FBX in FBXS:
        # run conversion
        convert_FBX(FBX)
    print '>> CONVERSION DONE!'