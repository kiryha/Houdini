"""
Project Manager entities CRUD: materials, projects, assets, shots
"""


import sqlite3
import entities


class EveData:
    def __init__(self, SQL_FILE_PATH):
        # Load database
        self.SQL_FILE_PATH = SQL_FILE_PATH

        # Data attributes
        # INTERNAL SET
        self.projects = []
        self.project_assets = []
        self.asset_types = []
        self.project_sequences = []
        self.sequence_shots = []
        self.shot_assets = []

        # Initialize data
        self.init_data()

    # UI
    def init_data(self):
        """
        Populate data when create a EveData instance
        """

        self.get_projects()
        self.get_asset_types()

    # CRUD
    # Project
    def add_project(self, project):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        # Add project to DB
        cursor.execute("INSERT INTO projects VALUES ("
                       ":id,"
                       ":name,"
                       ":houdini_build,"
                       ":width,"
                       ":height,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': project.name,
                        'houdini_build': project.houdini_build,
                        'width': project.width,
                        'height': project.height,
                        'description': project.description})

        connection.commit()
        project.id = cursor.lastrowid  # Add database ID to the project object
        connection.close()

        # Add project to data instance
        self.projects.append(project)

    def get_project(self, project_id):
        """ Get project by id """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM projects WHERE id=:id",
                       {'id': project_id})
        project_tuple = cursor.fetchone()
        project_object = entities.Converter.convert_to_project([project_tuple])[0]

        connection.close()

        if project_object:
            return project_object

    def get_project_by_name(self, project_name):
        """ Get project by id """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM projects WHERE name=:name",
                       {'name': project_name})
        project_tuple = cursor.fetchone()
        project_object = entities.Converter.convert_to_project([project_tuple])[0]

        connection.close()

        if project_object:
            return project_object

    def get_projects(self):
        """ Get all project items from projects table in db """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM projects")
        project_tuples = cursor.fetchall()
        project_objects = entities.Converter.convert_to_project(project_tuples)

        connection.close()

        self.projects.extend(project_objects)

    def get_project_assets(self, project):
        """ Get all project assets from assets table in db """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM assets WHERE project=:project",
                       {'project': project.id})

        asset_tuples = cursor.fetchall()
        asset_objects = entities.Converter.convert_to_asset(asset_tuples)

        connection.close()

        # Clear list and append assets
        del self.project_assets[:]
        for asset in asset_objects:
            self.project_assets.append(asset)

    def get_project_sequences(self, project):
        """ Get all project sequences from sequences table in db """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM sequences WHERE project=:project",
                       {'project': project.id})

        sequence_tuples = cursor.fetchall()
        sequence_objects = entities.Converter.convert_to_sequence(sequence_tuples)

        connection.close()

        # Clear list and append assets
        del self.project_sequences[:]
        for sequence in sequence_objects:
            self.project_sequences.append(sequence)

    def get_sequence_shots(self, sequence_id):
        """
        Get all sequence shots from shots table in db
        """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM shots WHERE sequence=:sequence",
                       {'sequence': sequence_id})

        shot_tuples = cursor.fetchall()
        shot_objects = entities.Converter.convert_to_shot(shot_tuples)

        connection.close()

        # Clear list and append assets
        del self.sequence_shots[:]
        for shot in shot_objects:
            self.sequence_shots.append(shot)

    def update_project(self, project):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("UPDATE projects SET "
                       "houdini_build=:houdini_build,"
                       "width=:width,"
                       "height=:height,"
                       "description=:description "

                       "WHERE id=:id",

                       {'id': project.id,
                        'houdini_build': project.houdini_build,
                        'width': project.width,
                        'height': project.height,
                        'description': project.description})

        connection.commit()
        connection.close()

        return project

    def del_project(self, project_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM projects WHERE id=:id",
                       {'id': project_id})

        connection.commit()
        connection.close()

        for project in self.projects:
            if project.id == project_id:
                self.projects.remove(project)

    # Assets
    def add_asset(self, asset, project_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO assets VALUES ("
                       ":id,"
                       ":name,"
                       ":project,"
                       ":type,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': asset.name,
                        'project': project_id,
                        'type': asset.type,
                        'description': asset.description})

        connection.commit()
        asset.id = cursor.lastrowid  # Add database ID to the asset object
        connection.close()

        self.project_assets.append(asset)

    def get_asset(self, asset_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM assets WHERE id=:id",
                       {'id': asset_id})

        asset_tuple = cursor.fetchone()

        connection.close()

        if asset_tuple:
            return entities.Converter.convert_to_asset([asset_tuple])[0]

    def get_asset_by_name(self, project_id, asset_name):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM assets WHERE "
                       "name=:name "
                       "AND project=:project",

                       {'name': asset_name,
                        'project': project_id})

        asset_tuple = cursor.fetchone()

        connection.close()

        if asset_tuple:
            return entities.Converter.convert_to_asset([asset_tuple])[0]

    def get_asset_types(self):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM asset_types")
        asset_types_tuples = cursor.fetchall()
        asset_types_objects = entities.Converter.convert_to_asset_types(asset_types_tuples)

        connection.close()

        self.asset_types.extend(asset_types_objects)

    def get_asset_type_string(self, asset_type_id):
        """
        Get asset type name by asset type id in Asset.asset_types dictionary
        :return:
        """

        for name, data in entities.Asset.asset_types.iteritems():
            if data['id'] == asset_type_id:
                return name

    def update_asset(self, asset):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("UPDATE assets SET "
                       "project=:project,"
                       "type=:type,"
                       "description=:description "

                       "WHERE id=:id",

                       {'id': asset.id,
                        'project': asset.project,
                        'type': asset.type,
                        'description': asset.description})

        connection.commit()
        connection.close()

        return asset

    def del_asset(self, asset_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        # Delete ASSET
        cursor.execute("DELETE FROM assets WHERE id=:id",
                       {'id': asset_id})

        # Delete asset LINK
        cursor.execute("DELETE FROM shot_assets WHERE asset_id=:asset_id",

                       {'asset_id': asset_id})

        connection.commit()
        connection.close()

        for asset in self.project_assets:
            if asset.id == asset_id:
                self.project_assets.remove(asset)

    # Sequence
    def add_sequence(self, sequence, project_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO sequences VALUES ("
                       ":id,"
                       ":name,"
                       ":project,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': sequence.name,
                        'project': project_id,
                        'description': sequence.description})

        connection.commit()
        sequence.id = cursor.lastrowid  # Add database ID to the sequence object
        connection.close()

        self.project_sequences.append(sequence)

    def get_sequence(self, sequence_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM sequences WHERE id=:id",
                       {'id': sequence_id})

        sequence_tuple = cursor.fetchone()

        connection.close()

        if sequence_tuple:
            return entities.Converter.convert_to_sequence([sequence_tuple])[0]

    def update_sequence(self, sequence):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("UPDATE sequences SET "
                       "description=:description "

                       "WHERE id=:id",

                       {'id': sequence.id,
                        'description': sequence.description})

        connection.commit()
        connection.close()

        return sequence

    def del_sequence(self, sequence_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM sequences WHERE id=:id",
                       {'id': sequence_id})

        connection.commit()
        connection.close()

        for sequence in self.project_sequences:
            if sequence.id == sequence_id:
                self.project_sequences.remove(sequence)

    # Shot
    def add_shot(self, shot, sequence_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO shots VALUES ("
                       ":id,"
                       ":name,"
                       ":sequence,"
                       ":start_frame,"
                       ":end_frame,"
                       ":width,"
                       ":height,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': shot.name,
                        'sequence': sequence_id,
                        'start_frame': shot.start_frame,
                        'end_frame': shot.end_frame,
                        'width': shot.width,
                        'height': shot.height,
                        'description': shot.description})

        connection.commit()
        shot.id = cursor.lastrowid  # Add database ID to the shot object
        connection.close()

        self.sequence_shots.append(shot)

    def get_shot(self, shot_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM shots WHERE id=:id",
                       {'id': shot_id})

        shot_tuple = cursor.fetchone()

        connection.close()

        if shot_tuple:
            return entities.Converter.convert_to_shot([shot_tuple])[0]

    def get_shot_assets(self, shot_id):

        # Clear shot_assets list
        del self.shot_assets[:]

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM shot_assets WHERE shot_id=:shot_id",
                       {'shot_id': shot_id})

        link_tuples = cursor.fetchall()

        connection.close()

        if link_tuples:
            # Append assets
            for link_tuple in link_tuples:
                self.shot_assets.append(self.get_asset(link_tuple[2]))

    def update_shot(self, shot):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("UPDATE shots SET "
                       "sequence=:sequence,"
                       "start_frame=:start_frame,"
                       "end_frame=:end_frame,"
                       "width=:width,"
                       "height=:height,"
                       "description=:description "

                       "WHERE id=:id",

                       {'id': shot.id,
                        'sequence': shot.sequence,
                        'start_frame': shot.start_frame,
                        'end_frame': shot.end_frame,
                        'width': shot.width,
                        'height': shot.height,
                        'description': shot.description})

        connection.commit()
        connection.close()

        return shot

    def del_shot(self, shot_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM shots WHERE id=:id",
                       {'id': shot_id})

        connection.commit()
        connection.close()

        for shot in self.sequence_shots:
            if shot.id == shot_id:
                self.sequence_shots.remove(shot)

    def link_asset(self, asset_id, shot_id):
        """
        Link asset to the shot
        """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        # Check if the asset link exists:
        cursor.execute("SELECT * FROM shot_assets WHERE asset_id=:asset_id AND shot_id=:shot_id",

                       {'asset_id': asset_id, 'shot_id': shot_id})

        if cursor.fetchone():
            connection.close()
            return

        cursor.execute("INSERT INTO shot_assets VALUES ("
                       ":id,"
                       ":shot_id,"
                       ":asset_id)",

                       {'id': cursor.lastrowid,
                        'shot_id': shot_id,
                        'asset_id': asset_id})

        connection.commit()
        connection.close()
        return True

    def unlink_asset(self, asset_id, shot_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM shot_assets WHERE asset_id=:asset_id AND shot_id=:shot_id",

                       {'asset_id': asset_id, 'shot_id': shot_id})

        connection.commit()
        connection.close()

        for asset in self.shot_assets:
            if asset.id == asset_id:
                self.shot_assets.remove(asset)