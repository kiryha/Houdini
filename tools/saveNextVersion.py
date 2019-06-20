# 256 Pipeline Tools
# Save Next Version. Incremental save current houdini scene (<fileCode>_001.hip >> <fileCode>_002.hip).
# If a file with next version exists, script finds the latest existing version and rise warning window with options:
# - Save file with the latest available version
# - Overwrite a file with latest existing version


import hou
import os

import dna
from PySide2 import QtCore, QtUiTools, QtWidgets

class SNV(QtWidgets.QWidget):
    def __init__(self, filePath):
        # Setup UI
        super(SNV, self).__init__()
        ui_file = '{}/saveNextVersion_warning.ui'.format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        # self.resize(320, 120)  # resize window
        self.setWindowTitle('Save Next Version')  # Title Main window
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
        newPath = dna.buildPathNextVersion(filePath)
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
        # If next version exists, get latest existing version
        newPath = dna.buildPathLatestVersion(newPath)
        win = SNV(newPath)
        win.show()

def run():
    saveNextVersion()