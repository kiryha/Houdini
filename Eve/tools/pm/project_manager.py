import os
import sqlite3
import subprocess
import webbrowser
from PySide2 import QtCore, QtWidgets

# Import UI
from ui import ui_pm_warning
from ui import ui_link_assets
from ui import ui_pm_main
from ui import ui_project
from ui import ui_project_properties
from ui import ui_pm_add_project
from ui import ui_asset
from ui import ui_asset_properties
from ui import ui_pm_add_asset
from ui import ui_sequence
from ui import ui_sequence_properties
from ui import ui_pm_add_sequence
from ui import ui_shot
from ui import ui_shot_properties
from ui import ui_pm_add_shot

from core.database import entities
from core.database import eve_data
from core import settings
from core import models

import houdini_launcher


def build_project_root(project_name):
    """Build project root folder string"""

    project_root = '{0}/{1}'.format(settings.PROJECTS, project_name)
    return project_root


def build_folder_structure():
    """
    Create list for project folder structure

    TODO: build assets, sequences and shots folders based on EVE data
    assets=None, shots=None

    :param assets: list of Asset objects, assets of current project
    :param shots:  list of Shot objects, shots of current project
    :return:
    """

    # PROJECT FOLDER STRUCTURE
    # Shots structure
    SHOTS = [
        ['010', [
            ['SHOT_010', []],
            ['SHOT_020', []]
        ]]
    ]
    # Assets structure
    ASSETS = [
        ['CHARACTERS', []],
        ['ENVIRONMENTS', []],
        ['PROPS', []],
        ['STATICS', []],
        ['FX', []]
    ]
    # Types structure
    TYPES = [
        ['ASSETS', ASSETS],
        ['SHOTS', SHOTS]
    ]
    # Formats structure
    FORMATS = [
        ['ABC', []],
        ['GEO', []],
        ['FBX', []]
    ]
    # Folders structure
    FOLDERS = [
        ['EDIT', [
            ['OUT', []],
            ['PROJECT', []]
        ]],
        ['PREP', [
            ['ART', []],
            ['SRC', []],
            ['PIPELINE', [
                ['genes', []]
            ]],
        ]],
        ['PROD', [
            ['2D', [
                ['COMP', SHOTS],
                ['RENDER', SHOTS]
            ]],
            ['3D', [
                ['lib', [
                    ['ANIMATION', []],
                    ['MATERIALS', [
                        ['MANTRA', []]
                    ]]
                ]],
                ['fx', TYPES],
                ['caches', TYPES],
                ['hda', [
                    ['ASSETS', ASSETS],
                    ['FX', TYPES],
                ]],
                ['render', SHOTS],
                ['scenes', [
                    ['ASSETS', ASSETS],
                    ['SHOTS', [
                        ['ANIMATION', SHOTS],
                        ['LAYOUT', SHOTS],
                        ['RENDER', SHOTS]
                    ]]
                ]],
                ['textures', TYPES],
            ]],
        ]]
    ]

    return FOLDERS


class Warnings(QtWidgets.QDialog, ui_pm_warning.Ui_Warning):
    def __init__(self, name):
        # SETUP UI WINDOW
        super(Warnings, self).__init__()
        self.setupUi(self)

        message = 'Delete {}?'.format(name)
        self.labWarning.setText(message)


class LinkAssets(QtWidgets.QDialog, ui_link_assets.Ui_LinkAssets):
    """
    Create asset entity in the database
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(LinkAssets, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent

        self.shot = None
        self.project_assets = None
        self.model_assets = None

        self.btnLinkAssets.clicked.connect(self.link_asset)
        self.btnLinkAssets.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AddProject class is shown (AddProject.show())
        """

        # Clean UI
        self.linShotName.setText(self.shot.name)
        # self.asset_ui.linAssetName.clear()
        # self.asset_ui.txtDescription.clear()
        #
        # Add assets to ui
        self.model_assets = models.ListModel(self.project_assets)
        self.listAssets.setModel(self.model_assets)

    def link_asset(self):
        """
        Link assets to the shots
        """

        model_indexes = self.listAssets.selectedIndexes()
        self.parent.link_assets(model_indexes, self.shot)


class ProjectUI(QtWidgets.QWidget, ui_project.Ui_Project):
    def __init__(self):
        super(ProjectUI, self).__init__()
        self.setupUi(self)
        self.linHoudini.setText(settings.default_build)


class AssetUI(QtWidgets.QWidget, ui_asset.Ui_Asset):
    def __init__(self):
        super(AssetUI, self).__init__()
        self.setupUi(self)


class SequenceUI(QtWidgets.QWidget, ui_sequence.Ui_Sequence):
    def __init__(self):
        super(SequenceUI, self).__init__()
        self.setupUi(self)


class ShotUI(QtWidgets.QWidget, ui_shot.Ui_Shot):
    def __init__(self):
        super(ShotUI, self).__init__()
        self.setupUi(self)


