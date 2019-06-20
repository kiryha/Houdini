# Create flipbook
# Check if 001 version exists. If so, get latest existing version and
# ask user to overwrite latest version or create new

import hou

import dna
reload(dna)

# Get current flipbook settings
desktop = hou.ui.curDesktop()
scene = desktop.paneTabOfType(hou.paneTabType.SceneViewer)
settings = scene.flipbookSettings().stash()

def runFB(flipbookPath):
    '''
    Run flipbook rendering
    '''

    # Setup flipbook settings
    settings.resolution(dna.resolution_LR)
    settings.frameRange((dna.frameStart, hou.playbar.frameRange()[1]))
    settings.output(flipbookPath)
    # Generate the flipbook using the modified settings
    scene.flipbook(scene.curViewport(), settings)
    # Report
    print '>> Saved FlipBook: {}'.format(flipbookPath)

def createFlipbook():
    '''
    Create hardware viewport render
    :return:
    '''

    # Build 001 version of flipbook file path
    flipbookPath = dna.buildFilePath('001', dna.fileTypes['flipbookSequence'], scenePath=hou.hipFile.path())

    dna.versionSolverState = None
    state = dna.versionSolver(flipbookPath, dna.fileTypes['flipbookSequence'])

    if state == 'SNV':
        # If exists and user choose save next version
        flipbookPath = dna.buildPathNextVersionFolder(dna.buildPathLatestVersionFolder(flipbookPath))
        dna.createFolder(flipbookPath)
    elif state == 'OVR':
        # If exists and user choose overwrite latest existing version
        flipbookPath = dna.buildPathLatestVersionFolder(flipbookPath)
    else:
        if state:
            # File does not exists, save it as is.
            flipbookPath = state
            # Create FOLDER for HIP
            dna.createFolder(flipbookPath)
        else:
            # User cancel action
            print '>> Canceled!'
            return

    runFB(flipbookPath)

def run():
    createFlipbook()