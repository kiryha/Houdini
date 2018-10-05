# 256 Pipeline tools
# Save Next Version UI and functionality

import hou
from PySide2 import QtCore, QtUiTools, QtWidgets
from MOTHER.dna import dna
reload(dna)

class SNV(QtWidgets.QWidget):
    def __init__(self, filePath):
        # Setup UI
        super(SNV, self).__init__()
        ui_file = '{}/saveNextVersion_Warning.ui'.format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        # Setup label
        message = 'File exists!\n{}'.format(dna.analyzeFliePath(filePath)[1])
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
        print '>> File saved with a latest version!'

    def OVR(self, filePath):
        hou.hipFile.save(filePath)
        print '>> File overwrited with a new version!'