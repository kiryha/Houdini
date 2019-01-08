# Create flipbook
# Check if 001 version exists. If so, get latest existing version and
# ask user to overwrite latest version or create new

import os
import hou

from EVE.dna import dna

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
        # Rename button
        self.ui.btn_SNV.setText('Save Next Version')

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
        latestVersion = getLatestVersion(fileLocation)  # '002'
        nextVersion = '{:03d}'.format(int(latestVersion) + 1)
        filePath = buildFBName(nextVersion)
        os.makedirs(dna.analyzeFliePath(filePath)['fileLocation'])
        runFB(filePath)

    def OVR(self, filePath):
        # Overwrite LATEST EXISTING version of flipbook
        runFB(filePath)


def getLatestVersion(filePath):
    '''
    Get FOLDER filePath, return string: latest available version ("002")
    Assume that last folder in filePath is a version of flipbook
    '''
    # Strip last slash from path
    if filePath.endswith('/'):
        filePath = filePath[:-1]

    # Get list of folders
    version = filePath.split('/')[-1]
    pathVersions = filePath.replace(version, '')
    listVersions = os.listdir(pathVersions)
    listVersionsInt = []

    # Build list of Integer folder names
    for i in listVersions:
        if len(i) == 3:
            listVersionsInt.append(int(i))

    # Find highest folder number
    maxInt = max(listVersionsInt)
    # Build a string ('002') from highest number
    latestVersion = '{:03d}'.format(maxInt)

    return latestVersion


def runFB(flipbookPath):
    '''
    Run flipbook rendering
    '''

    settings.output(flipbookPath)
    # Generate the flipbook using the modified settings
    scene.flipbook(scene.curViewport(), settings)
    # Report
    print 'Saved: {}'.format(flipbookPath)


def buildFBName(version):
    '''
    Build file name for the flipbook based on scene name
    Expected naming convention for animation and render scenes:
    ANM_E010_S010_001.hip
    RND_E010_S010_001.hip

    param version: string flipbook file version (001)
    '''

    # Get current scene name
    scenePath = hou.hipFile.path()
    sceneName = scenePath.split('/')[-1].split('.')[0]

    try:
        sceneType, episode, shot, sceneVersion = sceneName.split('_')
    except:
        print 'Unsupported file name!'

    flipbookName = '{0}_{1}_{2}.$F.exr'.format(episode, shot, version)
    flipbookPath = '{0}/{1}/SHOT_{2}/{3}/{4}'.format(dna.rootRender3D, episode[-3:], shot[-3:], version, flipbookName)

    return flipbookPath


def createFlipbook():
    # Setup flipbook settings
    settings.resolution(dna.resolution)
    settings.frameRange((dna.frameStart, hou.playbar.frameRange()[1]))

    # Build 001 version of flipbook file path
    flipbookPath = buildFBName('001')
    fileLocation = dna.analyzeFliePath(flipbookPath)['fileLocation']

    if not os.path.exists(fileLocation):
        # Write flipbook if not exists
        os.makedirs(fileLocation)
        runFB(flipbookPath)
    else:
        # If 001 file exists get latest version
        latestVersion = getLatestVersion(fileLocation)
        # Build latest existing path
        flipbookPath = buildFBName(latestVersion)
        win = SNV(flipbookPath)
        win.show()

def run():
    createFlipbook()

