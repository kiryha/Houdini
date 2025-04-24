"""
Parse BDF data
"""

import hou
import json

   
def get_facade_attributes():
    """
    Get attributes from current Mass Model
    """
    
    # Read current Mass Model data
    out_mass_model = hou.node("../out_mass_model")  
    mass_model_geo = out_mass_model.geometry()
    prim = mass_model_geo.prim(0)
    # Facade orientation (F, S, ...) + facade scale factor (0, 1, ...) = facade rule token (F0, S0)
    facade_orientation = prim.attribValue("facade_orientation")
    facade_scale = prim.attribValue("facade_scale")
    facade_rule_token = f'{facade_orientation}{facade_scale}'   

    return facade_rule_token


def read_bdf_data():
    """
    Read BDF data
    """
    
    bdf_file_path = "C:/Users/kko8/OneDrive/projects/procedural_city/PROD/3D/lib/grammar/BDF.json"
    with open(bdf_file_path, 'r') as f:
        bdf_data = json.load(f)

    return bdf_data

    
def get_number_of_floors(bdf_data):
    """
    Return number of levels and floors in facade
    """

    levels_data = bdf_data['levels']

    number_of_levels = len(levels_data.keys())
    number_of_floors = 0
    
    for floor_data in levels_data.values():
        floors = int(floor_data['floor_repeat'])
        number_of_floors += floors
        
    return number_of_levels, number_of_floors
    

def get_floor_coordinates(bdf_data):
    """
    Calculate Y coordinate of each floor of the facade
    """

    levels_data = bdf_data['levels']
    
    floor_coordinates = [0.0]  # 0.0 - first floor coordinate
    
    for floor_data in levels_data.values():
        for floor in range(floor_data['floor_repeat']):
            floor_height = floor_data['floor_height']
            floor_coordinate = floor_height + floor_coordinates[-1] 
            floor_coordinates.append(floor_coordinate)
            
    # Remove last coord cos we don't copy assets there
    building_height = floor_coordinates.pop()
    
    return floor_coordinates, building_height


# Rule Parsinhg
def expand_frool_rule(level_index, facade_rule_token, P0, P1, X):

    levels_data = read_bdf_data()['levels']
    modules_data = read_bdf_data()['modules']

    facade_width = (P1 - P0).length() 

    rule_varialtion = 0
    floor_rule = levels_data[str(level_index)]['floor_rule'][facade_rule_token][rule_varialtion]
    floor_rule = "(A)"


    split_positions = [(0.1, -0.5, 0.6), (0.8, 1.0, 0.5), (-0.3, 0.45, 0.67)]
    
    # Convert array of tuples to 3 lists of floats
    split_position_x = [pos[0] for pos in split_positions]
    split_position_y = [pos[1] for pos in split_positions]
    split_position_z = [pos[2] for pos in split_positions]

    return split_position_x, split_position_y, split_position_z
    
    
def get_floors_data(bdf_data, facade_rule_token):
    """
    {floor_index: {level_index: 0, split_positions: [0.1, 0.6, 0.9, 1.5, 2]}}
    """
    
    floors_data = {}
    floor_index = 0
    rule_varialtion = 0
    
    for level_index, level_data in bdf_data['levels'].items():
        for repeat_index in range(level_data['floor_repeat']):
            
            floor_data = {}
            
            floor_data['level_index'] = level_index
            floors_data[str(floor_index)] = floor_data
            
            floor_index += 1

    return floors_data



# Interface 
def init_data():
    
    # Get scene globals
    geo = hou.pwd().geometry()
    grammar_parser_node = hou.pwd()
    

    bdf_data = read_bdf_data()

    # Get facade attributes
    facade_rule_token = get_facade_attributes()  # F0

    # Get vertical segmentation data
    number_of_levels, number_of_floors = get_number_of_floors(bdf_data)
    floor_coordinates, building_height = get_floor_coordinates(bdf_data)

    # Get horizontal segmentation data
    floors_data = get_floors_data(bdf_data, facade_rule_token)

    # Populate attributes
    geo.addAttrib(hou.attribType.Global, "number_of_levels", number_of_levels)
    geo.addAttrib(hou.attribType.Global, "number_of_floors", number_of_floors)

    geo.addArrayAttrib(hou.attribType.Global, "floor_coordinates", hou.attribData.Float)
    geo.setGlobalAttribValue("floor_coordinates", floor_coordinates)

    geo.addAttrib(hou.attribType.Global, "floors_data", {})
    geo.setGlobalAttribValue("floors_data", floors_data) 
