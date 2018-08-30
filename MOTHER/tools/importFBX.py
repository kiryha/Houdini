'''
Import mixmao FBX animation
from hardcoded path
'''

import hou
import os

dirFBX = 'P:/PROJECTS/NSI/PROD/3D/lib/ANIMATION/CHARACTERS/ROMA/FBX/'
filesNamesFBX = [fileName for fileName in os.listdir(dirFBX) if os.path.isfile(os.path.join(dirFBX, fileName))]

def run():
    for fileName in filesNamesFBX:
        fileFBX =  '{0}{1}'.format(dirFBX,fileName)
        if not hou.node('/obj/{}_fbx'.format(fileName.replace('.fbx',''))):
            fbx = hou.hipFile.importFBX(fileFBX)
            fbx[0].parm('scale').set(0.01) # Set FBX scale
            print '>> IMPORTED: {}'.format(fileName)
        else:
            print '>> EXISTS: {}'.format(fileName) 