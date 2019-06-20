# Create flipbook
# Check if 001 version exists. If so, get latest existing version and
# ask user to overwrite latest version or create new

import os
import hou

import dna
reload(dna)

from PySide2 import QtCore, QtUiTools, QtWidgets

# Get current flipbook settings
desktop = hou.ui.curDesktop()
scene = desktop.paneTabOfType(hou.paneTabType.SceneViewer)
settings = scene.flipbookSettings().stash()

class SNV(QtWidgets.QWidget):
    def __init__(self, filePath):
        # Setup UI
        super(SNV, self).__init__()
        ui_file = '{}/saveNextVersion_Warning.ui'.format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        # Setup label
        message = 'File exists!\n{}'.format(dna.analyzeFliePath(filePath)['fileName'])
        self.ui.lab_message.setText(message)

        # Setup buttons
        self.ui.btn_SNV.clicked.connect(lambda: self.SNV(filePath))
        self.ui.btn_SNV.clicked.connect(self.close)
        self.ui.btn_OVR.clicked.connect(lambda: self.OVR(filePath))
        self.ui.btn_OVR.clicked.connect(self.close)
        self.ui.btn_ESC.clicked.connect(self.close)

    def SNV(self, filePath):
        # Save NEXT version of flipbook
        fileLocation = dna.analyzeFliePath(filePath)['fileLocation']
        fileName = dna.analyzeFliePath(filePath)['fileName']
        latestVersion = dna.extractLatestVersionFolder(fileLocation)  # '002'
        nextVersion = '{:03d}'.format(int(latestVersion) + 1)
        filePath = dna.buildFilePath(nextVersion, dna.fileTypes['flipbookSequence'], scenePath=hou.hipFile.path())
        os.makedirs(dna.analyzeFliePath(filePath)['fileLocation'])
        runFB(filePath)

    def OVR(self, filePath):
        # Overwrite LATEST EXISTING version of flipbook
        runFB(filePath)

def runFB(flipbookPath):
    '''
    Run flipbook rendering
    '''

    settings.output(flipbookPath)
    # Generate the flipbook using the modified settings
    scene.flipbook(scene.curViewport(), settings)
    # Report
    print 'Saved: {}'.format(flipbookPath)

def createFlipbook():
    # Setup flipbook settings
    settings.resolution(dna.resolution_LR)
    settings.frameRange((dna.frameStart, hou.playbar.frameRange()[1]))

    # Build 001 version of flipbook file path
    flipbookPath = dna.buildFilePath('001', dna.fileTypes['flipbookSequence'], scenePath=hou.hipFile.path())
    fileLocation = dna.analyzeFliePath(flipbookPath)['fileLocation']

    if not os.path.exists(fileLocation):
        # Write flipbook if not exists
        os.makedirs(fileLocation)
        runFB(flipbookPath)
    else:
        # If 001 file exists get latest version
        latestVersion = dna.extractLatestVersionFolder(fileLocation)
        # Build latest existing path
        flipbookPath = dna.buildFilePath(latestVersion, dna.fileTypes['flipbookSequence'], scenePath=hou.hipFile.path())
        # Ask user to save next version or overwrite latest
        win = SNV(flipbookPath)
        win.show()

def run():
    createFlipbook()

