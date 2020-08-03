"""
Create file path strings for any file in Eve
Asset path example: 'Z:/projects/Avatar/3D/scenes/ASSETS/NYC/AST_NYC_001.hip'



File Naming convention for filePath:
<file_path> = <file_location>/<file_name>
<file_name> = <file_code>_<file_version>.<file_extension>
<file_code_version> = <file_code>_<file_version>
<file_code> = <file_prefix>_<file_base>

Version definition:
    - VERSION: current
    - NEXT: current + 1
    - LAST: maximum number of existing versions on HDD
    - LATEST: last + 1


Eve can generate/analyze 3 types of path:
    - FILE PATH:      S:/location/code_name_001.mb
                      S:/location/001/code_name_001.mb

    - FILE SEQUENCE:   S:/location/001/code_name_001.001.mb

    - FILE LOCATION:  S:/location/001

"""


import os
import glob
import settings
from PySide2 import QtWidgets, QtCore


class SNV(QtWidgets.QDialog):
    def __init__(self, file_name, parent=None):
        super(SNV, self).__init__(parent=parent)
        # Keep window on top of Maya UI
        self.parent = parent
        self.setParent(self.parent, QtCore.Qt.WindowStaysOnTopHint)

        # Create widgets
        self.resize(400, 50)
        self.setWindowTitle('Warning! File version exists:')
        self.lab = QtWidgets.QLabel(file_name)
        self.lab.setAlignment(QtCore.Qt.AlignHCenter)
        self.btnOVR = QtWidgets.QPushButton("Overwrite")
        self.btnSNV = QtWidgets.QPushButton(" Save Next Version ")
        self.btnCancel = QtWidgets.QPushButton("Cancel")
        # Create layout and add widgets
        layout_main = QtWidgets.QVBoxLayout()
        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addWidget(self.btnOVR)
        layout_buttons.addWidget(self.btnSNV)
        layout_buttons.addWidget(self.btnCancel)
        layout_main.addWidget(self.lab)
        layout_main.addLayout(layout_buttons)
        # Set dialog layout
        self.setLayout(layout_main)
        # Add button signal to greetings slot
        self.btnOVR.clicked.connect(self.OVR)
        self.btnSNV.clicked.connect(self.SNV)
        self.btnCancel.clicked.connect(self.close)

    def OVR(self):
        self.done(2)

    def SNV(self):
        self.done(3)


