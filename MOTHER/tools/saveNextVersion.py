# 256 Pipeline Tools
# Save Next Version. Incremental save current houdini scene (<fileCode>_001.hip >> <fileCode>_002.hip).
# If a file with next version exists, warning window rise with options:
# - Overwrite  a file with next version
# - Save file with the latest available version

import hou
import os
import glob
from PySide2 import QtCore, QtUiTools, QtWidgets

from MOTHER.dna import dna
reload(dna)

pathUI = os.environ['JOB'].replace('PROD/3D', 'PREP/PIPELINE/MOTHER/ui/ui/')

class SNV(QtWidgets.QWidget):
    def __init__(self, filePath):
        # Setup UI
        super(SNV, self).__init__()
        ui_file = '{}saveNextVersion_Warning.ui'.format(pathUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        # Setup label
        message = 'File exists!\n{}'.format(dna.analyzePath(filePath)[1])
        self.ui.lab_message.setText(message)
        # Setup buttons
        self.ui.btn_SNV.clicked.connect(lambda: self.SNV(filePath))
        self.ui.btn_SNV.clicked.connect(self.close)
        self.ui.btn_OVR.clicked.connect(lambda: self.OVR(filePath))
        self.ui.btn_OVR.clicked.connect(self.close)
        self.ui.btn_ESC.clicked.connect(self.close)

    def SNV(self, filePath):
        newPath = buildPathLatestVersion(filePath)
        hou.hipFile.save(newPath)
        print '>> File saved with a latest version!'

    def OVR(self, filePath):
        hou.hipFile.save(filePath)
        print '>> File overwrited with a new version!'


def extractLatestVersion(listExisted):
    '''
    Get list of files, return latest existing version + 1 (<###> string)
    '''
    listVersions = []
    for filePath in listExisted:
        listVersions.append(int(dna.analyzePath(filePath)[3]))
    latestVersion = '{:03}'.format(max(listVersions) + 1)
    return latestVersion


def buildPathNextVersion(filePath):
    '''
    Get filePath, create new filePath with a next version in fileName
    '''
    fileLocation, fileName, fileCode, fileVersion, fileExtenstion = dna.analyzePath(filePath)
    fileVersionNext = '{:03}'.format(int(fileVersion) + 1)
    filePathNextVersion = '{0}{1}_{2}.{3}'.format(fileLocation, fileCode, fileVersionNext, fileExtenstion)

    return filePathNextVersion


def buildPathLatestVersion(filePath):
    '''
    Get filePath, create new filePath with a latest available version in fileName
    '''
    fileLocation, fileName, fileCode, fileVersion, fileExtenstion = dna.analyzePath(filePath)

    listExisted = glob.glob('{0}{1}_*.{2}'.format(fileLocation, fileCode, fileExtenstion))
    fileVersionLatest = extractLatestVersion(listExisted)
    filePathLatestVersion = '{0}{1}_{2}.{3}'.format(fileLocation, fileCode, fileVersionLatest, fileExtenstion)

    return filePathLatestVersion


def saveNextVersion():
    # Get current name
    filePath = hou.hipFile.path()

    # Get next version
    newPath = buildPathNextVersion(filePath)

    # Check if next version exists
    if not os.path.exists(newPath):
        hou.hipFile.save(newPath)
        print '>> File saved with a next version!'
    else:
        win = SNV(newPath)
        win.show()


def run():
    saveNextVersion()