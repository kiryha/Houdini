# MOTHER
# Houdini pipeline for VFX production

# Wrapper to run Houdini with custom environment
import os, subprocess

# DEFINE COMMON VARIABLES
# Pipeline root folder
rootPipeline = ''
# Project root folder
rootProject = os.path.dirname(os.path.dirname(os.path.dirname(__file__))).replace('\\','/')
# Houdini JOB root
root3D = '{0}/PROD/3D'.format(rootProject)
# HOUDINI_OTLSCAN_PATH
pathHDA = ''
# Houdini install dir
build = ''
houdini = 'C:/Program Files/Side Effects Software/Houdini {0}/bin/houdinifx.exe'.format(build)
# HDA skip folders
filterFolders = ['backup']


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
            # Filter unnecessary folders
            if not path.split('/')[-1] in filterFolders:
                pathHDA += '{};'.format(folder[0].replace('\\', '/'))

    # Get list of sub folders
    listPaths_HDA = os.walk('{0}/hda'.format(root3D)) # HDA
    listPaths_MTL = os.walk('{0}/lib/MATERIALS'.format(root3D))  # Material library
    listPaths_LIT = os.walk('{0}/lib/LIGHTS'.format(root3D))  # Light library

    # Combine paths to a string
    combinePaths(listPaths_HDA)
    combinePaths(listPaths_MTL)
    combinePaths(listPaths_LIT)

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
os.environ['HOUDINI_PATH'] = '{}/PREP/PIPELINE/settings;&'.format(rootProject)
# Path to custom python tools
os.environ['PYTHONPATH'] = '{0}/dna;{0}/tools;&'.format(rootPipeline)

# Icons
# os.environ['HOUDINI_UI_ICON_PATH'] = '{}/EVE/icons'.format(rootPipeline)
# Houdini current user pref folder in MyDocuments (win)
# os.environ['home'] = '{}/Documents/houdiniUserPrefs'.format(os.path.expanduser("~"))

# Setup Redshift
# os.environ['HOUDINI_DSO_ERROR'] = '2'
# os.environ['PATH'] += ';' + 'C:/ProgramData/Redshift/bin;$PATH'
# os.environ['HOUDINI_PATH'] += 'C:/ProgramData/Redshift/Plugins/Houdini/17.0.459;&'

# Run Houdini
subprocess.Popen(houdini)

# Prevent closing CMD window
# raw_input()
