'''
256 Pipeline tools
Vray (VRAY) to Redshift (RED) material converter in Houdini
Select source SHOP network and run script

Required hierarchy of materials
SHOP VRAY >> VRAY materials containers >> VRAY material nodes
'''

import hou

# DEFINE COMMON VARIABLES
# Bump and displacement scale
scaleBump = 0.1
# RED network name
nameSHOP_RED = '{}_RS'
# Dictionary with VRAY and RED material parameters correspondence (parameter_VRAY : parameter_RED)
shaderParametersList = {'diffuse_color': 'diffuse_color',
                        'diffuse_factor': 'diffuse_weight',
                        'diffuse_texture': 'diffuse_color',

                        'ambinet_color': 'transl_color',
                        'ambient_factor': 'transl_weight',

                        'emissive_color': 'emission_color',
                        'emissive_texture': 'emission_color',

                        'reflect_color': 'refl_color',
                        'reflect_factor': 'refl_weight',
                        'reflect_texture': 'refl_color',

                        'shininess': 'refl_roughness',
                        'shininess_texture': 'refl_roughness',

                        'specular_color': 'coat_color',
                        'specular_factor': 'coat_weight',
                        'specular_texture': 'coat_color',

                        'opacity_color': 'refr_color',
                        'opacity_factor': 'refr_weight',

                        'bump_texture': 'input'}

# Get scene OBJ context object
OBJ = hou.node('/obj/')
# Get VRAY SHOP network from selection
SHOP_VRAY = hou.selectedNodes()

def checkConditions():
    '''
    Check if environment conditions allows to run script without errors
    '''
    if not SHOP_VRAY:  # If user select anything
        print '>> Nothing selected! Select SHOP network!'
        return 0
    elif SHOP_VRAY[0].type().name() != 'shopnet':  # If user select SHOP
        print '>> Wrong selection type. Select SHOP network!'
        return 0
    elif hou.node('/obj/{0}/'.format(nameSHOP_RED.format(SHOP_VRAY[0]))):  # If there is no RED target SHOP network
        print '>> Redshift SHOP already exists!'
        return 0

def returnParameterRED(parameterVRAY):
    '''
    Return corresponding RED parameter for input VRAY parameter

    Table of correspondence is shaderParametersList dictionary
    Here we cut possible indexes in input parameter string:
    diffuse_texture2 >> diffuse_texture
    '''
    try:
        index = int(parameterVRAY[-1])
        key = parameterVRAY.replace(str(index), '')
    except:
        key = parameterVRAY

    parameterRED = shaderParametersList[key]
    return parameterRED

def checkParameterInList(parameter):
    '''
    Check if input parameter exists in shaderParametersList
    '''
    try:
        index = int(parameter[-1])
        key = parameter.replace(str(index), '')
    except:
        key = parameter

    if key in shaderParametersList.keys():
        return 1

def getAllNodeParameters(node):
    params = [param.name() for param in node.parms()]
    return params

def checkIfTexture(parameter):
    '''
    Check if input parameter is a texture parameter
    '''
    if 'texture' in parameter.split('_')[-1]:
        return 1

def checkIfBump(parameter):
    '''
    Check if input parameter is a BUMP parameter
    '''
    if 'bump' in parameter.split('_')[0]:
        return 1

def getTexturedParameters():
    '''
    Search and output all parameters in selected SHOP network with textures
    '''

    # list of textures
    listTexturedParameters = []
    # Get list of VRAY materials
    listMaterials_VRAY = SHOP_VRAY.children()
    for material_VRAY in listMaterials_VRAY:
        materials = [material for material in material_VRAY.children() if material.type().name() == 'vopsurface']
        # print material.name()
        for node in materials:
            textures = [texture for texture in node.children() if texture.type().name() == 'subnet']
            for parameter in textures:
                params = [param for param in parameter.children() if param.name() == 'texture_name']
                for i in params:
                    texturedParameter = i.parm('parmname').eval()
                    if not texturedParameter in listTexturedParameters:
                        print '>> ADDED PARAMETER: {0} FROM MAT: {1}'.format(texturedParameter, material_VRAY)
                        listTexturedParameters.append(texturedParameter)
    print listTexturedParameters

def extractVrayVopsurfaceNode(listNodes_VRAY):
    '''
    Find and return Vray vopsurface node from list of VRay nodes in each material
    :param listNodes_VRAY - List of nodes in each material container
    :return: node_VRAY - Vray vopsurface node with VRAY material parameters
    '''
    for node_VRAY in listNodes_VRAY:
        if node_VRAY.type().name() == 'vopsurface':
            return node_VRAY

