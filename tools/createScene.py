# 256 Pipeline tools
# Create ANIMATION and RENDER scenes

import hou
import os
import json

from PySide2 import QtCore, QtUiTools, QtWidgets
import dna
reload(dna)

# Get environment data
rootProject = os.environ['ROOT']
genesFileShots = dna.genesFileShots.format(rootProject)
genesFileAssets = dna.genesFileAssets.format(rootProject)
genesShots = json.load(open(genesFileShots)) # All shots genes
genesAssets = json.load(open(genesFileAssets)) # All shots genes

# Get Houdini root nodes
sceneRoot = hou.node('/obj/')
outRoot = hou.node('/out/')


class CreateScene(QtWidgets.QWidget):
    def __init__(self):
        super(CreateScene, self).__init__()
        ui_file = "{}/createScene_main.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(320, 120)  # resize window
        self.setWindowTitle('Create Scene')  # Title Main window

        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        self.ui.btn_createRenderScene.clicked.connect(lambda: self.createScene(fileType=dna.fileTypes['renderScene']))
        self.ui.btn_createAnimScene.clicked.connect(lambda: self.createScene(fileType=dna.fileTypes['animationScene']))
        self.ui.btn_createRenderScene.clicked.connect(self.close)

    def createScene(self, fileType):
        '''
        Create hip scene and build all content (bring assets and camera)
        :param fileType:
        :return:
        '''
        sequenceNumber = self.ui.lin_episode.text()
        shotNumber = self.ui.lin_shot.text()

        # If shot exists in database run scene creation
        if not dna.checkGenes(sequenceNumber, shotNumber, genesShots):
            return

        if dna.createHip(fileType, sequenceNumber=sequenceNumber, shotNumber=shotNumber):
            dna.buildSceneContent(fileType, sequenceNumber, shotNumber, genesShots)

# Create CS object
CS = CreateScene()

def run():
    # Run the Create Scene Tool
    CS.show()