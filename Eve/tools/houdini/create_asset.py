import sys
import os

import hou

from core.database import entities
from core.database import asset_data

from core import file_path
from core import settings

# Get data from database based on env variables and arguments
eve_root = os.environ['EVE_ROOT']
asset_id = int(sys.argv[-1])
asset_data = asset_data.AssetData(settings.SQL_FILE_PATH.format(eve_root), asset_id)

# Create EveFilePath
file_type = entities.EveFile.file_types['asset_hip']
file_path_asset = file_path.EveFilePath()
file_path_asset.build_path_asset_hip(file_type, asset_data.asset_type, asset_data.asset.name, '001')
scene_path = file_path_asset.version_control()

# Save file
if scene_path:
    if not os.path.exists(file_path_asset.location):
        os.makedirs(file_path_asset.location)
    hou.hipFile.save(scene_path)
