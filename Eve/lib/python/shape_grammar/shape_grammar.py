"""
Parse BDF data
"""

import re
import hou
import json

   
# Data management: read from file, scene, populate to scene
def read_bdf_data(building_style):
    """
    Read BDF data
    """
    
    bdf_file_path = f"C:/Users/kko8/OneDrive/projects/procedural_city/PROD/3D/lib/grammar/{building_style}.json"
    with open(bdf_file_path, 'r') as f:
        bdf_data = json.load(f)

    print(f'>> BDF data file: {bdf_file_path.split("/")[-1]}')

    return bdf_data 


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


def get_mass_model_attributes(mass_model_node_name, facade_index):
    """
    Get attributes from current Mass Model.
    
    Assume each facade of mass model i a primitive. Get data from current prim attributes
        Facade orientation (F, S, R, ...) + 
        Facade scale factor (0-small, 1-medium, ...)
        Facade rule token: facade orientation + facade scale factor (F0, S0)
    """
    
    # Read current Mass Model data
    mass_model_node = hou.node(f"../{mass_model_node_name}")  
    mass_model_geo = mass_model_node.geometry()
    facade_prim = mass_model_geo.prim(facade_index)

    facade_orientation = facade_prim.attribValue("facade_orientation")
    facade_scale = facade_prim.attribValue("facade_scale")
    building_style = facade_prim.attribValue("building_style")
    facade_rule_token = f'{facade_orientation}{facade_scale}'   

    return facade_rule_token, building_style


def populate_levels_data(levels_data):
    """
    Populate levels data to scene: store dictionary on Detail attribute of facade
    """

    geo = hou.pwd().geometry()

    geo.addAttrib(hou.attribType.Global, "levels_data", {})
    geo.setGlobalAttribValue("levels_data", levels_data)
    

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
def evaluate_levels_data(mass_model_node_name, facade_index):
    """
    Evaluate levels data

    levels_data = {floor_index: {level_index: 0, floor_index: 0, position: (0.0, 0.0, 0.0)}}
    """
    
    # Get facade attributes
    facade_rule_token, building_style = get_mass_model_attributes(mass_model_node_name, facade_index)
    
    bdf_data = read_bdf_data(building_style)
    levels_data = bdf_data['levels']

    floor_index = 0
    floor_coordinates = [0.0]  # List to store floor coordinates
    expanded_levels_data = {}

    for level_index, floor_data in levels_data.items():
        for floor in range(floor_data['floor_repeat']):
            floor_height = floor_data['floor_height']

            # Store expanded floor data
            expanded_floor_data = {"level_index": level_index, "floor_index": floor_index, "floor_coordinate": floor_coordinates[-1]}
            expanded_levels_data[str(floor_index)] = expanded_floor_data

            # Update counters
            floor_coordinate = floor_height + floor_coordinates[-1]
            floor_coordinates.append(floor_coordinate)
            floor_index += 1            
    
    return expanded_levels_data


def evaluate_floors_data():
    """
    Evaluate floors data: how we place modules based of floor rule

    floors_data = {module_index: {module_name: "A", position: 0.0, module_width: 2.0, module_scale: 1.0}}
    """
    
    levels_data = {}

    return levels_data


def evaluate_bucket(bucket, evaluated_buckets):
    """
    Build an abstract syntax tree (AST) from a bucket (inside | |).

    if we find a "matches", then token is a macro (e.g. "(A)"), otherwise it is a module (e.g. "A")

    ast_macro =[{'type': 'macro', 'parts': ['A'], 'star': False, 'max_rep': None}]
    ast_module =[{'type': 'module', 'parts': ['A'], 'star': False, 'max_rep': 1}]
    """

    bucket_is_macro = re.match(r"^\(([^)]+)\)(?:\*|(?:\[(\d+)\]))?$", bucket)

    if bucket_is_macro:
        inner = bucket_is_macro.group(1)     # e.g. 'A' or 'W-A'
        star  = bucket.endswith("*")
        cap   = bucket_is_macro.group(2)
        max_rep = int(cap) if cap else None
        parts = inner.split("-")
        evaluated_buckets.append({"type":"macro", "parts":parts, "star":star, "max_rep":max_rep}) 
    else:  # Bucket is a module_code (e.g. "C")
        key = bucket.strip()
        if key:
            evaluated_buckets.append({ "type":"module", "parts":[key], "star": False, "max_rep":1})


