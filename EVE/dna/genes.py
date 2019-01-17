'''
256 pipeline tools
Database file, contain ASSET and SHOT data. In future this data would be taken from Shotgun
A gene is a region of DNA that encodes function.
'''


# TEMP DATA !!!
# UNCOMMENT 1 SHOT and CHANGE SHOT_010 >> SHOT_020 in 2 shot!!!!
SHOTS = [
    #{'code': 'SHOT_010', 'sg_cut_out': 125, 'sg_sequence': {'name': '010'}, 'assets': [{'name': 'CLOUDS'}]},
    {'code': 'SHOT_010', 'sg_cut_out': 200, 'sg_sequence': {'name': '010'}, 'assets': [{'name': 'CITY'}, {'name': 'ROMA'}]}
        ]

ASSETS = [
    {'code': 'CITY',
     'sg_asset_type': 'Environment',
     'hda_name': 'city',
     'animation_hda': {'name': 'CITY_ANM', 'hda_name': 'city_anm'},
     'proxy_hda': {'name': 'CITY_PRX', 'hda_name': 'city_prx'},
     'crowds_hda': {'name': 'CROWDS', 'hda_name': 'city_crowds'},
     'light_hda': {'name': 'CITY_LIT', 'hda_name': 'city_lights'}},

    {'code': 'ROMA',
     'sg_asset_type': 'Character'}
        ]

"""
def getStotData(episodeNumber, shotNumber):
    '''
    Get shot dictionary by eppisode and shot numbers (010 > 010)

    :param episodeNumber: string '010'
    :param shotNumber: string '010'
    :return shot: shot dictionary
    {'code': 'SHOT_010', 'sg_cut_out': 200, 'sg_sequence': {'name': '010'}, 'assets': [{'name': 'CITY'}, {'name': 'ROMA'}]}
    '''

    shotCode = 'SHOT_{0}'.format(shotNumber)

    for shot in SHOTS:
        # Find shot of requested sequence
        if shot['sg_sequence']['name'] == episodeNumber:
            # Find shot
            if shot['code'] == shotCode:
                return shot

def getSortedData(assetsData, sortType):

    # assetsData = list of assets dictionaries linked to shot
    # sortType = 'Environment', 'Character', 'Prop'

    if sortType == 'Environment':
        for assetData in assetsData:
            if assetData['sg_asset_type'] == sortType:
                return assetData

    if sortType == 'Character':
        listCharacters = []
        for assetData in assetsData:
            if assetData['sg_asset_type'] == sortType:
                listCharacters.append(assetData)
        return listCharacters

def getAssetsData(assetData_short):

    # assetsData = [{'name': 'CITY'}, {'name': 'ROMA'}]

    assetsData_full = []

    for asset in assetData_short:
        for assetData_full in ASSETS:
            if assetData_full['code'] == asset['name']:
                assetsData_full.append(assetData_full)

    return assetsData_full

shotData = getStotData('010', '020')
# print shotData
assetsData = getAssetsData(shotData['assets'])
envData = getSortedData(assetsData,  'Environment')
charData = getSortedData(assetsData,  'Character')

print charData
"""