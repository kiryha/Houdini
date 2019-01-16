# 256 Pipeline tools
# Create ANIMATION and RENDER scenes

import hou
import os
from PySide2 import QtCore, QtUiTools, QtWidgets
from EVE.dna import dna
reload(dna)

# Get scene root node
sceneRoot = hou.node('/obj/')


'''
# HDA manips
import hou

city = hou.node('/obj/ENVIRONMENT/CITY')
#city.allowEditingOfContents()
#print city.type().definition().libraryFilePath()
#hou.hda.installFile('P:/PROJECTS/NSI/PROD/3D/hda/ENVIRONMENTS/CITY/CITY_009.hdanc')
#city.changeNodeType('city')
'''

# Asset and shot data. Meant to be stored in database (Shotgun). Will be moved to genes.py
# Shotgun schema: project > sequence > shot
# We use term <episode> instead of <sequence>. episode = sequence





# name = display name of asset in Houdini UI, had_name = name of HDA, proxy_hda = Low res ENV asset version
data_city = {'name': 'CITY',
           'hda_name': 'city',
           'animation_hda': {'name': 'CITY_ANM', 'hda_name': 'city_anm'},
           'proxy_hda': {'name': 'CITY_PRX', 'hda_name': 'city_prx'},
           'crowds_hda': {'name': 'CROWDS', 'hda_name': 'city_crowds'},
           'light_hda': {'name': 'CITY_LIT', 'hda_name': 'city_lights'}}

data_roma = {'name': 'ROMA'}

data_shot = {'name': 'SHOT_010',
            'scene': {'name': '010'},
            'characters': [data_roma],
            'environment': data_city,
            'props': []}

class SNV(QtWidgets.QWidget):
    def __init__(self, filePath, sceneType):
        # Setup UI
        super(SNV, self).__init__()
        self.sceneType = sceneType # RND, ANM etc. To return back to CS object
        ui_file = '{}/saveNextVersion_Warning.ui'.format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        # Setup label
        message = 'File exists!\n{}'.format(dna.analyzeFliePath(filePath)['fileName'])
        self.ui.lab_message.setText(message)

        # Setup buttons
        self.ui.btn_SNV.clicked.connect(self.SNV)
        self.ui.btn_SNV.clicked.connect(self.close)
        self.ui.btn_OVR.clicked.connect(self.OVR)
        self.ui.btn_OVR.clicked.connect(self.close)
        self.ui.btn_ESC.clicked.connect(self.close)

    def SNV(self):
        CS.createScene(self.sceneType, 'SNV')

    def OVR(self):
        CS.createScene(self.sceneType, 'OVR')