def copyParameters(node_VRAY, nodeMAT_RED, parameter_VRAY, material_RED, nodeRSM_RED):
    '''
    Copy parameters from VRAY material to RED nodes

    :param node_VRAY - VRAY node with material parameters
    :param nodeMAT_RED - RED node with material parameters
    :param parameter_VRAY - current parameter (string) from dictionary to copy data from
    :param material_RED
    :param nodeRSM_RED
    '''

    # Check if parameter exist in shaderParametersList
    if checkParameterInList(parameter_VRAY):
        # Get VRAY shader parameter (object)
        parameter_VRAY = node_VRAY.parmTuple(parameter_VRAY)
        # Get parameter value for VRAY
        parameterValue_VRAY = parameter_VRAY.eval()
        # Get corresponding RED parameter
        parameter_RED = returnParameterRED(parameter_VRAY.name())

        # Set RED shader parameter
        # Process textured parameters
        if checkIfTexture(parameter_VRAY.name()):  # Check if current parameter is textured

            # Get string texture path from tuple and fix slashes
            parameterValue_VRAY = parameterValue_VRAY[0].replace('\\', '/')

            # Process bump and displacement
            if checkIfBump(parameter_VRAY.name()):  # Check if current parameter is a bump
                # Check if texture name exists
                if parameterValue_VRAY != '':
                    # Create and connect  bump node
                    bump_RED = material_RED.createNode('redshift::BumpMap')
                    nodeRSM_RED.setNamedInput('Bump Map', bump_RED, 'out')
                    bump_RED.parm('scale').set(scaleBump)
                    # Create and connect texture node
                    texture_RED = material_RED.createNode('redshift::TextureSampler')
                    texture_RED.setName(parameter_VRAY.name())
                    bump_RED.setNamedInput('input', texture_RED, 'outColor')
                    textureName = parameterValue_VRAY # Set texture name
                    texture_RED.parm('tex0').set(textureName)
                    # Create and connect displacement node
                    disp_RED = material_RED.createNode('redshift::Displacement')
                    nodeRSM_RED.setNamedInput('Displacement', disp_RED, 'out')
                    disp_RED.setNamedInput('texMap', texture_RED, 'outColor')
                    disp_RED.parm('scale').set(scaleBump)

            # Process other textures
            else:
                # Check if texture name exists
                if parameterValue_VRAY != '':
                    textureName = parameterValue_VRAY # Set texture name
                    texture_RED = material_RED.createNode('redshift::TextureSampler')
                    texture_RED.setName(parameter_VRAY.name())
                    nodeMAT_RED.setNamedInput(parameter_RED, texture_RED, 'outColor')
                    texture_RED.parm('tex0').set(textureName)

        # Process other parameters
        else:
            if parameter_VRAY.name() == 'opacity_factor':  # Invert opacity (to map refraction weight)
                nodeMAT_RED.parmTuple(parameter_RED).set(tuple([1.0 - parameterValue_VRAY[0]]))
            else:
                nodeMAT_RED.parmTuple(parameter_RED).set(parameterValue_VRAY)

        # Layout redshift material nodes in Network View
        material_RED.layoutChildren()

def buildShaderNetwork_RED(material_RED, nodeRSM_RED, node_VRAY):
    '''
    Create RED shader network and copy parameters from VRAY material inside RED material container.
    :param material_RED - Redshift Material Container
    :param nodeRSM_RED - Redshift_Material node
    :param node_VRAY - VRAY node with material parameters
    '''

    # print 'convertMaterials().node_VRAY = {}'.format(node_VRAY.name())

    # Create <redshift::Material> node with material parameters
    nodeMAT_RED = material_RED.createNode('redshift::Material')
    material_RED.moveToGoodPosition()
    # Make connections: redshift::material1 >> redshift_material1
    nodeRSM_RED.setNamedInput('Surface', nodeMAT_RED, 'outColor')

    # Get all parameters for node_VRAY
    parameters_VRAY = getAllNodeParameters(node_VRAY)

    # Copy parameters from VRAY to RED
    for parameter_VRAY in parameters_VRAY:
        copyParameters(node_VRAY, nodeMAT_RED, parameter_VRAY, material_RED, nodeRSM_RED)

def buildMaterial_RED(SHOP_RED, material_VRAY):
    '''
    Create RED Material based on VRAY material parameters
    :param SHOP_RED - SHOP network for RED materials
    :param material_VRAY - source VRAY material
    '''
    print '>> Current material = {}'.format(material_VRAY.name())

    # Create RED material container
    material_RED = SHOP_RED.createNode('redshift_vopnet')  # Create RED Material container with redshift_material1 node
    material_RED.setName(material_VRAY.name())
    material_RED.moveToGoodPosition()
    nodeRSM_RED = material_RED.children()[0]  # Get redshift_material1 node

    # Get list of VRAY material nodes
    listNodes_VRAY = material_VRAY.children()
    # Get VRAY vopsurface node
    node_VRAY = extractVrayVopsurfaceNode(listNodes_VRAY)

    # Create RED shader and copy Vray parameters
    buildShaderNetwork_RED(material_RED, nodeRSM_RED, node_VRAY)

def convertMaterials():
    '''
    Convert Materials main function: run convertion procedure
    '''

    # Create RED SHOP Network
    SHOP_RED = OBJ.createNode('shopnet')
    SHOP_RED.setName(nameSHOP_RED.format(SHOP_VRAY))

    # Get list of VRAY materials
    listMaterials_VRAY = SHOP_VRAY.children()

    # Create RED materials inside RED SHOP network
    for material_VRAY in listMaterials_VRAY:
        buildMaterial_RED(SHOP_RED, material_VRAY)
    # Layout redshift materials in Nwtwork View
    SHOP_RED.layoutChildren()


# RUN SCRIPT
# Check if conditions are fine and run conversion
if checkConditions() != 0:
    print '>> CONVERTING MATERIALS...'
    SHOP_VRAY = SHOP_VRAY[0]  # Get VRAY SHOP Network object from tuple
    convertMaterials()  # Run conversion procedure
    # getTexturedParameters() # List of parameters with textures, uncomment to print it
    print '>> CONVERSION DONE!'