def evaluate_shape_grammar(level_index, facade_rule_token, P0, P1):
    """
    Parse a single floor shape grammar rule string ("C|(W)|C") and
    return a list of world space split positions (Vector3).

    level_index: number of current level (0, 1, 2, ...)
    facade_rule_token: facade orientation + facade sacale factor (F0, S0, F1, etc) - comes from mass model
    P0: Facade start point
    P1: Facade end point

    # Data examples
    floor_rule = "(A)"
    modules_data = {"A": {"width": 2.0}}
    module_placements = {'0': {'module_code': 'A', 'cursor': 0.0, 'module_width': 1.8}, 
                         '1': {'module_code': 'A', 'cursor': 2.0, 'module_width': 1.8}, ...}


    
    evaluated_buckets for "C|(W)|C" ([]):
        {"type":"module", "parts":["C"], "star":False, "max_rep":1},
        {"type":"macro",  "parts":["W"], "star":False, "max_rep":None},
        {"type":"module", "parts":["C"], "star":False, "max_rep":1}
    """
    
    levels_data = read_bdf_data()['levels']
    modules_data = read_bdf_data()['modules']

    rule_varialtion = 0
    floor_rule = levels_data[str(level_index)]['floor_rule'][facade_rule_token][rule_varialtion]

    facade_length = (P1 - P0).length()
    split_axis = (P1 - P0).normalized()  # Facade local X axis
    # print(f'split_axis: {split_axis}))  #  facade_length: {facade_length}'

    # Tokenize buckets (tokens)
    buckets = floor_rule.split("|")

    # For each bucket, build a minimal Abstract Syntax Tree
    evaluated_buckets = []
    for bucket in buckets:
        evaluate_bucket(bucket, evaluated_buckets)

    print(f'evaluated_buckets: {evaluated_buckets}')

    # First pass: place mandatory copies and collect loop-macros
    module_placements = {}  # (module_code, cursor, module_width) data. To set prim attributes later in Houdini
    loopers    = []  # macros that can repeat indefinitely
    cursor     = 0.0 # cursor: module X position on facade in local facade coordinates
    module_index = 0 # Iteration of module placement

    for bucket in evaluated_buckets:
        for module_code in bucket["parts"]:
            module_width = modules_data[module_code]['width']
            placement = {"module_code": module_code, "cursor": cursor, "module_width": module_width}
            module_placements[str(module_index)] = placement

            cursor += module_width
            module_index += 1

        if bucket["type"]=="macro" and bucket["max_rep"] is None:
            loopers.append(bucket)

    # print(f'module_placements 1: {module_placements}')
    # print(f'loopers: {loopers}')

    # Loop-append phase
    remaining = facade_length - cursor
    # print(f'remaining: {remaining}')
    for bucket in loopers:
        macro_width = sum(modules_data[module_code]['width'] for module_code in bucket["parts"])
        full_copies = int( remaining // macro_width )  # how many full copies fit?
        
        if bucket["max_rep"] is not None: # cap if fixed max_rep
            full_copies = min(full_copies, bucket["max_rep"])
            
        for i in range(full_copies + 1):
            for module_code in bucket["parts"]:
                module_width = modules_data[module_code]['width']
                placement = {"module_code": module_code, "cursor": cursor, "module_width": module_width}
                module_placements[str(module_index)] = placement

                cursor += module_width
                module_index += 1
           
            remaining -= macro_width
   
    # # tar-scale last macro to absorb final slack
    # if evaluated_buckets and evaluated_buckets[-1]["star"]:
    #     slack = facade_length - cursor          # positive gap still empty
    #     if slack > 1e-6:
    #         parts = evaluated_buckets[-1]["parts"]
    #         total_nom = sum(modules_data[p]['width'] for p in parts)
    #         ratio = (slack + total_nom) / total_nom

    #         # find the last |parts| placements we just wrote
    #         for i, part in enumerate(parts[::-1], 1):
    #             idx = str(module_index - i)     # last entries in dict
    #             new_w = modules_data[part]['width'] * ratio
    #             module_placements[idx]["module_width"] = new_w

    # 7) STAR-BUCKET SCALING: if the last bucket was marked star, 
    #    stretch ALL of its placements to fill exactly facade_length.
    if evaluated_buckets and evaluated_buckets[-1]["star"]:
        total_used = cursor                                  # current total span
        if total_used > 1e-6:
            # print(f'total_used: {total_used}')
            scale_ratio = facade_length / total_used         # how much to stretch
            # Stretch every placement of THAT bucket
            last_parts = set(evaluated_buckets[-1]["parts"]) # e.g. {'A'}
            for key, placement in module_placements.items():
                if placement["module_code"] in last_parts:
                    # resize each A by the same ratio:
                    placement["module_width"] *= scale_ratio

            # (Optional) Recompute cursor = facade_length if you need it later
            cursor = facade_length

    # Build world-space points from local cursor positions
    placement_positions = []
    for module_placement in module_placements.values():
        cursor = module_placement['cursor']
        world_position = P0 + split_axis * cursor
        placement_positions.append(world_position)

    print(f'module_placements: {module_placements}')

    return module_placements, placement_positions
    
    
# Load Initial data 
def get_grammar_data():  

    bdf_data = read_bdf_data()

    # Get facade attributes
    facade_rule_token = get_facade_attributes()  # F0

    # Get vertical segmentation data
    number_of_levels, number_of_floors = get_number_of_floors(bdf_data)
    floor_coordinates, building_height = get_floor_coordinates(bdf_data)

    # Get horizontal segmentation data
    floors_data = get_floors_data(bdf_data, facade_rule_token)

    return number_of_levels, number_of_floors, floor_coordinates, floors_data
