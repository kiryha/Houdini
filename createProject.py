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
from MOTHER.ui import createProject_Warning

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
# Nested lists basic block is ['FOLDERNAME', []]
# Sequence-shot structure
# Add reel level for a big projects
SS = [
    ['010',[
        ['SHOT_010', []],
        ['SHOT_020', []]
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
    ['SHOTS', SS]
    ]
# Folders structure
folders = [
    ['EDIT', [
        ['OUT', []],
        ['PROJECT', []]
    ]],
    ['PREP', [
        ['ART', []],
        ['SRC', []],
        ['PIPELINE', []],
        ]],
    ['PROD', [
        ['2D', [
            ['COMP', SS],
            ['RENDER', SS]
        ]],
        ['3D', [
            ['comp', []],
            ['geo',[
                ['ABC', AS],
                ['GEO', AS],
                ['FBX', AS]
            ]],
            ['hda',AS],
            ['render', SS],
            ['scenes', [
                ['ANIMATION', SS],
                ['LAYOUT', SS],
                ['RENDER', SS]
            ]],
            ['sim', AS],
            ['tex', AS],
        ]],
    ]]
    ]

# WARNING WINDOW
class Warning(QWidget, createProject_Warning.Ui_warning):
    '''
    Warning window.
    Show existing project path,
    send back to a parent class (CreateProject.createProject function) user choice (OK or NO)
    '''
    def __init__(self, parent, message):
        super(Warning, self).__init__()

        # SETUP UI
        self.setupUi(self)
        self.parent = parent
        self.lab_warning.setText('Folder <{0}> exists!'.format(message))

        # SETUP FUNCTIONALITY
        self.btn_proceed.clicked.connect(self.proceed)
        self.btn_proceed.clicked.connect(self.close)
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_cancel.clicked.connect(self.close)

    def proceed(self):
        # PROCEED button
        CreateProject.createProject(self.parent, 'OK')

    def cancel(self):
        # CANCEL button
        CreateProject.createProject(self.parent, 'NO')

# SHOTGUN PROJECT SETUP
class ShotgunSetup(QMainWindow, createProject_SG.Ui_SetupShotgun):
    '''
    Setup project data in Shotgun.
    Create assets and shots entities.
    '''
    def __init__(self):
        super(ShotgunSetup, self).__init__()

        # SETUP UI
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
        Run Shotgun Setup window
        '''
        self.sg = ShotgunSetup()
        self.sg.show()

    def selectProjectFolder(self):
        '''
        Let user to select project location
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

    def createFolder(self, path):
        '''
        Create folder from input path
        :param path: Path to create folder
        '''
        if not os.path.exists(path):
            os.mkdir(path)

    def createFolders(self, pathRoot, list):
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
                self.createFolder(path)
                self.createFolders(path, folder[1])

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

    def createProject_HDD(self, projectRoot):
        '''
        Create project on HDD in project root folder and copy pipeline files
        :return:
        '''

        # Create nested folder structure
        self.createFolders(projectRoot, folders)
        # Copy PIPELINE
        rootPipeline_NEW = '{}/PREP/PIPELINE'.format(projectRoot)
        self.copyTree(rootPipeline_SRC, rootPipeline_NEW)

        print '>> Folder structure with pipeline files created in {0}/'.format(projectRoot)

    def createProject_SG(self, projectName):
        print '>> Project {0} created in Shotgun.'.format(projectName)

    def createProject(self, catchWarning = None):
        '''
        Create new project on HDD and in Shotgun:
        :param catchWarning: returned value from Warning class (OK or NO)
        '''

        projectRoot = self.lab_path.text()
        projectName = self.lin_name.text()

        # HDD
        # Create folder structure on HDD and copy pipeline files

        if os.path.exists(projectRoot):
            # If project folder already exists
            if catchWarning == None:
                # Run warning dialog
                self.warning = Warning(self, projectRoot)  # Run SNV window
                win = self.warning.show()

                if not win:  # Prevent script to run further before user reply in warning UI
                    return

            elif catchWarning == 'OK':
                # Create project structure on HDD in existing folder
                self.createProject_HDD(projectRoot)
            else:
                return
        else:
            # Create new project structure on HDD
            self.createFolder(projectRoot)
            self.createProject_HDD(projectRoot)

        # SHOTGUN
        # Create project in Shotgun
        if self.chb_skipSG.isChecked() != True:
            self.createProject_SG(projectName)

        # Report about creation
        print '>> Project creation complete!'
        print '>> Run Houdini with {0}/PREP/PIPELINE/runHoudini.bat and create some magic!'.format(projectRoot)


# Run Create Project script
app = QApplication([])
CP = CreateProject()
CP.show()
app.exec_()