class ProjectProperties(QtWidgets.QWidget, ui_project_properties.Ui_ProjectProperties):
    def __init__(self):
        super(ProjectProperties, self).__init__()
        self.setupUi(self)
        self.project_ui = ProjectUI()
        self.layoutProject.addWidget(self.project_ui)


class AssetProperties(QtWidgets.QWidget, ui_asset_properties.Ui_AssetProperties):
    def __init__(self):
        super(AssetProperties, self).__init__()
        self.setupUi(self)
        self.asset_ui = AssetUI()
        self.layoutAsset.addWidget(self.asset_ui)


class SequenceProperties(QtWidgets.QWidget, ui_sequence_properties.Ui_SequenceProperties):
    def __init__(self):
        super(SequenceProperties, self).__init__()
        self.setupUi(self)
        self.sequence_ui = SequenceUI()
        self.layoutSequence.addWidget(self.sequence_ui)


class ShotProperties(QtWidgets.QWidget, ui_shot_properties.Ui_ShotProperties):
    def __init__(self):
        super(ShotProperties, self).__init__()
        self.setupUi(self)
        self.shot_ui = ShotUI()
        self.layoutShot.addWidget(self.shot_ui)


class AddProject(QtWidgets.QDialog, ui_pm_add_project.Ui_AddProject):
    """
    Add project entity Dialog.
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(AddProject, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent
        self.project_ui = ProjectUI()
        self.layoutProject.addWidget(self.project_ui)
        self.project_ui.linProjectLocation.setEnabled(False)

        self.project_ui.linProjectName.textChanged.connect(self.project_name_changed)
        # self.project_ui.btnPickMaya.clicked.connect(self.pick_maya)
        self.btnAddProject.clicked.connect(self.add_project)
        self.btnAddProject.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AppProject class is shown (AddProject.show())
        :param event:
        :return:
        """

        # Clean UI
        self.project_ui.linProjectName.clear()
        self.project_ui.txtDescription.clear()
        self.project_ui.linProjectName.clear()

    def project_name_changed(self):

        project_name = self.project_ui.linProjectName.text()
        project_root = build_project_root(project_name)
        self.project_ui.linProjectLocation.setText(project_root)

    def add_project(self):
        """
        Create asset entity in datatbase
        :return:
        """

        # Get project data from UI
        project_name = self.project_ui.linProjectName.text()
        houdini_build = self.project_ui.linHoudini.text()
        project_width = self.project_ui.linProjectWidth.text()
        project_height = self.project_ui.linProjectHeight.text()
        project_description = self.project_ui.txtDescription.toPlainText()

        # Call add_project in PM class
        self.parent.add_project(project_name, houdini_build, project_width, project_height, project_description)


class AddAsset(QtWidgets.QDialog, ui_pm_add_asset.Ui_AddAsset):
    """
    Create asset entity in the database
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(AddAsset, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent
        self.asset_ui = AssetUI()
        self.layoutAsset.addWidget(self.asset_ui)

        self.project = None
        self.asset_types = None
        self.model_asset_types = None

        self.btnAddAsset.clicked.connect(self.add_asset)
        self.btnAddAsset.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AddProject class is shown (AddProject.show())
        """

        # Clean UI
        self.asset_ui.linProjectName.setText(self.project.name)
        self.asset_ui.linAssetName.clear()
        self.asset_ui.txtDescription.clear()

        # Add asset types to ui
        self.model_asset_types = models.ListModel(self.asset_types)
        self.asset_ui.comAssetType.setModel(self.model_asset_types)

    def add_asset(self):
        """
        Create asset entity in the DB
        """

        # Get asset name from UI
        asset_name = self.asset_ui.linAssetName.text()
        asset_type_index = self.asset_ui.comAssetType.model().index(self.asset_ui.comAssetType.currentIndex(), 0)
        asset_type_id = asset_type_index.data(QtCore.Qt.UserRole + 1)
        # asset_publish = self.asset_ui.linHDAName.text()
        asset_description = self.asset_ui.txtDescription.toPlainText()

        self.parent.add_asset(self.project, asset_name, asset_type_id, asset_description)


class AddSequence(QtWidgets.QDialog, ui_pm_add_sequence.Ui_AddSequence):
    """
    Create sequence entity in the database
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(AddSequence, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent
        self.sequence_ui = SequenceUI()
        self.layoutSequence.addWidget(self.sequence_ui)

        self.project = None

        self.btnAddSequence.clicked.connect(self.add_sequence)
        self.btnAddSequence.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AddSequence class is shown (AddSequence.show())
        :param event:
        :return:
        """

        self.sequence_ui.linProjectName.setText(self.project.name)
        self.sequence_ui.linSequenceName.clear()
        self.sequence_ui.txtDescription.clear()

    def add_sequence(self):
        """
        Create sequence entity in the DB
        :return:
        """

        # Get sequence name from UI
        sequence_name = self.sequence_ui.linSequenceName.text()
        sequence_description = self.sequence_ui.txtDescription.toPlainText()

        self.parent.add_sequence(self.project, sequence_name, sequence_description)


