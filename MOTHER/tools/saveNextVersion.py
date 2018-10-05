# 256 Pipeline Tools
# Save Next Version. Incremental save current houdini scene (<fileCode>_001.hip >> <fileCode>_002.hip).
# If a file with next version exists, warning window rise with options:
# - Overwrite  a file with next version
# - Save file with the latest available version

import hou
import os

from MOTHER.dna import dna
from MOTHER.ui.widgets import SaveNextVersion

def saveNextVersion():
    # Get current name
    filePath = hou.hipFile.path()

    # Get next version
    newPath = dna.buildPathNextVersion(filePath)

    # Check if next version exists
    if not os.path.exists(newPath):
        hou.hipFile.save(newPath)
        print '>> File saved with a next version!'
    else:
        win = SaveNextVersion.SNV(newPath)
        win.show()

def run():
    saveNextVersion()