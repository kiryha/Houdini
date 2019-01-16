'''
256 pipeline tools
Database file, contain ASSET and SHOT data. In future this data would be taken from Shotgun
A gene is a region of DNA that encodes function.
'''



SHOTS = [
    {'code': 'SHOT_010', 'sg_cut_out': 125, 'sg_sequence': {'name': '010'}, 'assets': [{'name': 'CLOUDS'}]},
    {'code': 'SHOT_020', 'sg_cut_out': 200, 'sg_sequence': {'name': '010'}, 'assets': [{'name': 'CITY'}, {'name': 'ROMA'}]}
        ]

ASSETS = [
    {'code': 'CITY',
     'sg_asset_type': 'Environment',
     'hda_name': 'city',
     'animation_hda': {'name': 'CITY_ANM', 'hda_name': 'city_anm'},
     'proxy_hda': {'name': 'CITY_PRX', 'hda_name': 'city_prx'},
     'crowds_hda': {'name': 'CROWDS', 'hda_name': 'city_crowds'},
     'light_hda': {'name': 'CITY_LIT', 'hda_name': 'city_lights'}},

    {'code': 'CITY',
     'sg_asset_type': 'Environment'}
        ]