class AddShot(QtWidgets.QDialog, ui_pm_add_shot.Ui_AddShot):
    """
    Create shot entity in the database
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(AddShot, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent
        self.shot_ui = ShotUI()
        self.layoutShot.addWidget(self.shot_ui)

        self.project = None
        self.sequence = None

        self.btnAddShot.clicked.connect(self.add_shot)
        self.btnAddShot.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AddShot class is shown (AddShot.show())
        """

        self.shot_ui.btnLinkAsset.setEnabled(False)
        self.shot_ui.btnUnlinkAsset.setEnabled(False)
        self.shot_ui.linProjectName.setText(self.project.name)
        self.shot_ui.linSequenceName.setText(self.sequence.name)
        self.shot_ui.linShotName.clear()
        self.shot_ui.txtDescription.clear()

    def add_shot(self):
        """
        Create sequence entity in the DB
        """

        # Get sequence name from UI
        shot_name = self.shot_ui.linShotName.text()
        shot_start_frame = self.shot_ui.linStartFrame.text()
        shot_end_frame = self.shot_ui.linEndFrame.text()
        shot_width = self.shot_ui.linWidth.text()
        shot_height = self.shot_ui.linHeight.text()
        shot_description = self.shot_ui.txtDescription.toPlainText()

        self.parent.add_shot(self.sequence,
                             shot_name,
                             shot_start_frame,
                             shot_end_frame,
                             shot_width,
                             shot_height,
                             shot_description)


