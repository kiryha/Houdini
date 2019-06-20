# 256 Pipeline Tools
# Save Next Version. Incremental save current houdini scene (<fileCode>_001.hip >> <fileCode>_002.hip).
# If a file with next version exists, script finds the latest existing version and rise warning window with options:
# - Save file with the latest available version
# - Overwrite a file with latest existing version


import hou
import os

import dna
reload(dna)

def saveNextVersion():
    '''
    Save Next version of current Houdini HIP file
    :return:
    '''

    # Get current name
    pathScene =  dna.buildPathNextVersionFile(hou.hipFile.path())

    # Check if file exist, decide what version to save.
    dna.versionSolverState = None
    state = dna.versionSolver(pathScene)

    if state == 'SNV':
        # If exists and user choose save next version
        pathScene = dna.buildPathNextVersionFile(dna.buildPathLatestVersionFile(pathScene))
    elif state == 'OVR':
        # If exists and user choose overwrite latest existing version
        pathScene = dna.buildPathLatestVersionFile(pathScene)
    else:
        if state:
            # File does not exists, save it as is.
            pathScene = state
            # Create FOLDER for HIP
            dna.createFolder(pathScene)
        else:
            # User cancel action
            print '>> Canceled!'
            return

    hou.hipFile.save(pathScene)

def run():
    saveNextVersion()