class EveFilePath:
    path_types = {
        'location':
            {'id': 1,
             'name': 'location',
             'description': 'S:/location/001'},
        'path':
            {'id': 2,
             'name': 'path',
             'description': 'S:/location/001/code_name_001.mb'},
        'sequence':
            {'id': 3,
             'name': 'sequence',
             'description': ' S:/location/001/code_name_001.001.mb'}}

    def __init__(self, file_path=None):

        # Environment set
        self.project_root = os.environ['EVE_PROJECT']  # Z:/projects/Avatar
        # DEFINE STRINGS
        self.file_name_template = '{0}_{1}_{2}.{3}'
        self.file_name_sequence_template = '{0}_{1}_{2}.{3}.{4}'
        self.sequence_token = '%03d'
        self.asset_root = '{0}/PROD/3D/scenes/ASSETS'.format(self.project_root)
        self.shot_root = '{0}/PROD/3D/scenes/SHOTS'.format(self.project_root)
        self.render_3d_root = '{0}/PROD/3D/images'.format(self.project_root)
        self.render_2d_root = '{0}/PROD/2D/RENDER'.format(self.project_root)
        self.comp_root = '{0}/PROD/2D/COMP'.format(self.project_root)

        # EVE FILE PATH OBJECT ATTRIBUTES
        self.type = None  # String path type ('path', 'sequence' or 'location')
        self.path = None
        self.name = None
        self.location = None
        self.prefix = None
        self.file_version = None
        self.folder_version = None
        self.code = None
        self.base = None
        self.extension = None

        # Disassemble file path if provided with initialization
        if file_path:
            self.set_path(file_path)

    # Parsing string file paths
    def set_path(self, file_path):

        self.path = file_path
        self.analyze_file_path()

    def print_file_path(self):

        print 'EveFilePath.type = ', self.type
        print 'EveFilePath.path = ', self.path
        print 'EveFilePath.name = ', self.name
        print 'EveFilePath.location = ', self.location
        print 'EveFilePath.prefix = ', self.prefix
        print 'EveFilePath.file_version = ', self.file_version
        print 'EveFilePath.folder_version = ', self.folder_version
        print 'EveFilePath.code = ', self.code
        print 'EveFilePath.base = ', self.base
        print 'EveFilePath.extension = ', self.extension

    def detect_path_type(self):
        """
        Detect if path type is:
            PATH =      S:/location/code_name_001.mb
            SEQUENCE =  S:/location/code_name_001.001.mb
            LOCATION =  S:/location/

        :return:
        """

        part_length = len(self.path.split('/')[-1].split('.'))  # ['code_name_001', '001', 'mb']

        if part_length == 1:
            self.type = 'location'
        elif part_length == 2:
            self.type = 'path'
        elif part_length == 3:
            self.type = 'sequence'
        else:
            print '>> ERROR! Can`t detect the file type of the path = {}'.format(self.path)

    def rebuild_path(self):
        '''
        Record new PATH after modifications
        '''

        if self.type == 'path':
            if self.folder_version:
                # Replace FOLDER VERSION in location with a new version
                location = self.location
                self.location = '{0}{1}'.format(location[:-3], self.folder_version)

            self.path = '{0}/{1}_{2}.{3}'.format(self.location, self.code, self.file_version, self.extension)

        if self.type == 'sequence':
            self.path = '{0}/{1}_{2}.{3}.{4}'.format(self.location, self.code, self.file_version, self.sequence_token, self.extension)

        if self.type == 'location':
            self.path = '{0}/{1}'.format(self.location, self.folder_version)

    def build_file_base(self, parts):
        ''' Calculate <file_base> part of the file name '''

        file_base = ''

        for i in range(len(parts) - 2):
            if i == 0:
                file_base += '{}'.format(parts[i + 1])
            else:
                file_base += '_{}'.format(parts[i + 1])

        return file_base

    def analyze_file_name(self):
        '''
        Disassemble <file_name> string
        Example naming conventions:
            <file_name> = AST_navigator_001.mb

        '''

        file_name = self.name

        file_extension = file_name.split('.')[-1]
        file_code_version = file_name.split('.')[0]
        parts = file_code_version.split('_')

        file_prefix = parts[0]
        file_version = parts[-1]
        file_base = self.build_file_base(parts)
        file_code = '{0}_{1}'.format(file_prefix, file_base)

        self.prefix = file_prefix
        self.file_version = file_version
        self.code = file_code
        self.base = file_base
        self.extension = file_extension

        # self.print_file_path()

    def analyze_file_path(self):
        '''
        Disassemble string file path into components

        '''

        file_path = self.path

        # Detect TYPE
        if not self.type:
            self.detect_path_type()

        if self.type == 'path' or self.type == 'sequence':
            file_name = file_path.split('/')[-1]
            file_location = file_path.replace('/{}'.format(file_name), '')

            # Check if file path has a FOLDER VERSION
            folder_version = None
            folder_name = file_location.split('/')[-1]
            if len(folder_name) == 3:
                try:
                    int(folder_name)
                    folder_version = folder_name
                except:
                    pass

            self.name = file_name
            self.location = file_location
            self.folder_version = folder_version

            self.analyze_file_name()

        elif self.type == 'location':
            self.location = self.path[:-4]
            self.folder_version = self.path.split('/')[-1]

        else:
            print '>>>> ERROR! Unknown path type for path = {}'.format(self.path)

    def build_next_file_version(self):
        '''
        Create next version of provided file (current + 1)

        '''

        self.file_version = '{0:03d}'.format(int(self.file_version) + 1)
        if self.folder_version:
            self.folder_version = self.file_version

        self.rebuild_path()
        self.analyze_file_path()

    def calculate_last_version(self):
        '''
        Get latest existing file version on HDD
        :return: integer, maximum existing version
        '''

        # # Get list of existing versions of file
        # list_existed = glob.glob('{0}{1}_*.{2}'.format(self.location, self.code, self.extension))
        #
        # list_versions = []
        # for file_path in list_existed:
        #     at_file = EveFilePath(file_path)
        #     list_versions.append(int(at_file.file_version))
        # last_version = max(list_versions)
        #
        # return last_version

        list_versions = []
        if self.type == 'path':
            # Get list of existing versions of FILES
            list_existed = glob.glob('{0}/{1}_*.{2}'.format(self.location, self.code, self.extension))
            list_existed = [name.replace('\\', '/') for name in list_existed]

            for file_path in list_existed:
                at_file = EveFilePath(file_path)
                list_versions.append(int(at_file.file_version))

        if self.type == 'location':
            # Get list of existing versions of FOLDERS
            list_existed = glob.glob('{0}/*'.format(self.location))
            # Filter non-version folder (by length) and fix slashes
            list_existed = [name.replace('\\', '/') for name in list_existed if len(name.split('\\')[-1]) == 3]

            for file_path in list_existed:
                at_file = EveFilePath(file_path)
                list_versions.append(int(at_file.folder_version))

        last_version = max(list_versions)

        if last_version:
            return last_version
        else:
            print '>> ERROR! Calculating last version fails.'

    def build_latest_file_version(self):
        '''
        Create LATEST version of provided file (last existed + 1)
        '''

        latest_version = self.calculate_last_version() + 1
        self.file_version = '{0:03d}'.format(latest_version)
        if self.folder_version:
            self.folder_version = self.file_version

        self.rebuild_path()
        self.analyze_file_path()

    def build_last_file_version(self):
        """
        Create LAST (existing on HDD) version of provided file.
        :return:
        """

        latest_version = self.calculate_last_version()
        self.file_version = '{0:03d}'.format(latest_version)
        if self.folder_version:
            self.folder_version = self.file_version

        self.rebuild_path()
        self.analyze_file_path()

    # Build string paths for database.EveFile.file_types
    def build_path_asset_hip(self, file_type, asset_type, asset_name, version):
        """
        Build asset file path:
            <asset_root>/<asset_name>/<file_type_code>_<asset_name>_<version>.mb

        :param file_type: dictionary, entities.EveFile.file_types['asset_hip']
        :param asset_type: string 'character', 'prop', etc
        :param asset_name:
        :param version:
        :return:
        """

        file_prefix = file_type['prefix']
        asset_folder = '{0}s'.format(asset_type)
        file_name = self.file_name_template.format(file_prefix, asset_name, version, settings.HIP)
        file_path = '{0}/{1}/{2}/{3}'.format(self.asset_root, asset_folder, asset_name, file_name)
        self.type = 'path'

        # print 'build_path_asset_hip [file_path] = ', file_path

        self.set_path(file_path)

    def build_path_shot_render(self, file_type, sequence_name, shot_name, version):

        # E:/256/PROJECTS/VEX/PROD/3D/scenes/SHOTS/RENDER/homework/L02/homework_L02_001.hipnc

        file_prefix = file_type['prefix']
        file_name = self.file_name_template.format(file_prefix, shot_name, version, settings.HIP)
        file_path = '{0}/RENDER/{1}/{2}/{3}'.format(self.shot_root, sequence_name, shot_name, file_name)
        self.type = 'path'

        print 'build_shot_render [file_path] = ', file_path

        self.set_path(file_path)

    # File version solver
    def version_control(self):
        """
        Check if provided FILE (FOLDER) path exists.
            If not - return the same path.
            If exists - ask user save next version or overwrite. Return new path based on user decision
        """

        if not os.path.exists(self.path):
            print '>> File saved to a new version: {}'.format(self.name)
            return self.path
        else:
            self.build_last_file_version()

            # Ask user which version to save
            if self.type == 'path' or self.type == 'sequence':
                file_name = self.name
            else:
                file_name = self.path

            answer = SNV(file_name).exec_()

            if not answer:
                return

            if answer == 2:  # Overwrite
                print '>> File overwritten: {}'.format(self.name)
            if answer == 3:  # Save latest version
                self.build_latest_file_version()
                print '>> File saved to a new version: {}'.format(self.name)

            return self.path
