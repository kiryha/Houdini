import hou
import os
from PySide2 import QtCore, QtWidgets
from ui import ui_asset_manager

from core import settings
from core.database import entities
from core.database import eve_data
from core.database import asset_data
from core import models
from core import file_path


reload(file_path)


class AssetManager(QtWidgets.QDialog, ui_asset_manager.Ui_AssetManager):
    def __init__(self):
        super(AssetManager, self).__init__()
        self.setupUi(self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Setup environment
        self.eve_root = os.environ['EVE_ROOT']
        self.project_name = os.environ['EVE_PROJECT_NAME']
        self.SQL_FILE_PATH = settings.SQL_FILE_PATH.format(self.eve_root)

        # Get Project Manager data
        self.eve_data = None
        self.project = None
        self.model_assets = None
        # Get asset data
        self.asset_data = None

        self.init_asset_manager()

        # Setup UI functionality
        self.btnAssetCrete.clicked.connect(self.create_asset_scene)
        self.btnAssetOpen.clicked.connect(self.open_asset_scene)

    def init_asset_manager(self):

        # Get Eve data
        self.eve_data = eve_data.EveData(self.SQL_FILE_PATH)
        self.project = self.eve_data.get_project_by_name(self.project_name)

        # Fill Asset Types
        model_asset_types = models.ListModel(self.eve_data.asset_types)
        self.comAssetType.setModel(model_asset_types)

        # Fill Asset list in UI
        self.eve_data.get_project_assets(self.project)
        self.model_assets = models.ListModel(self.eve_data.project_assets)
        self.comAssetName.setModel(self.model_assets)

    def get_asset_data(self):
        # Get Asset Object
        index = self.comAssetName.model().index(self.comAssetName.currentIndex(), 0)
        asset_id = index.data(QtCore.Qt.UserRole + 1)
        self.asset_data = asset_data.AssetData(self.SQL_FILE_PATH, asset_id)

    def create_asset_scene(self):

        # Get Asset Object
        self.get_asset_data()

        # Create file path string
        asset_file_path = file_path.EveFilePath()
        file_type = entities.EveFile.file_types['asset_hip']
        asset_file_path.build_path_asset_hip(file_type, self.asset_data.asset_type, self.asset_data.asset.name, '001')
        scene_path = asset_file_path.version_control()

        # Save file
        if scene_path:
            if not os.path.exists(asset_file_path.location):
                os.makedirs(asset_file_path.location)
            hou.hipFile.save(scene_path)

    def open_asset_scene(self):

        # Get Asset Object
        self.get_asset_data()

        asset_file_path = file_path.EveFilePath()
        file_type = entities.EveFile.file_types['asset_hip']
        asset_file_path.build_path_asset_hip(file_type, self.asset_data.asset_type, self.asset_data.asset.name, '001')
        asset_file_path.build_last_file_version()

        hou.hipFile.load(asset_file_path.path)


def run_asset_manager():
    asset_manager = AssetManager()
    asset_manager.show()

