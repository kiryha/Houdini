# MOTHER
# Houdini pipeline for VFX production

# Wrapper to run Houdini with custom environment
import os, subprocess

# DEFINE COMMON VARIABLES
# Pipeline root folder
rootPipeline = os.path.dirname(__file__).replace('\\','/')
# Project root folder
rootProject = os.path.dirname(os.path.dirname(rootPipeline)).replace('\\','/')
# Houdini JOB root
root3D = '{0}/PROD/3D'.format(rootProject)
# HOUDINI_OTLSCAN_PATH
pathHDA = ''
# Houdini install dir
houdini = 'C:/Program Files/Side Effects Software/Houdini 16.5.536/bin/houdinifx.exe' # 16.5.536 17.0.352


def getHDA():
    '''
    Build HOUDINI_OTLSCAN_PATH env variable value:
    Get all subfolders of HDA location dirs (hda and lib/materials) and combine to one string
    Used by Houdini to search for HDA (Houdini Digital Assets)
    '''

    def combinePaths(listPaths):
        '''
        Combine paths string from list of paths
        :param listPaths: list of subfolders in processed folder
        '''
        global pathHDA
        for folder in listPaths:
            path = folder[0].replace('\\', '/')
            if not 'backup' in path: # Exclude backup folders
                pathHDA += '{};'.format(folder[0].replace('\\', '/'))

    # Get list of sub folders
    listPaths_HDA = os.walk('{0}/hda'.format(root3D)) # HDA
    listPaths_MTL = os.walk('{0}/lib/MATERIALS'.format(root3D))  # LIBRARY

    # Combine paths to a string
    combinePaths(listPaths_HDA)
    combinePaths(listPaths_MTL)

    # Add Houdini standard OTLs
    global pathHDA
    pathHDA = pathHDA + '&'

    return pathHDA

# SETUP PROJECT ENVIRONMENT
# Root of the project
os.environ['ROOT'] = rootProject
# Root of houdini project
os.environ['JOB'] = root3D
# Houdini digital assets folder including sub folders
os.environ['HOUDINI_OTLSCAN_PATH'] = getHDA()
# Houdini path
os.environ['HOUDINI_PATH'] = '{}/EVE/houdini;&'.format(rootPipeline)
# Path to custom python tools
os.environ['PYTHONPATH'] = '{}/EVE/tools;&'.format(rootPipeline)
# Icons
# os.environ['HOUDINI_UI_ICON_PATH'] = '{}/EVE/icons'.format(rootPipeline)
# Houdini current user pref folder in MyDocuments (win)
# os.environ['home'] = '{}/Documents/houdiniUserPrefs'.format(os.path.expanduser("~"))

# Run Houdini
subprocess.Popen(houdini)

# Prevent closing CMD window
# raw_input()