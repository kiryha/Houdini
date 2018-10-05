# 256 Pipeline tools
# Create ANIMATION and RENDER scenes

import hou
import os
from PySide2 import QtCore, QtUiTools, QtWidgets
from MOTHER.dna import dna
from MOTHER.ui.widgets import SaveNextVersion

class CreateScene(QtWidgets.QWidget):
    def __init__(self):
        super(CreateScene,self).__init__()
        ui_file = "{}/createScene_Main.ui".format(dna.folderUI)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        
        self.ui.btn_createRenderScene.clicked.connect(lambda: self.createScene('RND'))
        
    def createScene(self, sceneType):

        # Start new session without saving current
        hou.hipFile.clear(suppress_save_prompt=True)

        # Get episode and shot from UI
        episode = self.ui.lin_episode.text()
        shot = self.ui.lin_shot.text()
        pathScene = dna.buildFliePath(episode, shot, sceneType)

        # SAVE FILE
        # Check if file exists. Run Save Next Version dialog if so, save scene if not.
        if not os.path.exists(pathScene):
            hou.hipFile.save(pathScene)
            print '>> File saved with a next version!'
        else:
            win = SaveNextVersion.SNV(pathScene)
            win.show()




def run():
    CS = CreateScene()
    CS.show()