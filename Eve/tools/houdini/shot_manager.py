import hou
import os
from PySide2 import QtCore, QtWidgets
from ui import ui_shot_manager

from core import settings
from core.database import entities
from core.database import eve_data
from core import models
from core import file_path


reload(file_path)


class ShotManager(QtWidgets.QDialog, ui_shot_manager.Ui_ShotManager):
    def __init__(self):
        super(ShotManager, self).__init__()
        self.setupUi(self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Setup environment
        self.eve_root = os.environ['EVE_ROOT']
        self.project_name = os.environ['EVE_PROJECT_NAME']
        self.SQL_FILE_PATH = settings.SQL_FILE_PATH.format(self.eve_root)

        # Get Project Manager data
        self.eve_data = None
        self.project = None
        self.model_sequences = None
        self.model_shots = None
        # UI selection
        self.selected_shot = None
        self.selected_sequence = None

        self.init_shot_manager()

        # Sequence-shot UI relation
        self.boxSequence.currentIndexChanged.connect(self.init_shots)
        self.boxShot.currentIndexChanged.connect(self.init_shot)

        # Setup UI functionality
        self.btnCreateRenderScene.clicked.connect(self.run_create_render_scene)
        self.btnOpenRenderScene.clicked.connect(self.run_open_render_scene)

    def init_shot_manager(self):
        """
        Load data for Shot Manager
        :return:
        """

        self.eve_data = eve_data.EveData(self.SQL_FILE_PATH)
        self.project = self.eve_data.get_project_by_name(self.project_name)

        self.eve_data.get_project_sequences(self.project)
        self.model_sequences = models.ListModel(self.eve_data.project_sequences)

        self.boxSequence.setModel(self.model_sequences)

        self.init_shots()

    def init_shots(self):
        """
        When sequence selected in Shot Manager Ui
        :return:
        """

        model_index = self.boxSequence.model().index(self.boxSequence.currentIndex(), 0)
        sequence_id = model_index.data(QtCore.Qt.UserRole + 1)

        self.eve_data.get_sequence_shots(sequence_id)
        self.model_shots = models.ListModel(self.eve_data.sequence_shots)

        self.selected_sequence = self.eve_data.get_sequence(sequence_id)

        self.boxShot.setModel(self.model_shots)

        self.init_shot()

    def init_shot(self):

        model_index = self.boxShot.model().index(self.boxShot.currentIndex(), 0)
        shot_id = model_index.data(QtCore.Qt.UserRole + 1)
        shot = self.eve_data.get_shot(shot_id)

        if shot:
            self.selected_shot = self.eve_data.get_shot(shot.id)

    def run_create_render_scene(self):

        # Build string PATH to file
        file_type = entities.EveFile.file_types['shot_render']
        shot_file_path = file_path.EveFilePath()
        shot_file_path.build_path_shot_render(file_type, self.selected_sequence.name, self.selected_shot.name, '001')

        scene_path = shot_file_path.version_control()
        if not scene_path:
            return

        # Create new scene
        hou.hipFile.clear()

        # Save file
        if scene_path:
            hou.hipFile.save(scene_path)

    def run_open_render_scene(self):
        """
        Open LAST existing scene version.

        WIP. Need to implement publishing and open user-defined or last published version.
        :return:
        """

        # Build string PATH to file
        file_type = entities.EveFile.file_types['shot_render']
        shot_file_path = file_path.EveFilePath()
        shot_file_path.build_path_shot_render(file_type, self.selected_sequence.name, self.selected_shot.name, '001')
        shot_file_path.build_last_file_version()

        hou.hipFile.load(shot_file_path.path)


def run_shot_manager():
    shot_manager = ShotManager()
    shot_manager.show()

