# MOTHER
# Houdini pipeline for VFX production

# Create folder structure for the project and copy pipeline files into it

# Common modules import
import os
import shutil
import webbrowser

# UI import
from MOTHER.ui import createProject_Main

# Py Side import
from PySide.QtGui import *

# COMMON VARIABLES
# Documentation paths
DOCS = 'https://github.com/kiryha/Houdini/wiki'
HELP = 'https://github.com/kiryha/Houdini/wiki/houdini-basics#run-new-project'
# Project paths
rootPipeline_SRC = os.path.dirname(__file__)
# Folder names to skip when copyTree
filterFolders = ['.dev', '.git', '.idea', 'hips']
# Houdini project folders
listHoudiniProjectDirs = ['comp', 'geo', 'hda', 'render', 'scenes', 'sim', 'tex']

# MAIN MODULE
class CreateProject(QMainWindow, createProject_Main.Ui_CreateProject):
    '''
    Create Project MAIN MODULE
    Set project name and location in UI, create folder structure, copy pipeline files
    '''

    def __init__(self):
        super(CreateProject, self).__init__()

        # SETUP UI
        self.setupUi(self)
        self.setFocus()  # Set active widget Main window

        self.lab_path.setText('C:')
        self.lin_name.setText('MY_PROJECT')

        # SETUP COMMON VARIABLES
        self.projectFolder = None # Project location
        self.projectName = None # Project name

        # SETUP FUNCTIONALITY
        self.act_docs.triggered.connect(lambda:  self.help(DOCS))
        self.act_help.triggered.connect(lambda:  self.help(HELP))
        self.btn_create.clicked.connect(self.createProject)
        self.btn_setFolder.clicked.connect(self.selectProjectFolder)
        self.lin_name.textChanged.connect(self.updateProjectPath)
        self.buildProjectPath()

    def help(self, URL):
        '''
        Open pipeline documentation in web browser
        '''
        webbrowser.open(URL)

    def selectProjectFolder(self):
        '''
        Allow user to select project location
        '''
        self.projectFolder = QFileDialog.getExistingDirectory(self, 'Select folder to store the project', 'C:/').replace('\\', '/')
        self.lab_path.setText(self.projectFolder)
        self.buildProjectPath() # Update path in UI

    def buildProjectPath(self):
        '''
        Create a string with full path to a project (project location + project name)
        '''
        self.projectFolder = self.lab_path.text() # Get project location
        self.updateProjectPath() # Set path in UI

    def updateProjectPath(self):
        '''
        Modify project path string in UI when user change NAME
        '''
        projectName = self.lin_name.text().replace(' ', '_') # Get project name from UI
        self.lab_path.setText('{0}/{1}'.format(self.projectFolder, projectName)) # Build full project path and update UI

    def copyTree(self, SRC, NEW):
        '''
        Copy all folder content RECURSION.
        SRC - source folder to copy from
        NEW - destination to copy all content from SRC
        '''
        if not os.path.exists(NEW):
            os.makedirs(NEW)
        for item in os.listdir(SRC):
            src = os.path.join(SRC, item).replace('\\', '/')
            new = os.path.join(NEW, item).replace('\\', '/')
            if os.path.isdir(src):
                folder = item.split('/')[-1]
                if not folder in filterFolders:
                    self.copyTree(src, new)
            else:
                if not os.path.exists(new):
                    shutil.copy2(src, new)

    def createProject(self):
        projectRoot = self.lab_path.text()

        # Create ROOT
        if not os.path.exists(projectRoot):
            os.makedirs(projectRoot)

        # Create Houdini Project Folder (temp)
        root3D = '{0}/PROD/3D'.format(projectRoot)
        os.makedirs(root3D)

        for folder in listHoudiniProjectDirs:
            os.makedirs('{}/{}'.format(root3D, folder))

        # Copy PIPELINE
        rootPipeline_NEW = '{}/PREP/PIPELINE'.format(projectRoot)
        self.copyTree(rootPipeline_SRC, rootPipeline_NEW)

        # Report
        print '>> Project created in {}'.format(projectRoot)


# Run Create Project script
app = QApplication([])
CP = CreateProject()
CP.show()
app.exec_()

