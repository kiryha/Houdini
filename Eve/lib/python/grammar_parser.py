"""
Parse BDF data
"""

import re
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
    modules_data = {"A": {"width": 1.0}}
    module_placements = {'1': {'0': {'module_code': 'A', 'cursor': 0.0, 'module_width': 2.0}}}

    
    evaluated_buckets for "C|(W)|C" ([]):
        {"type":"module", "parts":["C"], "star":False, "max_rep":1},
        {"type":"macro",  "parts":["W"], "star":False, "max_rep":None},
        {"type":"module", "parts":["C"], "star":False, "max_rep":1}
    """
    print(f'level_index: {level_index}, facade_rule_token: {facade_rule_token}, P0: {P0}, P1: {P1}')
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
    star_buckets = []  # macros that can be stretched
    cursor     = 0.0 # cursor: module X position on facade in local facade coordinates
    module_index = 0 # Iteration of module placement

    for bucket in evaluated_buckets:
        if bucket["type"] == "macro" and bucket["star"]:
            # Save starred buckets for later processing
            star_buckets.append(bucket)
            continue
            
        # Add one copy of each non-star module/macro
        for module_code in bucket["parts"]:
            module_width = modules_data[module_code]['width']
            placement = {"module_code": module_code, "cursor": cursor, "module_width": module_width}
            module_placements[str(module_index)] = placement

            cursor += module_width
            module_index += 1

        # Collect repeatable macros for the second pass
        if bucket["type"] == "macro" and bucket["max_rep"] is None and not bucket["star"]:
            loopers.append(bucket)

    # Loop-append phase for repeatable macros
    remaining = facade_length - cursor
    
    for bucket in loopers:
        macro_width = sum(modules_data[module_code]['width'] for module_code in bucket["parts"])
        full_copies = int(remaining // macro_width)  # how many full copies fit?
        
        if bucket["max_rep"] is not None: # cap if fixed max_rep
            full_copies = min(full_copies, bucket["max_rep"])
            
        for i in range(full_copies):  # Changed to not add the extra copy
            for module_code in bucket["parts"]:
                module_width = modules_data[module_code]['width']
                placement = {"module_code": module_code, "cursor": cursor, "module_width": module_width}
                module_placements[str(module_index)] = placement

                cursor += module_width
                module_index += 1
           
            remaining -= macro_width

    # Star-scale phase: handle starred macros to fill the remaining space
    if star_buckets and remaining > 1e-6:
        # For simplicity, we'll just use the first starred bucket
        star_bucket = star_buckets[0]
        
        # Calculate total nominal width of starred parts
        parts = star_bucket["parts"]
        total_nominal_width = sum(modules_data[p]['width'] for p in parts)
        
        # Calculate scaling ratio to fill remaining space
        scaling_ratio = (remaining / total_nominal_width)
        
        # Place the scaled modules
        for module_code in parts:
            original_width = modules_data[module_code]['width']
            scaled_width = original_width * scaling_ratio
            
            placement = {"module_code": module_code, "cursor": cursor, "module_width": scaled_width}
            module_placements[str(module_index)] = placement
            
            cursor += scaled_width
            module_index += 1

    # Build world-space points from local cursor positions
    placement_positions = []
    for module_placement in module_placements.values():
        cursor = module_placement['cursor']
        world_position = P0 + split_axis * cursor
        placement_positions.append(world_position)

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
