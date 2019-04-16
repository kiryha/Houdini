# 256 Pipeline tools
# Edit Mantra render settings

import hou
import os

from PySide2 import QtCore, QtUiTools, QtWidgets
from EVE.dna import dna
reload(dna)


class RenderManager(QtWidgets.QWidget):
    def __init__(self):
        super(RenderManager, self).__init__()
        ui_file = "{}/renderManager_Main.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Common variables
        self.scenePath = hou.hipFile.path()

        self.ui.btn_updateRenderPath.clicked.connect(self.updateRenderPath)
        #self.ui.btn_createRenderScene.clicked.connect(self.close)

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

# Create CS objectfileTypes
RM = RenderManager()

def run():
    # Run the Create Scene Tool
    RM.show()