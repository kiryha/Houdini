# 256 Pipeline tools
# Edit Mantra render settings

import hou
import os

from PySide2 import QtCore, QtUiTools, QtWidgets
import dna
reload(dna)



class SceneManager(QtWidgets.QWidget):
    def __init__(self):
        super(SceneManager, self).__init__()
        ui_main = "{}/sceneManager_main.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_main, parentWidget=self)

        # Setup window properties
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.resize(320, 20)  # resize window
        self.setWindowTitle('Scene Manager')  # Title Main window
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Common variables
        self.scenePath = hou.hipFile.path()

        self.ui.btn_updateRenderPath.clicked.connect(self.updateRenderPath)

    def updateRenderPath(self):
        '''
        Set <Mantra node > Images > Output Picture> to the latest version
        '''

        # Get Mantra node
        mantra = hou.node('/out/{0}'.format(dna.mantra))

        if not mantra:
            print '>> There is NO "{}" Mantra node in scene!'.format(dna.mantra)

        else:
            renderSequence = dna.buildRenderSequencePath(self.scenePath)
            mantra.parm('vm_picture').set(renderSequence)
            print '>> Output Images updated: {}'.format(renderSequence)

# Create Render Manager instance
SM = SceneManager()

def run():
    # Run the Render Manager Tool
    SM.show()