class CreateScene(QtWidgets.QWidget):
    def __init__(self):
        super(CreateScene, self).__init__()
        ui_file = "{}/createScene_Main.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        
        self.ui.btn_createRenderScene.clicked.connect(lambda: self.createScene(fileType=dna.fileTypes['render']))
        self.ui.btn_createRenderScene.clicked.connect(self.close)

    def createScene(self, fileType, catch = None):
        '''
        Save new scene, build scene content.
        :param sceneType: type of created scene, Render, Animation etc
        :param catch: determinate if procedure were run for the firs time from this class,
        or it returns user reply from SNV class
        :return:
        '''

        # Get episode and shot from UI
        episodeNumber = self.ui.lin_episode.text()
        shotNumber = self.ui.lin_shot.text()


        # If createRenderScene() runs first time
        if catch == None:

            # Build path to 001 version
            pathScene = dna.buildFliePath('001', fileType, episodeNumber=episodeNumber, shotNumber=shotNumber)

            # Start new Houdini session without saving current
            hou.hipFile.clear(suppress_save_prompt=True)

            # Check if file exists
            if not os.path.exists(pathScene):
                # Save first version if NOT EXISTS
                hou.hipFile.save(pathScene)
                hou.ui.displayMessage('File created:\n{}'.format(pathScene.split('/')[-1]))
                # print '>> First version of file saved!'
            else:
                # If 001 version exists, get latest existing version
                pathScene = dna.buildPathLatestVersion(pathScene)
                # Run Save Next Version dialog if EXISTS
                winSNV = SNV(pathScene, fileType)
                winSNV.show()
                return

        # If createRenderScene() runs from SNV class: return user choice, OVR or SNV
        elif catch == 'SNV':
            # Save latest version
            newPath = dna.buildPathNextVersion(dna.buildPathLatestVersion(dna.buildFliePath('001', fileType, episodeNumber=episodeNumber, shotNumber=shotNumber)))
            hou.hipFile.save(newPath)
            hou.ui.displayMessage('New version saved:\n{}'.format(newPath.split('/')[-1]))
        elif catch == 'OVR':
            # Overwrite existing file
            pathScene = dna.buildPathLatestVersion(dna.buildFliePath('001', fileType, episodeNumber=episodeNumber, shotNumber=shotNumber))
            hou.hipFile.save(pathScene)
            hou.ui.displayMessage('File overwited:\n{}'.format(pathScene.split('/')[-1]))
        else:
            return

        # Build scene content
        self.buildSceneContent(fileType, episodeNumber=episodeNumber, shotNumber=shotNumber)

    def createContainer(self, parent, name, bbox=0, mb=None, disp=1):
        '''
        Create scene container for CHARS, ENV etc
        :param parent: container node parent object (where to cretae it)
        :param name: container name
        :param bbox: display container content as bounding box (bbox = 2, full = 0)
        :param mb: turn on motion blur for container content geometry
        :param disp: Display container node flag (ON = 1, OFF = 0)
        :return:
        '''

        CONTAINER = parent.createNode('geo',name)
        # Delete all nodes in container
        for node in CONTAINER.children():
            node.destroy()

        # Display as bounding box
        CONTAINER.parm('viewportlod').set(bbox)

        # Set display flag
        CONTAINER.setDisplayFlag(disp)

        # Turn ON motion blur
        if mb is not None:
            CONTAINER.parm('geo_velocityblur').set(1)

        return CONTAINER

    def convertPathCache(self, pathCache):
        '''
        Convert geometry cache string path (used in FileCacheSOP) to path suitable for dna.extractLatestVersionFolder()
        Expand $JOB variable to a full path, remove file name
        :param pathCache:
        :return :
        '''

        fileName = pathCache.split('/')[-1]
        pathCacheFolder = pathCache.replace('$JOB', dna.root3D).replace(fileName, '')

        return pathCacheFolder

    def buildCharacterLoader(self, CHARACTERS, characterName):
        '''
        Create network to load character data (geo cache, hairs, etc)

        :param CHARACTERS: Characters container - geometry node object
        :param characterName: string character name
        :return:
        '''

        # Build a path to the 001 version of cache
        # $JOB/geo/SHOTS/010/SHOT_010/ROMA/GEO/001/E010_S010_ROMA_001.$F.bgeo.sc
        pathCache = dna.buildFliePath('001',
                                      dna.fileTypes['cacheAnim'],
                                      scenePath=hou.hipFile.path(),
                                      characterName=characterName)

        # Check latest existing version, build new path if exists
        pathCacheFolder = self.convertPathCache(pathCache)
        latestCacheVersion = dna.extractLatestVersionFolder(pathCacheFolder)
        if latestCacheVersion != '001':
            pathCache = dna.buildFliePath(latestCacheVersion,
                                          dna.fileTypes['cacheAnim'],
                                          scenePath=hou.hipFile.path(),
                                          characterName=characterName)


        cache = CHARACTERS.createNode('filecache', 'CACHE_{}'.format(characterName))
        cache.parm('loadfromdisk').set(1)
        cache.parm('file').set(pathCache)
        null = CHARACTERS.createNode('null', 'OUT_{}'.format(characterName))
        null.setInput(0, cache)
        null.setDisplayFlag(1)
        null.setRenderFlag(1)

        CHARACTERS.layoutChildren()

    def buildSceneContent(self, fileType, episodeNumber, shotNumber):
        '''
        Create scene content: import characters, environments, materials etc.
        :param fileType:
        :param episodeNumber:
        :param shotNumber:
        :return:
        '''

        # Create Render scene
        if fileType == dna.fileTypes['render']:

            # Get data for the current shot (episodeNumber > shotNumber)


            # BUILD ENVIRONMENT
            # Proxy
            ENV_PRX = self.createContainer(sceneRoot, dna.nameEnvProxy)
            ENV_PRX.createNode(data_city['proxy_hda']['hda_name'], data_city['proxy_hda']['name'])
            ENV_PRX.setPosition([0, 0])
            # Base
            ENVIRONMENT = self.createContainer(sceneRoot, dna.nameEnv, bbox=2, disp=0)
            ENVIRONMENT.createNode(data_city['hda_name'], data_city['name'])
            ENVIRONMENT.setPosition([0, -dna.nodeDistance_y])
            # Animation
            ENV_ANM = self.createContainer(sceneRoot, dna.nameEnvAnim, bbox=2, mb=1)
            ENV_ANM.createNode(data_city['animation_hda']['hda_name'], data_city['animation_hda']['name'])
            ENV_ANM.setPosition([0, -2 * dna.nodeDistance_y])

            CROWDS = self.createContainer(sceneRoot, dna.nameCrowds, bbox=2, mb=1)
            #CROWDS.createNode(data_city['crowds_hda']['hda_name'], data_city['crowds_hda']['name'])
            CROWDS.setPosition([0, -3 * dna.nodeDistance_y])


            # BUILD CHARACTERS
            # Create characters container
            CHARACTERS = self.createContainer(sceneRoot, dna.nameChars, mb=1)
            CHARACTERS.setPosition([0, -4 * dna.nodeDistance_y])

            # Create character loaders
            for character in data_shot['characters']:
                self.buildCharacterLoader(CHARACTERS, character['name'])

            # IMPORT MATERIALS
            # Create Geometry node in scene root
            ML = sceneRoot.createNode('ml_general', dna.nameMats)
            ML.setPosition([dna.nodeDistance_x, 0])

            # IMPORT ENV LIGHTS
            LIT = sceneRoot.createNode(data_city['light_hda']['hda_name'], data_city['light_hda']['name'])
            LIT.setPosition([dna.nodeDistance_x, -dna.nodeDistance_y])

            # OUTPUT

        # Save scene
        hou.hipFile.save()

# Create CS object
CS = CreateScene()

def run():
    # Run the Create Scene Tool
    CS.show()