class ProjectManager(QtWidgets.QMainWindow,  ui_pm_main.Ui_ProjectManager):
    """
    Custom "Shotgun". Create, edit, delete projects data. Launch apps

    Project, Asset, Sequence, Shot widgets are nested (to reuse same widget in 2 places):
        ASSET >> ASSET PROPERTIES >> PROJECT MANAGER
        ASSET >> ADD ASSET

    """

    def __init__(self):
        super(ProjectManager, self).__init__()
        # SETUP UI
        self.setupUi(self)
        self.project_properties_ui = ProjectProperties()
        self.asset_properties_ui = AssetProperties()
        self.sequence_properties_ui = SequenceProperties()
        self.shot_properties_ui = ShotProperties()
        self.layoutProperties.addWidget(self.project_properties_ui)
        self.layoutProperties.addWidget(self.asset_properties_ui)
        self.layoutProperties.addWidget(self.sequence_properties_ui)
        self.layoutProperties.addWidget(self.shot_properties_ui)
        self.btn_project_create = 'Create Project'
        self.btn_project_update = 'Update Project'

        # SETUP ENVIRONMENT
        os.environ['EVE_ROOT'] = os.environ['EVE_ROOT'].replace('\\', '/')
        self.eve_root = os.environ['EVE_ROOT']  # E:/Eve/Eve

        # Load Eve DB
        # Create database file if not exists (first time Project Manager launch)
        self.SQL_FILE_PATH = settings.SQL_FILE_PATH.format(self.eve_root)
        if not os.path.exists(self.SQL_FILE_PATH):
            if not os.path.exists(os.path.dirname(self.SQL_FILE_PATH)):
                os.makedirs(os.path.dirname(self.SQL_FILE_PATH))
            self.create_database()
        self.eve_data = eve_data.EveData(self.SQL_FILE_PATH)
        self.model_projects = models.ListModel(self.eve_data.projects)
        self.model_assets = None
        self.model_sequences = None
        self.model_shots = None
        self.model_shot_assets = None

        # Eve data
        self.selected_project = None
        self.selected_asset = None
        self.selected_sequence = None
        self.selected_shot = None

        # Load ADD ENTITY classes
        self.AP = AddProject(self)
        self.AA = AddAsset(self)
        self.AE = AddSequence(self)
        self.AS = AddShot(self)
        self.LA = LinkAssets(self)

        # Fill UI with data from database
        self.init_pm()

        # Connect functions
        # Menu
        self.actionEveDocs.triggered.connect(self.docs)
        # Project section
        self.listProjects.clicked.connect(self.init_project)
        self.btnAddProject.clicked.connect(self.AP.exec_)
        self.btnDelProject.clicked.connect(self.del_project)
        # Asset section
        self.listAssets.clicked.connect(self.init_asset)
        self.btnAddAsset.clicked.connect(self.run_add_asset)
        self.btnDelAsset.clicked.connect(self.del_asset)
        # Sequence section
        self.listSequences.clicked.connect(self.init_sequence)
        self.btnAddSequence.clicked.connect(self.run_add_sequence)
        self.btnDelSequence.clicked.connect(self.del_sequence)
        # Shot section
        self.listShots.clicked.connect(self.init_shot)
        self.btnAddShot.clicked.connect(self.run_add_shot)
        self.btnDelShot.clicked.connect(self.del_shot)

        # Project properties
        self.project_properties_ui.btnCreateProject.clicked.connect(self.run_create_project)
        self.project_properties_ui.btnLaunchHoudini.clicked.connect(self.launch_houdini)

        # Asset properties
        self.asset_properties_ui.btnUpdateAsset.clicked.connect(self.update_asset)
        self.asset_properties_ui.btnCreateHoudiniFile.clicked.connect(self.create_asset_file)

        # Sequence properties
        self.sequence_properties_ui.btnUpdateSequence.clicked.connect(self.update_sequence)

        # Shot properties
        self.shot_properties_ui.btnUpdateShot.clicked.connect(self.update_shot)
        self.shot_properties_ui.shot_ui.btnLinkAsset.clicked.connect(self.run_link_assets)
        self.shot_properties_ui.shot_ui.btnUnlinkAsset.clicked.connect(self.run_unlink_assets)

    def docs(self):
        """
        Run Carry Over HELP in web browser
        """

        # Root folder for the report files
        webbrowser.open(settings.DOCS)

    def init_database(self, connection, cursor):
        """
        Create database tables
        :return:
        """

        # TYPES
        cursor.execute('''CREATE TABLE asset_types (
                        id integer primary key autoincrement,
                        name text,
                        description text
                        )''')

        cursor.execute('''CREATE TABLE file_types (
                        id integer primary key autoincrement,
                        name text,
                        description text
                        )''')

        # MAIN ITEMS
        cursor.execute('''CREATE TABLE projects (
                        id integer primary key autoincrement,
                        name text,
                        houdini_build text,
                        width integer,
                        height integer,
                        description text
                        )''')

        cursor.execute('''CREATE TABLE assets (
                        id integer primary key autoincrement,
                        name text,
                        project integer,
                        type integer,
                        description text,
                        FOREIGN KEY(project) REFERENCES projects(id)
                        FOREIGN KEY(type) REFERENCES asset_types(id)
                        )''')

        cursor.execute('''CREATE TABLE sequences (
                        id integer primary key autoincrement,
                        name text,
                        project integer,
                        description text,
                        FOREIGN KEY(project) REFERENCES projects(id)
                        )''')

        cursor.execute('''CREATE TABLE shots (
                        id integer primary key autoincrement,
                        name text,
                        sequence integer,
                        start_frame integer,
                        end_frame integer,
                        width integer, 
                        height integer,
                        description text,
                        FOREIGN KEY(sequence) REFERENCES sequences(id)
                        )''')

        # FILES
        cursor.execute('''CREATE TABLE asset_files (
                        id integer primary key autoincrement,
                        type integer,
                        asset integer,
                        snapshot integer,
                        description text,
                        FOREIGN KEY(type) REFERENCES file_types(id)
                        FOREIGN KEY(asset) REFERENCES assets(id)
                        FOREIGN KEY(snapshot) REFERENCES asset_snapshots(id)
                        )''')

        cursor.execute('''CREATE TABLE shot_files (
                        id integer primary key autoincrement,
                        type integer,
                        shot integer,
                        snapshot integer,
                        description text,
                        FOREIGN KEY(type) REFERENCES file_types(id)
                        FOREIGN KEY(shot) REFERENCES shots(id)
                        FOREIGN KEY(snapshot) REFERENCES shot_snapshots(id)
                        )''')

        # LINKS
        # Link assets to the shots
        cursor.execute('''CREATE TABLE shot_assets (
                        id integer primary key autoincrement,
                        shot_id integer,
                        asset_id integer,
                        FOREIGN KEY(shot_id) REFERENCES shots(id)
                        FOREIGN KEY(asset_id) REFERENCES assets(id)
                        )''')

        # SNAPSHOTS
        cursor.execute('''CREATE TABLE asset_snapshot (
                        id integer primary key autoincrement,
                        asset_name text,
                        asset_id text,
                        asset_version text,
                        description text
                        )''')

        connection.commit()

    def init_asset_types(self, connection, cursor):
        """
        Fill asset types table in the DB (character, environment, prop, FX)

        :param connection:
        :param cursor:
        :return:
        """

        for name, data in entities.Asset.asset_types.iteritems():
            cursor.execute("INSERT INTO asset_types VALUES ("
                           ":id,"
                           ":name,"
                           ":description)",

                           {'id': data['id'],
                            'name': name,
                            'description': data['description']})

        connection.commit()

    def init_file_types(self, connection, cursor):
        """
        Fill file types table in the DB.

        Any file used in Eve should has a particular type. Here is the full list of all possible types in Eve.

        asset_hip:
            Working scene for Assets. Here we store all source data to build an asset. Results are exported as caches,
            and caches used in asset_hda files.

        asset_hda:
            Houdini Digital Asset for ASSETS. Used to load assets of any type (char, env, props, fx) into shots.
            Contain cached data with interface. Source of cached data is stored in asset_hip

        :param connection:
        :param cursor:
        :return:
        """

        for name, data in entities.EveFile.file_types.iteritems():
            cursor.execute("INSERT INTO file_types VALUES ("
                           ":id,"
                           ":name,"
                           ":description)",

                           {'id': data['id'],
                            'name': name,
                            'description': data['description']})

        connection.commit()

    def init_default_project(self, SQL_FILE_PATH, project_name):
        """
        Create Library project for Athena materials
        :param SQL_FILE_PATH:
        :return:
        """

        project = entities.Project(project_name)
        project.houdini_build = '{0}'.format(settings.HOUDINI)
        project.description = 'Eve default project for documentation and tutorials.'

        connection = sqlite3.connect(SQL_FILE_PATH)
        cursor = connection.cursor()

        # Add "library" project to DB
        cursor.execute("INSERT INTO projects VALUES ("
                       ":id,"
                       ":name,"
                       ":houdini_build,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': project.name,
                        'houdini_build': project.houdini_build,
                        'description': project.description})

        connection.commit()
        project.id = cursor.lastrowid  # Add database ID to the project object
        connection.close()

        # Add asset for the project
        # asset = entities.Asset('U256', project.id)
        #
        # connection = sqlite3.connect(SQL_FILE_PATH)
        # cursor = connection.cursor()
        #
        # cursor.execute("INSERT INTO assets VALUES ("
        #                ":id,"
        #                ":name,"
        #                ":project_id,"
        #                ":description)",
        #
        #                {'id': cursor.lastrowid,
        #                 'name': asset.name,
        #                 'project_id': asset.project_id,
        #                 'description': asset.description})
        #
        # connection.commit()
        # project.id = cursor.lastrowid  # Add database ID to the project object
        # connection.close()

    def create_database(self):
        """
        Create database file with necessary tables
        :return:
        """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        self.init_database(connection, cursor)
        self.init_asset_types(connection, cursor)
        self.init_file_types(connection, cursor)
        self.init_default_project(self.SQL_FILE_PATH, 'eve_example')

        connection.close()

    def init_pm(self):
        """
        Read Athena database and populate information in Project Manager UI
        :return:
        """

        # Hide PROPERTIES widgets
        self.project_properties_ui.hide()
        self.asset_properties_ui.hide()
        self.sequence_properties_ui.hide()
        self.shot_properties_ui.hide()

        # Fill PROJECTS and MATERIALS views
        self.listProjects.setModel(self.model_projects)

    def init_project(self):
        """
        When PROJECT selected in UI
        """

        # Show and set up PROPERTIES widget
        self.project_properties_ui.show()
        self.asset_properties_ui.hide()
        self.sequence_properties_ui.hide()
        self.shot_properties_ui.hide()

        # Setup data
        model_index = self.listProjects.currentIndex()  # .selectedIndexes()[0]
        project_id = model_index.data(QtCore.Qt.UserRole + 1)
        project = self.eve_data.get_project(project_id)
        self.selected_project = project
        self.eve_data.get_project_assets(project)
        self.eve_data.get_project_sequences(project)

        # Clear SHOTS in UI
        self.listShots.setModel(models.ListModel([]))

        # Fill Project Properties widget
        project_root = build_project_root(project.name)
        self.project_properties_ui.project_ui.linProjectLocation.setText(project_root)
        self.project_properties_ui.project_ui.linProjectLocation.setEnabled(False)
        self.project_properties_ui.project_ui.linProjectName.setText(project.name)
        self.project_properties_ui.project_ui.linProjectName.setEnabled(False)
        self.project_properties_ui.project_ui.linHoudini.setText(project.houdini_build)
        self.project_properties_ui.project_ui.linProjectWidth.setText(str(project.width))
        self.project_properties_ui.project_ui.linProjectHeight.setText(str(project.height))
        self.project_properties_ui.project_ui.txtDescription.setText(project.description)

        # FILL ASSET and SEQUENCE WIDGETS
        self.model_assets = models.ListModel(self.eve_data.project_assets)
        self.listAssets.setModel(self.model_assets)

        self.model_sequences = models.ListModel(self.eve_data.project_sequences)
        self.listSequences.setModel(self.model_sequences)

        # Enable/disable UI buttons depending on project existence
        if os.path.exists(project_root):
            self.project_properties_ui.btnCreateProject.setText(self.btn_project_update)
            self.project_properties_ui.btnLaunchHoudini.setEnabled(True)
            self.project_properties_ui.btnLaunchNuke.setEnabled(True)
            self.project_properties_ui.btnOpenFolder.setEnabled(True)
        else:
            self.project_properties_ui.btnCreateProject.setText(self.btn_project_create)
            self.project_properties_ui.btnLaunchHoudini.setEnabled(False)
            self.project_properties_ui.btnLaunchNuke.setEnabled(False)
            self.project_properties_ui.btnOpenFolder.setEnabled(False)

    def init_asset(self):
        """
        When ASSET selected in UI
        """

        # Show and set up PROPERTIES widget
        self.project_properties_ui.hide()
        self.asset_properties_ui.show()
        self.sequence_properties_ui.hide()
        self.shot_properties_ui.hide()

        # Setup data
        model_index = self.listAssets.currentIndex()
        asset_id = model_index.data(QtCore.Qt.UserRole + 1)
        asset = self.eve_data.get_asset(asset_id)
        self.selected_asset = asset

        # Fill ASSET WIDGET
        self.asset_properties_ui.asset_ui.linAssetName.setEnabled(False)
        self.asset_properties_ui.asset_ui.linProjectName.setText(self.selected_project.name)
        self.asset_properties_ui.asset_ui.linAssetName.setText(asset.name)

        model_asset_types = models.ListModel(self.eve_data.asset_types)
        self.asset_properties_ui.asset_ui.comAssetType.setModel(model_asset_types)
        # Find AssetType string by database index
        # !!! Probably wrong implementation of model data! and can be done via ListModel() !!!!!
        asset_type_string = self.eve_data.get_asset_type_string(asset.type)
        self.asset_properties_ui.asset_ui.comAssetType.setCurrentText(asset_type_string)
        self.asset_properties_ui.asset_ui.txtDescription.setText(asset.description)

    def init_sequence(self):
        """
        When SEQUENCE selected in UI
        """

        # Show and set up PROPERTIES widget
        self.project_properties_ui.hide()
        self.asset_properties_ui.hide()
        self.sequence_properties_ui.show()
        self.shot_properties_ui.hide()

        # Setup data for sequence
        model_index = self.listSequences.currentIndex()
        sequence_id = model_index.data(QtCore.Qt.UserRole + 1)
        sequence = self.eve_data.get_sequence(sequence_id)
        self.selected_sequence = sequence
        # and shot
        self.eve_data.get_sequence_shots(sequence.id)
        self.model_shots = models.ListModel(self.eve_data.sequence_shots)
        self.listShots.setModel(self.model_shots)

        # Fill SEQUENCE WIDGET
        self.sequence_properties_ui.sequence_ui.linSequenceName.setEnabled(False)
        self.sequence_properties_ui.sequence_ui.linProjectName.setText(self.selected_project.name)
        self.sequence_properties_ui.sequence_ui.linSequenceName.setText(sequence.name)
        self.sequence_properties_ui.sequence_ui.txtDescription.setText(sequence.description)

    def init_shot(self):
        """
        When SHOT selected in UI
        """

        # Show and set up PROPERTIES widget
        self.project_properties_ui.hide()
        self.asset_properties_ui.hide()
        self.sequence_properties_ui.hide()
        self.shot_properties_ui.show()

        # Setup data
        model_index = self.listShots.currentIndex()
        shot_id = model_index.data(QtCore.Qt.UserRole + 1)
        shot = self.eve_data.get_shot(shot_id)
        self.selected_shot = shot

        # FILL SHOT ASSETS WIDGET
        self.eve_data.get_shot_assets(shot_id)
        self.model_shot_assets = models.ListModel(self.eve_data.shot_assets)
        self.shot_properties_ui.shot_ui.listAssets.setModel(self.model_shot_assets)

        # Fill SHOT WIDGET
        self.shot_properties_ui.shot_ui.linShotName.setEnabled(False)
        self.shot_properties_ui.shot_ui.linProjectName.setText(self.selected_project.name)
        self.shot_properties_ui.shot_ui.linSequenceName.setText(self.selected_sequence.name)
        self.shot_properties_ui.shot_ui.linShotName.setText(self.selected_shot.name)
        self.shot_properties_ui.shot_ui.linStartFrame.setText(str(shot.start_frame))
        self.shot_properties_ui.shot_ui.linEndFrame.setText(str(shot.end_frame))
        self.shot_properties_ui.shot_ui.linWidth.setText(str(shot.width))
        self.shot_properties_ui.shot_ui.linHeight.setText(str(shot.height))
        self.shot_properties_ui.shot_ui.txtDescription.setText(shot.description)

    def add_project(self, project_name, houdini_build, project_width, project_height, project_description):
        """
        Add project to database and reload UI
        """

        # Create project object
        project = entities.Project(project_name)
        project.houdini_build = houdini_build
        project.width = project_width
        project.height = project_height
        project.description = project_description

        # Add project to DB and update UI
        self.model_projects.layoutAboutToBeChanged.emit()
        self.eve_data.add_project(project)
        self.model_projects.layoutChanged.emit()

    def add_asset(self, project, asset_name, asset_type_id, asset_description):
        """
        Add new asset data to the DB
        """

        # Create asset and set asset properties
        asset = entities.Asset(asset_name, project.id)
        asset.type = asset_type_id
        asset.description = asset_description

        # Add asset to DB and update UI
        self.model_assets.layoutAboutToBeChanged.emit()
        self.eve_data.add_asset(asset, project.id)
        self.model_assets.layoutChanged.emit()

    def add_sequence(self, project, sequence_name, sequence_description):

        # Create sequence and set sequence properties
        sequence = entities.Sequence(sequence_name, project.id)
        sequence.description = sequence_description

        # Add asset to DB and update UI
        self.model_sequences.layoutAboutToBeChanged.emit()
        self.eve_data.add_sequence(sequence, project.id)
        self.model_sequences.layoutChanged.emit()

    def add_shot(self, sequence, shot_name, shot_start_frame, shot_end_frame, shot_width, shot_height, shot_description):

        # Create shot and set shot properties
        shot = entities.Shot(shot_name, sequence.id)
        shot.start_frame = shot_start_frame
        shot.end_frame = shot_end_frame
        shot.width = shot_width
        shot.height = shot_height
        shot.description = shot_description

        # Add asset to DB and update UI
        self.model_shots.layoutAboutToBeChanged.emit()
        self.eve_data.add_shot(shot, sequence.id)
        self.model_shots.layoutChanged.emit()

    def del_project(self):
        """
        Delete project from database, update UI
        """

        model_index = self.listProjects.currentIndex()
        project_id = model_index.data(QtCore.Qt.UserRole + 1)
        project_name = model_index.data(QtCore.Qt.UserRole + 2)

        # Notify user about deletion
        warn = Warnings(project_name)
        if warn.exec_():
            # Remove project from DB
            self.model_projects.layoutAboutToBeChanged.emit()
            self.eve_data.del_project(project_id)
            self.model_projects.layoutChanged.emit()

    def del_asset(self):
        """
        Delete shot from database, update UI
        """

        # Notify user about delete
        warning = Warnings(self.selected_asset.name)
        if warning.exec_():
            self.model_assets.layoutAboutToBeChanged.emit()
            self.eve_data.del_asset(self.selected_asset.id)
            self.model_assets.layoutChanged.emit()

    def del_sequence(self):

        # Notify user about delete
        warning = Warnings(self.selected_sequence.name)
        if warning.exec_():
            self.model_sequences.layoutAboutToBeChanged.emit()
            self.eve_data.del_sequence(self.selected_sequence.id)
            self.model_sequences.layoutChanged.emit()

    def del_shot(self):

        # Notify user about delete
        warning = Warnings(self.selected_shot.name)
        if warning.exec_():
            self.model_shots.layoutAboutToBeChanged.emit()
            self.eve_data.del_shot(self.selected_shot.id)
            self.model_shots.layoutChanged.emit()

    def update_project(self):
        """
        Update project data in the DB
        """

        print '>> Updating project...'

        # Load athena data
        project = self.selected_project

        # Update project data
        project.maya = self.project_properties_ui.project_ui.linHoudini.text()
        project.width = self.project_properties_ui.project_ui.linProjectWidth.text()
        project.height = self.project_properties_ui.project_ui.linProjectHeight.text()
        project.description = self.project_properties_ui.project_ui.txtDescription.toPlainText()

        self.eve_data.update_project(project)

        # Update folder structure on HDD
        # FOLDERS = build_folder_structure()
        # self.create_folders(build_project_root(project_name), FOLDERS)

        print '>> Project {0} updated!'.format(project.name)

    def update_asset(self):
        """
        Update asset data in DB according to Asset Properties widget.
        """

        print '>> Updating asset...'

        # Get asset
        asset = self.selected_asset

        # Modify asset data
        asset_type_index = self.asset_properties_ui.asset_ui.comAssetType.model().index(
                                                    self.asset_properties_ui.asset_ui.comAssetType.currentIndex(), 0)
        asset_type_id = asset_type_index.data(QtCore.Qt.UserRole + 1)

        asset.type = asset_type_id
        asset.description = self.asset_properties_ui.asset_ui.txtDescription.toPlainText()

        # Save asset data
        self.eve_data.update_asset(asset)

        print '>> Asset "{}" updated!'.format(asset.name)

    def update_sequence(self):
        """
        Update sequence data in DB according to Sequence Properties widget.

        """

        print '>> Updating sequence...'

        # Get sequence
        sequence = self.selected_sequence

        # Modify sequence data
        sequence.description = self.sequence_properties_ui.sequence_ui.txtDescription.toPlainText()

        # Save sequence data
        self.eve_data.update_sequence(sequence)

        print '>> Sequence "{}" updated!'.format(sequence.name)

    def update_shot(self):
        """
        Update sequence data in DB according to Sequence Properties widget.
        """

        print '>> Updating shot...'

        # Get shot
        shot = self.selected_shot

        # Modify shot data
        shot.start_frame = self.shot_properties_ui.shot_ui.linStartFrame.text()
        shot.end_frame = self.shot_properties_ui.shot_ui.linEndFrame.text()
        shot.width = self.shot_properties_ui.shot_ui.linWidth.text()
        shot.height = self.shot_properties_ui.shot_ui.linHeight.text()
        shot.description = self.shot_properties_ui.shot_ui.txtDescription.toPlainText()

        # Save shot data
        self.eve_data.update_shot(shot)

        print '>> Shot "{}" updated!'.format(shot.name)

    def link_assets(self, model_indexes, shot):

        for model_index in model_indexes:
            # Link asset
            if self.eve_data.link_asset(model_index.data(QtCore.Qt.UserRole + 1), shot.id):
                # Updated UI
                self.model_shot_assets.layoutAboutToBeChanged.emit()
                self.eve_data.get_shot_assets(shot.id)
                self.model_shot_assets.layoutChanged.emit()

                print '>> Asset {0} linked to shot {1}'.format(model_index.data(QtCore.Qt.UserRole + 2), shot.name)
            else:
                print '>> Asset {0} already linked to shot {1}'.format(model_index.data(QtCore.Qt.UserRole + 2), shot.name)

    def unlink_assets(self, list_assets, shot):

        for asset in list_assets:
            self.eve_data.unlink_asset(asset.id, shot.id)
            print '>> Asset {0} unlinked from shot {1}'.format(asset.name, shot.name)

    # MAIN FUNCTIONS
    def launch_houdini(self, script=None, id=None):

        HOUDINI = settings.HOUDINI.format(self.project_properties_ui.project_ui.linHoudini.text())

        # Run Maya
        houdini_launcher.run_houdini(self.eve_root,
                                     settings.PROJECTS,
                                     HOUDINI,
                                     self.selected_project.name,
                                     script=script,
                                     id=id)

    def create_folder(self, path):
        """
        Create folder at input path
        :param path: Path to create folder (C:/TEMP)
        """

        if not os.path.exists(path):
            os.makedirs(path)

    def create_folders(self, root, folders_template):
        """
        Recursively build folder structure based on template
        :param root: Root directory to create folder structure
        :param folders_template: List of lists, folder structure template
        :return:
        """

        if folders_template:
            for folder in folders_template:
                folder_name = folder[0]
                path = '{}/{}'.format(root, folder_name)
                self.create_folder(path)
                self.create_folders(path, folder[1])

    def create_project(self, project_name):
        """
        Create project structure with necessary data on HDD
        :param project_name: string, Project code
        :return:
        """

        # Build project root folder string
        project_root = build_project_root(project_name)
        # Get project data from projects DB
        project = self.eve_data.get_project_by_name(project_name)

        # Create folder structure on HDD
        folders = build_folder_structure()  # assets=project.assets, shots=project.shots
        self.create_folders(project_root, folders)

        # Open project folder
        subprocess.Popen('explorer "{}"'.format(project_root.replace('/', '\\')))

    def run_create_project(self):
        """
        Read UI data and run project creation procedure
        """

        # Read UI data
        project_name = self.selected_project.name

        # Determine project action: create new or update existing
        if self.project_properties_ui.btnCreateProject.text() == self.btn_project_update:
            self.update_project()
        else:
            print '>> Creating project...'
            # Create project
            self.create_project(project_name)
            print '>> Project creation complete!'

    def run_add_asset(self):
        """
        Run create asset window
        """

        # Check if project selected in UI
        if not self.listProjects.selectedIndexes():
            print 'Select Project to create assets!'

        else:
            self.AA.project = self.selected_project
            self.AA.asset_types = self.eve_data.asset_types
            self.AA.exec_()

    def run_add_sequence(self):

        # Check if project selected in UI
        if not self.listProjects.selectedIndexes():
            print 'Select Project to create sequence!'

        else:
            self.AE.project = self.selected_project
            self.AE.exec_()

    def run_add_shot(self):

        # Check if project selected in UI
        if not self.listSequences.selectedIndexes():
            print 'Select Sequence to create shot!'

        else:
            self.AS.project = self.selected_project
            self.AS.sequence = self.selected_sequence
            self.AS.exec_()

    def run_link_assets(self):

        self.LA.shot = self.selected_shot
        self.LA.project_assets = self.eve_data.project_assets
        self.LA.show()

    def run_unlink_assets(self):

        # Get selected assets from UI
        model_indexes = self.shot_properties_ui.shot_ui.listAssets.selectedIndexes()

        list_assets = []
        for model_index in model_indexes:
            list_assets.append(self.eve_data.get_asset(model_index.data(QtCore.Qt.UserRole + 1)))

        # Break links
        self.unlink_assets(list_assets, self.selected_shot)

    def create_asset_file(self):

        script = '{0}/tools/houdini/create_asset.py'.format(self.eve_root)
        self.launch_houdini(script, self.selected_asset.id)

# Run Project Manager
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    PM = ProjectManager()
    PM.show()
    app.exec_()
