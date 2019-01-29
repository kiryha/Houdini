# 256 Pipeline tools
# Create ANIMATION and RENDER scenes

import hou
import os
from PySide2 import QtCore, QtUiTools, QtWidgets
from EVE.dna import dna
reload(dna)


# Get Houdini root nodes
sceneRoot = hou.node('/obj/')
outRoot = hou.node('/out/')

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
        
        self.ui.btn_createRenderScene.clicked.connect(lambda: self.createScene(fileType=dna.fileTypes['renderScene']))
        self.ui.btn_createRenderScene.clicked.connect(self.close)

    def createScene(self, fileType, catch = None):
        '''
        Save new scene, build scene content.
        :param sceneType: type of created scene, Render, Animation etc
        :param catch: determinate if procedure were run for the firs time from this class,
        or it returns user reply from SNV class
        :return:
        '''

        # Get sequence and shot from UI
        sequenceNumber = self.ui.lin_episode.text()
        shotNumber = self.ui.lin_shot.text()


        # If createRenderScene() runs first time
        if catch == None:

            # Build path to 001 version
            pathScene = dna.buildFliePath('001', fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber)

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
            newPath = dna.buildPathNextVersion(dna.buildPathLatestVersion(dna.buildFliePath('001', fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber)))
            hou.hipFile.save(newPath)
            hou.ui.displayMessage('New version saved:\n{}'.format(newPath.split('/')[-1]))
        elif catch == 'OVR':
            # Overwrite existing file
            pathScene = dna.buildPathLatestVersion(dna.buildFliePath('001', fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber))
            hou.hipFile.save(pathScene)
            hou.ui.displayMessage('File overwited:\n{}'.format(pathScene.split('/')[-1]))
        else:
            return

        # Build scene content
        self.buildSceneContent(fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber)

    def createHDA(self, parent, hdaTypeName, hdaName):
        '''
        Create Houdini digital asset node
        :param hdaTypeName:
        :param hdaName:
        :return:
        '''

        # Create HDA node inside parent container
        hda = parent.createNode(hdaTypeName, hdaName)

        # Set HDA file version (latest)
        hdaDefinitions = hda.type().allInstalledDefinitions()
        hdaPaths = [i.libraryFilePath() for i in hdaDefinitions]
        latestVersion = dna.extractLatestVersionFile(hdaPaths)  # 010

        for i in hdaPaths:
            if latestVersion in i.split('/')[-1]:
                latestIndex = hdaPaths.index(i)
                hdaDefinitions[latestIndex].setIsPreferred(True)

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

    def buildCharacterLoaders(self, CHARACTERS, charactersData):
        '''
        Create network to load characters data (geo cache, hairs, etc)

        TBD: merge loaders in several chars are in shot
        :param CHARACTERS: Characters container - geometry node object
        :param charactersData: dictionaries with character data linked to a shot
        :return:
        '''

        for characterData in charactersData:
            # Create nodes network for each character
            characterName = characterData['code']
            cache = CHARACTERS.createNode('filecache', 'CACHE_{0}'.format(characterName))
            cache.parm('loadfromdisk').set(1)
            null = CHARACTERS.createNode('null', 'OUT_{0}'.format(characterName))
            null.setInput(0, cache)

            # Build and set path to the 001 cache version
            pathCache = dna.buildFliePath('001',
                                          dna.fileTypes['cacheAnim'],
                                          scenePath=hou.hipFile.path(),
                                          characterName=characterName)

            cache.parm('file').set(pathCache)

            # Set render flags
            null.setDisplayFlag(1)
            null.setRenderFlag(1)


        CHARACTERS.layoutChildren()

    def importCameraAnimation(self, scenePath):
        '''
        Import camera to the render scene
        :param scenePath:
        :return:
        '''

        cameraPath = dna.buildFliePath('001', dna.fileTypes['camera'], scenePath=scenePath)
        sceneRoot.loadItemsFromFile(cameraPath)

    def importCharacterAnimation(self, scenePath, charactersData):
        '''
        Import character animation for the current render scene: set FileCache nodes paths.

        pathCache = $JOB/geo/SHOTS/010/SHOT_010/ROMA/GEO/001/E010_S010_ROMA_001.$F.bgeo.sc
        :param charactersData: list of characters dics for the current shot
        :param scenePath: Full path to Houdini render scene
        :return:
        '''

        for characterData in charactersData:
            characterName = characterData['code']

            # BUILD CACHE PATH (LATEST VERSION)
            # Build a path to the 001 version of cache

            pathCache = dna.buildFliePath('001',
                                          dna.fileTypes['cacheAnim'],
                                          scenePath=scenePath,
                                          characterName=characterName)

            # Check latest existing version, build new path if exists
            pathCacheFolder = self.convertPathCache(pathCache)
            latestCacheVersion = dna.extractLatestVersionFolder(pathCacheFolder)
            if latestCacheVersion != '001':
                pathCache = dna.buildFliePath(latestCacheVersion,
                                              dna.fileTypes['cacheAnim'],
                                              scenePath=scenePath,
                                              characterName=characterName)

            # SET FILE CACHE NODE PARAM
            # Get cache node
            cache = hou.node('{0}/{1}/CACHE_{2}'.format(sceneRoot, dna.nameChars, characterName))
            # Set path
            cache.parm('file').set(pathCache)

    def buildSceneContent(self, fileType, sequenceNumber, shotNumber):
        '''
        Create scene content: import characters, environments, materials etc.
        :param fileType:
        :param sequenceNumber:
        :param shotNumber:
        :return:
        '''

        # Create Render scene
        if fileType == dna.fileTypes['renderScene']:
            # Get shot data
            shotData, assetsData, environmentData, charactersData = dna.getShotGenes(sequenceNumber, shotNumber)

            # Initialize scene
            scenePath = hou.hipFile.path()

            # BUILD ENVIRONMENT
            # Proxy
            ENV_PRX = self.createContainer(sceneRoot, dna.nameEnvProxy)
            self.createHDA(ENV_PRX, environmentData['proxy_hda']['hda_name'], environmentData['proxy_hda']['name'])
            ENV_PRX.setPosition([0, 0])
            # Base
            ENVIRONMENT = self.createContainer(sceneRoot, dna.nameEnv, bbox=2, disp=0)
            self.createHDA(ENVIRONMENT, environmentData['hda_name'], environmentData['code'])
            ENVIRONMENT.setPosition([0, -dna.nodeDistance_y])
            # Animation
            ENV_ANM = self.createContainer(sceneRoot, dna.nameEnvAnim, bbox=2, mb=1)
            self.createHDA(ENV_ANM, environmentData['animation_hda']['hda_name'], environmentData['animation_hda']['name'])
            ENV_ANM.setPosition([0, -2 * dna.nodeDistance_y])

            CROWDS = self.createContainer(sceneRoot, dna.nameCrowds, bbox=2, mb=1)
            self.createHDA(CROWDS, environmentData['crowds_hda']['hda_name'], environmentData['crowds_hda']['name'])
            CROWDS.setPosition([0, -3 * dna.nodeDistance_y])

            # BUILD CHARACTERS
            # Create characters container
            CHARACTERS = self.createContainer(sceneRoot, dna.nameChars, mb=1)
            CHARACTERS.setPosition([0, -4 * dna.nodeDistance_y])

            # Create nodes to pull character caches
            self.buildCharacterLoaders(CHARACTERS, charactersData)

            # IMPORT MATERIALS
            # Create Geometry node in scene root
            ML = sceneRoot.createNode('ml_general', dna.nameMats)
            ML.setPosition([dna.nodeDistance_x, 0])

            # IMPORT ENV LIGHTS
            LIT = sceneRoot.createNode(environmentData['light_hda']['hda_name'], environmentData['light_hda']['name'])
            LIT.setPosition([dna.nodeDistance_x, -dna.nodeDistance_y])

            # SETUP OUTPUT
            # Create mantra render node
            mantra = outRoot.createNode('ifd', 'RENDER')

            # Render file version setup
            # renderFile = '$JOB/render/010/SHOT_040/001/E010_S040_001.$F.exr'
            renderFile = dna.buildFliePath('001', dna.fileTypes['renderSequence'], scenePath=scenePath)
            # Create folder for render file
            fileLocation = dna.analyzeFliePath(renderFile)['fileLocation']
            if not os.path.exists(fileLocation):
                # Make 001 folder
                os.makedirs(fileLocation)
            else:
                # If 001 file exists get latest version
                latestVersion = dna.extractLatestVersionFolder(fileLocation)
                nextVersion = '{:03d}'.format(int(latestVersion) + 1)
                # Build latest existing path
                renderFile = dna.buildFliePath(nextVersion, dna.fileTypes['renderSequence'], scenePath=scenePath)
                os.makedirs(dna.analyzeFliePath(renderFile)['fileLocation'])
                # Localize path (add $JOB)
                renderFile = renderFile.replace(dna.root3D, '$JOB')

            # Setup Mantra parameters
            mantra.parm('vm_picture').set(renderFile)
            mantra.parm('camera').set('/obj/E{0}_S{1}'.format(sequenceNumber, shotNumber))
            # Set common parameters from preset
            for param, value in dna.renderSettings['common'].iteritems():
                mantra.parm(param).set(value)
            # Set DRAFT parameters
            for param, value in dna.renderSettings['draft'].iteritems():
                mantra.parm(param).set(value)

            # SETUP SCENE (end frame ...)
            frameEnd = shotData['sg_cut_out']
            hou.playbar.setFrameRange(dna.frameStart, frameEnd)
            hou.playbar.setPlaybackRange(dna.frameStart, frameEnd)

            # IMPORT ANIMATION
            # Later would be provided as separate tool
            # Import camera
            self.importCameraAnimation(scenePath)
            # Import characters caches
            self.importCharacterAnimation(scenePath, charactersData)


        # Save scene
        hou.hipFile.save()

# Create CS object
CS = CreateScene()

def run():
    # Run the Create Scene Tool
    CS.show()