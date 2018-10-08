# 256 Pipeline Tools
# Save Next Version. Incremental save current houdini scene (<fileCode>_001.hip >> <fileCode>_002.hip).
# If a file with next version exists, warning window rise with options:
# - Overwrite  a file with next version
# - Save file with the latest available version

import hou
import os

from MOTHER.dna import dna
from PySide2 import QtCore, QtUiTools, QtWidgets

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
        newPath = dna.buildPathLatestVersion(filePath)
        hou.hipFile.save(newPath)
        print '>> File saved with a LATEST version!'

    def OVR(self, filePath):
        hou.hipFile.save(filePath)
        print '>> Next version OVERWRITED!'

def saveNextVersion():
    # Get current name
    filePath = hou.hipFile.path()

    # Get next version
    newPath = dna.buildPathNextVersion(filePath)

    # Check if next version exists
    if not os.path.exists(newPath):
        hou.hipFile.save(newPath)
        print '>> File saved with a NEXT version!'
    else:
        win = SNV(newPath)
        win.show()

def run():
    saveNextVersion()