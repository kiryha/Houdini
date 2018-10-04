# 256 Pipeline tools
# Create ANIMATION and RENDER scenes

import hou
import os
from PySide2 import QtCore, QtUiTools, QtWidgets

path_ui = os.environ['JOB'].replace('PROD/3D', 'PREP/PIPELINE/MOTHER/ui')
 
class CreateScene(QtWidgets.QWidget):
    def __init__(self):
        super(CreateScene,self).__init__()
        ui_file = "{}/ui/createScene_Main.ui".format(path_ui)
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        
        self.ui.pushButton.clicked.connect(self.click)
        
    def click(self):
        print 'A B C'

def run():
    CS = CreateScene()
    CS.show()