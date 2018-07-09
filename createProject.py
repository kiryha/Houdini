# MOTHER
# Houdini pipeline for VFX production

# Create folder structure for the project and copy pipeline files into it

# Common modules import
import os
import shutil
import webbrowser

# UI import
from MOTHER.ui import createProject_Main
from MOTHER.ui import createProject_SG

# Py Side import
from PySide.QtGui import *

# COMMON VARIABLES
# Documentation paths
DOCS = 'https://github.com/kiryha/Houdini/wiki'
HELP = 'https://github.com/kiryha/Houdini/wiki/Tools#create-project'
# Project paths
rootPipeline_SRC = os.path.dirname(__file__)
# Folder names to skip when run copyTree
filterFolders = ['.dev', '.git', '.idea', 'hips']
# File names to skip when run copyTree
filterFiles = ['createProject.py', 'createProject.bat', 'README.md']

# PROJECT FOLDER STRUCTURE
# Reel-sequence-shot structure
RSS = [
    ['REEL_01',[
        ['010',[
            ['SHOT_010', []],
            ['SHOT_020', []]
        ]]
    ]]
]
# Assets-shots structure
AS = [
    ['ASSETS', [
        ['CHARACTERS', []],
        ['ENVIRONMENTS', []],
        ['PROPS', []],
        ['STATIC', []]
    ]],
    ['SHOTS', RSS]
]
# Folders structure
folders = [
    ['EDIT', []],
    ['PREP', [
        ['SRC', []],
        ['PIPELINE', []],
        ]],
    ['PROD', [
        ['2D', [
            ['COMP', RSS]
        ]],
        ['3D', [
            ['comp',[]],
            ['geo',[
                ['ABC', AS],
                ['GEO', AS],
                ['FBX', AS]
            ]],
            ['hda',AS],
            ['render',[
                ['BLAST', RSS],
                ['RENDER', RSS]
            ]],
            ['scenes', AS],
            ['sim',AS],
            ['tex',AS],
        ]],
    ]]
            ]

# SHOTGUN PROJECT SETUP
class ShotgunSetup(QMainWindow, createProject_SG.Ui_SetupShotgun):
    '''
    Setup project data in Shotgun.
    Create assets and shots entities.
    '''
    def __init__(self):
        super(ShotgunSetup, self).__init__()
        self.setupUi(self)

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
        self.btn_setupSG.clicked.connect(self.setupShotgun)
        self.lin_name.textChanged.connect(self.updateProjectPath)
        self.buildProjectPath()


    def help(self, URL):
        '''
        Open pipeline documentation in web browser
        '''
        webbrowser.open(URL)

    def setupShotgun(self):
        '''
        Run User Manager
        '''
        self.sg = ShotgunSetup()
        self.sg.show()

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
                if not item in filterFiles:
                    if not os.path.exists(new):
                        shutil.copy2(src, new)

    def createProject_HDD(self):
        '''
        Create project on HDD
        :return:
        '''
        projectRoot = self.lab_path.text()

        def createFolder(path):
            # Create folder from input path
            if not os.path.exists(path):
                os.mkdir(path)


        def addFolders(pathRoot, list):
            '''
            Recursively build folder structure based on template (folders list)
            :param pathRoot:
            :param list:
            :return:
            '''
            if list:
                for folder in list:
                    folderName = folder[0]
                    path = '{}/{}'.format(pathRoot, folderName)
                    createFolder(path)
                    addFolders(path, folder[1])

        # Create project root folder
        createFolder(projectRoot)
        # Create nested folder structure
        addFolders(projectRoot, folders)

        # Copy PIPELINE
        rootPipeline_NEW = '{}/PREP/PIPELINE'.format(projectRoot)
        self.copyTree(rootPipeline_SRC, rootPipeline_NEW)

    def createProject_SG(self):
        pass

    def createProject(self):
        '''
        Create project procedure
        '''
        # Create folder structure on HDD and copy pipeline files
        self.createProject_HDD()
        # Create project in Shotgun
        if self.chb_skipSG.isChecked() != True:
            self.createProject_SG()
        # Report about creation
        print '>> Project created in {}'.format(self.lab_path.text())


# Run Create Project script
app = QApplication([])
CP = CreateProject()
CP.show()
app.exec_()

