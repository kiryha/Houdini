# 256 Pipeline tools
# Save character materials assignment information to a database
# Part A: dump materials. Select character material SOP (assign materials via group) and run script

import hou
import json

from MOTHER.dna import dna
reload(dna)

materialPath = '/obj/MATERIALS/GENERAL/'
characterName = 'ROMA'
section = 'materials'
materialsData = {}

materialNode = hou.selectedNodes()


def checkConditions():
    '''
    Check if environment conditions allows to run script without errors
    '''
    if not materialNode:  # If user select anything
        print '>> Nothing selected! Select material SOP!'
        return 0


def getMaterials(materialNode):
    print '>> Building material dictionary:  MATERIAL [ GROUPS ]:'
    materialsNumber = materialNode.parm('num_materials').eval()
    n = 1
    for material in range(materialsNumber):
        group = materialNode.parm('group{}'.format(n)).eval()
        material = materialNode.parm('shop_materialpath{}'.format(n)).eval().replace(materialPath, '')
        materialsData[material] = group
        print '{0} [ {1} ]'.format(material, group)
        n += 1

    return materialsData



def run():
    if checkConditions() != 0:
        materialsData = getMaterials(materialNode[0])
        dna.setCharacterData(characterName, section, materialsData)
        print '>> DONE'


