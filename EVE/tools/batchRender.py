'''
Utility for rendering sequence of hip files (aka Deadline Render)
'''
import os
import sys

#os.environ['PATH'] = 'C:/PROGRA~1/SIDEEF~1/HOUDIN~1.459/bin;&'
#import hou

import subprocess
cmdTools = '"C:/Program Files/Side Effects Software/Houdini 17.0.459/bin/hcmd.exe"'
#batch = 'hscript P:\PROJECTS\NSI\PROD\3D\scenes\RENDER\render.cmd'
#batch = 'mread P:/PROJECTS/NSI/PROD/3D/scenes/RENDER/000/SHOT_010/RND_E000_S010_001.hiplc"'
batch = 'hscript P:/PROJECTS/NSI/PROD/3D/scenes/RENDER/render.cmd'
# sys.path.append(cmdTools)
# cmd = '{0} {1}'.format(cmdTools, batch)
#os.system(cmd)

# subprocess.Popen(cmdTools).communicate()
# os.environ['PATH'] = 'C:/Program Files/Side Effects Software/Houdini 17.0.459/bin/hcmd.exe;&'
# ubprocess.call(["C:/Program Files/Side Effects Software/Houdini 17.0.459/bin/hcmd.exe", "hscript", "P:\PROJECTS\NSI\PREP\PIPELINE\EVE\genes\render.cmd"], shell=True)
subprocess.call(["C:/Program Files/Side Effects Software/Houdini 17.0.459/bin/hcmd.exe", "P:/PROJECTS/NSI/PREP/PIPELINE/EVE/genes/render.cmd"], shell=True)
#subprocess.call(["hscript", "P:\PROJECTS\NSI\PREP\PIPELINE\EVE\genes\render.cmd"], shell=True)