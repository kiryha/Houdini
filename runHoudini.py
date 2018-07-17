# MOTHER
# Houdini pipeline for VFX production

# Wrapper to run Houdini with custom environment
import os, subprocess

# DEFINE VARIABLES
# Pipeline root folder
rootPipeline = os.path.dirname(__file__).replace('\\','/')
# Project root folder
rootProject = os.path.dirname(os.path.dirname(rootPipeline)).replace('\\','/')
# Houdini JOB root
root3D = '{0}/PROD/3D'.format(rootProject)
# Houdini install dir
PC = os.environ['COMPUTERNAME']
houdini = 'C:/Program Files/Side Effects Software/Houdini 16.5.439/bin/houdinifx.exe'
# houdini = 'C:/Program Files/Side Effects Software/Houdini 16.0.504.20/bin/houdinifx.exe'

def getOTL():
    '''
    Build HOUDINI_OTLSCAN_PATH value:
    Get all subfolders of <root3D>/hda folder and combine to one string
    '''

    pathOTL = ''
    listPaths = os.walk('{0}/hda'.format(root3D)) # Get list of sub folders

    for folder in listPaths:
        path = folder[0].replace('\\', '/')
        if not 'backup' in path: # Exclude backup folders
            pathOTL += '{};'.format(folder[0].replace('\\', '/'))

    pathOTL = pathOTL + '&' # Add Houdini standard OTL paths
    return pathOTL

# SETUP PROJECT ENVIRONMENT
# Root of houdini project
os.environ['JOB'] = root3D
# Houdini digital assets folder including sub folders
os.environ['HOUDINI_OTLSCAN_PATH'] = getOTL()
# Houdini path
os.environ['HOUDINI_PATH'] = '{}/MOTHER/houdini;&'.format(rootPipeline)
# Icons
# os.environ['HOUDINI_UI_ICON_PATH'] = '{}/MOTHER/icons'.format(rootPipeline)
# Houdini current user pref folder in MyDocuments (win)
# os.environ['home'] = '{}/Documents/houdiniUserPrefs'.format(os.path.expanduser("~"))



# Run Houdini
subprocess.Popen(houdini)

# Prevent closing CMD window
raw_input()
