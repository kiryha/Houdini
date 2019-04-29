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

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(240, 65)  # resize window
        self.setWindowTitle('Create Scene')  # Title Main window

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

        print '>> Building Render scene...'

        # Get sequence and shot from UI
        sequenceNumber = self.ui.lin_episode.text()
        shotNumber = self.ui.lin_shot.text()


        # If createRenderScene() runs first time
        if catch == None:

            # Build path to 001 version
            pathScene = dna.buildFilePath('001', fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber)

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
            newPath = dna.buildPathNextVersion(dna.buildPathLatestVersion(dna.buildFilePath('001', fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber)))
            hou.hipFile.save(newPath)
            hou.ui.displayMessage('New version saved:\n{}'.format(newPath.split('/')[-1]))
        elif catch == 'OVR':
            # Overwrite existing file
            pathScene = dna.buildPathLatestVersion(dna.buildFilePath('001', fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber))
            hou.hipFile.save(pathScene)
            hou.ui.displayMessage('File overwited:\n{}'.format(pathScene.split('/')[-1]))
        else:
            return

        # Build scene content
        self.buildSceneContent(fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber)

        # Save scene
        hou.hipFile.save()

        print '>> Building Render scene done!'

    def createHDA(self, parent, hdaTypeName, hdaName):
        '''
        Create Houdini digital asset node and set latest file version
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

    def createContainer_rem(self, parent, name, bbox=0, mb=None, disp=1):
        '''
        Moved to DNA, need to be deleted!!!

        Create scene container for CHARS, ENV etc
        :param parent: container node parent object (where to cretae it)
        :param name: container name
        :param bbox: display container content as bounding box (bbox = 2, full = 0)
        :param mb: turn on motion blur for container content geometry
        :param disp: Display container node flag (ON = 1, OFF = 0)
        :return:
        '''

        CONTAINER = parent.createNode('geo',name)

        # Display as bounding box
        CONTAINER.parm('viewportlod').set(bbox)

        # Set display flag
        CONTAINER.setDisplayFlag(disp)

        # Turn ON motion blur
        if mb is not None:
            CONTAINER.parm('geo_velocityblur').set(1)

        return CONTAINER

    def buildSceneContent(self, fileType, sequenceNumber, shotNumber):
        '''
        Create scene content: import characters, environments, props, materials etc.

        Render scene schema:
            [Render obj]      [Environment]     [Characters]     [Props]      [FX]
            - materials       - Env             - char 1         - prop 1     - fx 1
            - lights                            - char 2         - prop 2     - fx 2
            - camera                            - ...            - ...        - ...

        :param fileType:
        :param sequenceNumber:
        :param shotNumber:
        :return:
        '''

        # Create Render scene
        if fileType == dna.fileTypes['renderScene']:

            # Get shot data
            shotGenes = dna.getShotGenes(sequenceNumber, shotNumber)
            env_data = shotGenes['environmentData']

            # Initialize scene
            scenePath = hou.hipFile.path()

            # SETUP SCENE (end frame ...)
            frameEnd = shotGenes['shotData']['sg_cut_out']
            hou.playbar.setFrameRange(dna.frameStart, frameEnd)
            hou.playbar.setPlaybackRange(dna.frameStart, frameEnd)

            # [Render obj]
            if env_data:
                # Add Material lib HDA
                mat_data = env_data['materials']
                ML = sceneRoot.createNode(mat_data['hda_name'], mat_data['name'])
                ML.setPosition([0, 0])
                # Add lights HDA
                lit_data = env_data['lights']
                LIT = sceneRoot.createNode(lit_data['hda_name'], lit_data['name'])
                LIT.setPosition([0, -dna.nodeDistance_y])
                # Add Camera via ABC. Done in Import ANM


            # [Environment]
            if env_data:
                ENV = sceneRoot.createNode(env_data['hda_name'], env_data['code'])
                ENV.setPosition([dna.nodeDistance_x, 0])

            # [Characters]
            char_data = shotGenes['charactersData']
            if char_data:
                for n, character in enumerate(char_data):
                    CHAR = dna.createContainer(sceneRoot, char_data[n]['code'], mb=1)
                    CHAR.setPosition([2*dna.nodeDistance_x, n*dna.nodeDistance_y])

            # [Props]
            # No props for NSI project.

            # [FX]
            fx_data = shotGenes['fxData']
            if fx_data:
                for n, FX in enumerate(fx_data):
                    FX = sceneRoot.createNode(FX['hda_name'], FX['code'])
                    FX.setPosition([3*dna.nodeDistance_x, n*dna.nodeDistance_y])


            # SETUP MANTRA OUTPUT
            # Create mantra render node
            mantra = outRoot.createNode('ifd', dna.mantra)

            # Render sequence setup
            renderSequence = dna.buildRenderSequencePath(scenePath)

            # Setup Mantra parameters
            mantra.parm('vm_picture').set(renderSequence)
            cameraName = dna.cameraName.format(sequenceNumber, shotNumber)
            mantra.parm('camera').set('/obj/{}'.format(cameraName))
            # Set common parameters from preset
            for param, value in dna.renderSettings['common'].iteritems():
                mantra.parm(param).set(value)
            # Set DRAFT parameters
            for param, value in dna.renderSettings['draft'].iteritems():
                mantra.parm(param).set(value)

# Create CS objectfileTypes
CS = CreateScene()

def run():
    # Run the Create Scene Tool
    CS.show()