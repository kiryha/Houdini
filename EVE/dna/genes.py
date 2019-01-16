'''
Database communication file

Currently contain ASSET and SHOT data. In future this data would be taken from Shotgun.
'''

'''
sys.path.append('C:/python-api-master')
import shotgun_api3
sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

# Setup
projectName = 'TESTER'
episodeCode = '010'
shotCode = 'SHOT_010'



project = sg.find_one("Project",[['name', 'is', projectName]],['name'])
episode = sg.find_one('Sequence', [['project.Project.name', 'is', projectName], ['code', 'is', episodeCode]], ['code']) 
shot = sg.find_one("Shot",[['project.Project.name', 'is', projectName], ['sg_sequence.Sequence.code', 'is', episodeCode]],['code', 'assets'])

# Get assets linked to a shot 010 > SHOT_010
asset = sg.find('Asset', [['shots.Shot.code', 'is', shotCode], ['shots.Shot.sg_sequence.Sequence.code', 'is', episodeCode]], ['code', 'sg_asset_type'])
'''

projectName = 'NSI'
episodeCode = '010'
shotCode = 'SHOT_010'


project = {'type': 'Project', 'id': 0, 'name': 'NSI'}
episode = {'code': '010', 'type': 'Sequence', 'id': 0}
shot =  {'code': 'SHOT_010', 'type': 'Shot', 'id': 0,
            'assets': [{'type': 'Asset', 'id': 0, 'name': 'CITY'},
                       {'type': 'Asset', 'id': 0, 'name': 'ROMA'}]}