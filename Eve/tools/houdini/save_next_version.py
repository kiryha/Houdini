'''
Save next version of input file
'''


from core import file_path
import hou

reload(file_path)

def save_next_version():

    scene_path = hou.hipFile.path()

    if scene_path:
        scene_file = file_path.EveFilePath(scene_path)
        scene_file.build_next_file_version()
        scene_path = scene_file.version_control()

        if scene_path:
            hou.hipFile.save(scene_path)
    else:
        print '>> Houdini file is not saved yet. Save scene first!'
