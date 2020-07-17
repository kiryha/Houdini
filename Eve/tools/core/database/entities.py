"""
Database entities classes for all tables
"""


class Project:
    def __init__(self, project_name):
        self.id = None
        self.name = project_name
        self.houdini_build = ''
        self.width = ''
        self.height = ''
        self.description = ''


class Asset:
    asset_types = {
        'character':
            {'id': 1,
             'name': 'character',
             'description': 'Character asset'},

        'environment':
            {'id': 2,
             'name': 'environment',
             'description': 'Environment asset'},

        'prop':
            {'id': 3,
             'name': 'prop',
             'description': 'Animated asset with rig'},

        'static':
            {'id': 4,
             'name': 'static',
             'description': 'Non animated asset'},

        'fx':
            {'id': 5,
             'name': 'fx',
             'description': 'FX asset'}}

    def __init__(self, asset_name, project_id):
        self.id = None
        self.name = asset_name
        self.project = project_id
        self.type = None
        self.description = ''

    def get_type(self):

        # Detect asset type, return type string ('character')
        for asset_type in Asset.asset_types:
            if Asset.asset_types[asset_type]['id'] == self.type:
                return Asset.asset_types[asset_type]['name']


class Sequence:
    def __init__(self, sequence_name, project_id):
        self.id = None
        self.name = sequence_name
        self.project = project_id
        self.description = ''


class Shot:
    def __init__(self, shot_name, sequence_id):
        self.id = None
        self.name = shot_name
        self.sequence = sequence_id
        self.start_frame = ''
        self.end_frame = ''
        self.width = ''
        self.height = ''
        self.description = ''


class AssetType:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class EveFile:
    file_types = {
        'asset_hip':
            {'id': 1,
             'name': 'asset_hip',
             'prefix': 'ast',
             'description': 'Houdini working scene for assets'},

        'asset_hda':
            {'id': 2,
             'name': 'asset_hda',
             'prefix': 'hda',
             'description': 'Houdini digital asset for assets'},

        'asset_fx':
            {'id': 3,
             'name': 'asset_hip',
             'prefix': 'fxa',
             'description': ''},

        'shot_animation':
            {'id': 4,
             'name': 'asset_hip',
             'prefix': 'anm',
             'description': ''},

        'shot_render':
            {'id': 5,
             'name': 'asset_hip',
             'prefix': 'rnd',
             'description': ''},

        'shot_fx':
            {'id': 6,
             'name': 'asset_hip',
             'prefix': 'fxs',
             'description': 'Houdini working scene for assets.'}}

    def __init__(self, file_type_id, source_id):
        self.id = None
        self.type = file_type_id
        self.source = source_id  # Source DB item id (asset, shot etc)
        self.snapshot = None
        self.description = ''


class Variation:
    """  WIP  """
    variation_types = {
        'material': {},
        'geometry': {},
        'light': {},
        'fx': {}}

    def __init__(self, variation_type_id):
        self.id = None
        self.type = variation_type_id
        self.value = None
        self.description = ''


class Converter:
    """
    Convert data from DB to Athena objects
    """

    @staticmethod
    def convert_to_project(project_tuples):
        """
        Convert list of projects tuples to list of Eve Project objects

        :param project_tuples: list of tuples, project data: [(id, name, houdini_build, width, height, description)]
        :return:
        """

        projects = []
        for project_tuple in project_tuples:
            project = Project(project_tuple[1])
            project.id = project_tuple[0]
            project.houdini_build = project_tuple[2]
            project.width = project_tuple[3]
            project.height = project_tuple[4]
            project.description = project_tuple[5]
            projects.append(project)

        return projects

    @staticmethod
    def convert_to_asset(asset_tuples):
        """
        Convert list of assets tuples to list of athena Asset objects
        :param asset_tuples:  [(id, name, project, type, description)]
        :return:
        """

        assets = []

        for asset_tuple in asset_tuples:
            asset = Asset(asset_tuple[1], asset_tuple[2])
            asset.id = asset_tuple[0]
            asset.type = asset_tuple[3]
            asset.description = asset_tuple[4]
            assets.append(asset)

        return assets

    @staticmethod
    def convert_to_sequence(sequence_tuples):
        """
        Convert list of sequence tuples to list of athena Sequence objects
        :param sequence_tuples:  [(id, name, project, description)]
        :return:
        """

        sequences = []

        for sequence_tuple in sequence_tuples:
            sequence = Sequence(sequence_tuple[1], sequence_tuple[2])
            sequence.id = sequence_tuple[0]
            sequence.description = sequence_tuple[3]
            sequences.append(sequence)

        return sequences

    @staticmethod
    def convert_to_shot(shot_tuples):
        """
        Convert list of shot tuples to list of athena Shot objects
        :param shot_tuples:  [(id, name, sequence, start_frame, end_frame, width, height, description)]
        :return:
        """

        shots = []

        for shot_tuple in shot_tuples:
            shot = Shot(shot_tuple[1], shot_tuple[2])
            shot.id = shot_tuple[0]
            shot.start_frame = shot_tuple[3]
            shot.end_frame = shot_tuple[4]
            shot.width = shot_tuple[5]
            shot.height = shot_tuple[6]
            shot.description = shot_tuple[7]
            shots.append(shot)

        return shots

    @staticmethod
    def convert_to_asset_types(asset_types_tuples):
        """
        Convert list of asset types tuples to list of Eve AssetType objects
        :param asset_types_tuples: list of tuples, asset type data: [(id, name, description)]
        :return:
        """

        asset_types = []
        for asset_types_tuple in asset_types_tuples:
            asset_type = AssetType(asset_types_tuple[0], asset_types_tuple[1], asset_types_tuple[2])
            asset_types.append(asset_type)

        return asset_types
