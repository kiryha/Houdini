"""
Module to calculate facade slicing into floors and modules according to text rule (Building Definition File, JSON)

Input:
    - grammar_rule: text rule
    - P0: start point of the floor
    - P1: end point of the floor
    - axis: local X axis of facade, slice happens along this axis
    - modules_data: modules name and size dictionary

Output:
    Floor slicing instructions:
    {module_index: {module_name: "A", position: 0.0, module_width: 2.0, module_scale: 1.0}}
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

    # print(f'>> BDF data file: {bdf_file_path.split("/")[-1]}')

    return bdf_data 


def get_floor_rule(levels_data, level_index, facade_rule_token, rule_varialtion):
    """
    Get floor rule from levels data dictionary
    """

    floor_rule = None
    level_data = levels_data.get(str(level_index))
    if level_data:
        floor_rules = level_data['floor_rule'].get(facade_rule_token)
        if floor_rules:
            floor_rule = floor_rules[rule_varialtion]
            if floor_rule:
                return floor_rule
            else:
                print(f'>> ERROR! Missing floor rule for rule variation: {rule_varialtion}')
        else:
            print(f'>> ERROR! Missing facade rule token: {facade_rule_token}')
    else:
        print(f'>> ERROR! Missing level data for level index: {level_index}')

    return None


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

    building_style = facade_prim.attribValue("building_style")

    return building_style


def populate_levels_data(levels_data):
    """
    Populate levels data to scene: store dictionary on Detail attribute of facade
    """

    geo = hou.pwd().geometry()

    geo.addAttrib(hou.attribType.Global, "levels_data", {})
    geo.setGlobalAttribValue("levels_data", levels_data)
    

def populate_floor_data(floor_data):

    geo = hou.pwd().geometry()

    geo.addAttrib(hou.attribType.Global, "floor_data", {})
    geo.setGlobalAttribValue("floor_data", floor_data)

# Rule parsing logic
def preprocess_buckets(buckets):
    """
    Preprocess buckets to handle [A]n syntax by converting them to macro form

    Converts [A]2 to (AA) for processing by the existing macro logic.
    """

    result = []
    for bucket in buckets:
        # Check if the token matches [X]n pattern
        match = re.match(r'\[(.+)\](\d+)$', bucket)
        if match:
            module = match.group(1)
            count = int(match.group(2))
            # Convert to a standard macro with repeated modules
            result.append('(' + '-'.join([module] * count) + ')')
        else:
            result.append(bucket)
            
    return result


def split_rule(rule):
    """
    Split and clean from empty stringsa bucket grammar rule (separated by '|') into tokens
    """

    buckets = [bucket for bucket in rule.split("|") if bucket]
    # Preprocess [A]n syntax into macro form
    buckets = preprocess_buckets(buckets)

    return buckets


def classify_buckets(buckets):
    """
    Create a list of all possible bucket types 
    
    ('module', 'macro', 'macro_star')
    """

    bucket_types = []
    for bucket in buckets:
        # Determine if bucket is a module name or expression (macro and macro with a star)
        if bucket.startswith("(") and bucket.endswith(")*"):
            bucket_types.append("macro_star")
        elif bucket.startswith("(") and bucket.endswith(")"):
            bucket_types.append("macro")
        else:
            bucket_types.append("module")

    return bucket_types


def get_module_width(bucket, modules_data):
    """
    Get the width of a module token, handling both simple and hyphenated names
    """

    if "-" in bucket:
        module_names = bucket.split("-")

        return sum(modules_data[name]["width"] for name in module_names)
    
    return modules_data[bucket]["width"]


def get_pattern_width(pattern, modules_data):
    """
    Width of the pattern inside a (…) bucket
    """
    inner = pattern.strip("()*")
    module_names = inner.split('-')  # <-- Split on hyphen
    return sum(modules_data[m]["width"] for m in module_names)


def expand_hyphenated_modules(bucket, modules_data):
    """
    Expand hyphenated module names like "A-B-C" into individual modules ["A", "B", "C"]
    Returns a list of individual module names
    """
    
    if "-" in bucket:
        return bucket.split("-")
    
    return [bucket]


def local_x_to_world(p0, p1, x_values):
    """
    Convert local-X offsets to world positions along the P0-P1 vector
    """

    axis = (p1 - p0).normalized()
    return [p0 + axis * v for v in x_values]


def set_module_placement(module_placements, idx, module_name, x, module_width, module_scale):
    """
    Set the placement of a module in the module_placements dictionary
    """
    
    module_placements[idx] = {
        "module_name": module_name,
        "position": x,
        "module_width": module_width,
        "module_scale": module_scale,
    }


def evaluate_floor_rule(building_style, level_index, facade_rule_token, P0, P1):
    """
    Return split positions (local X) and a per-module dictionary
    {index: {'module_name', 'position', 'module_width', 'module_scale'}}

    Supports several patterns:
    - "A"       - place module A
    - "(A)"     - repeat whole modules
    - "(A)*"    - repeat, scale to fill
    - "C|(W)|C" - fixed modules + repeating bucket
    - "[A]n"    - repeat module A exactly n times (converted to macro)
    - "A-B-C"   - place modules A, B, C in sequence

    building_style:: string code of the building style.
    We have one Building Definition File for each building style (brownstone, glass tower, pre‑war masonry, etc).
    The BDF name defined by building style.
    level_index:: number of current level (0, 1, 2, ...)
    facade_rule_token:: facade orientation + facade sacale factor (F0, S0, F1, etc) - comes from mass model
    P0:: Facade start point
    P1:: Facade end point
    """

    # Read BDF data
    rule_varialtion = 0
    facade_length = (P1 - P0).length()
    levels_data = read_bdf_data(building_style)['levels']  
    modules_data = read_bdf_data(building_style)['modules']
    floor_rule = get_floor_rule(levels_data, level_index, facade_rule_token, rule_varialtion)

    if not floor_rule:
        print(f'>> ERROR! Data missing in BDF!')
        return 
    
    # print(f'>> floor_rule: {floor_rule}')

    buckets = split_rule(floor_rule)  # "A|(B)*|C" -> ["A", "(B)*", "C"]
    bucket_types = classify_buckets(buckets)  # 'module', 'macro', 'macro_star'

    # First pass: calculate total fixed width and identify macro regions
    fixed_width = 0.0
    macro_regions = []  # Store info about each macro region
    current_fixed_width = 0.0
    
    for i, (bucket, bucket_type) in enumerate(zip(buckets, bucket_types)):
        if bucket_type == "module":
            width = get_module_width(bucket, modules_data) # "A" -> 2.0
            fixed_width += width
            current_fixed_width += width
        elif bucket_type.startswith("macro"):
            pattern = bucket
            pattern_width = get_pattern_width(pattern, modules_data)
            macro_regions.append({
                'index': i,
                'pattern': pattern,
                'pattern_width': pattern_width,
                'type': bucket_type,
                'preceding_fixed_width': current_fixed_width
            })
    
    # Calculate available space for each macro region
    remaining_length = facade_length - fixed_width
    if macro_regions:
        space_per_region = remaining_length / len(macro_regions)
        
    # Emit positions
    x = 0.0
    module_placements = {}
    idx = 0
    current_macro_region = 0

    for bucket, bucket_type in zip(buckets, bucket_types):
        if bucket_type == "module":
            # Handle hyphenated modules (A-B-C)
            module_names = expand_hyphenated_modules(bucket, modules_data) # "A-B-C" -> ["A", "B", "C"]
            for module_name in module_names:
                module_width = modules_data[module_name]["width"]
                set_module_placement(module_placements, idx, module_name, x, module_width, 1.0)
                x += module_width
                idx += 1
        elif bucket_type.startswith("macro"):
            # Get current macro region info
            region = macro_regions[current_macro_region]
            pattern_width = region['pattern_width']
            available_space = space_per_region
            
            if bucket_type == "macro":
                pattern_count = int(available_space // pattern_width)
                scale = 1.0
            else:  # macro_star
                pattern_count = max(1, int(available_space // pattern_width))
                scale = available_space / (pattern_count * pattern_width)
            
            inner = bucket.strip("()*")
            module_names = inner.split('-')
            for _ in range(pattern_count):
                for module_name in module_names:
                    module_width = modules_data[module_name]["width"] * scale
                    set_module_placement(module_placements, idx, module_name, x, module_width, scale)
                    x += module_width
                    idx += 1
            
            current_macro_region += 1

    return module_placements


# Houdini Calls
def evaluate_levels_data(mass_model_node_name, facade_index):
    """
    Evaluate levels data for Vertical split building into floors

    levels_data = {floor_index: {level_index: 0, floor_index: 0, position: (0.0, 0.0, 0.0)}}
    """

    # print(f'>> Evaluating levels...')

    # Get facade attributes
    building_style = get_mass_model_attributes(mass_model_node_name, facade_index)
    
    bdf_data = read_bdf_data(building_style)
    levels_data = bdf_data['levels']

    floor_index = 0
    floor_coordinates = [0.0]  # List to store Y coordinates of each floor
    expanded_levels_data = {}

    for level_index, floor_data in levels_data.items():
        for floor in range(floor_data['floor_repeat']):
            floor_height = floor_data['floor_height']

            # Store expanded floor data
            expanded_floor_data = {"level_index": level_index, 
                                   "floor_index": floor_index,
                                   "floor_coordinate": floor_coordinates[-1]}
            
            expanded_levels_data[str(floor_index)] = expanded_floor_data

            # Update counters
            floor_coordinate = floor_height + floor_coordinates[-1]
            floor_coordinates.append(floor_coordinate)
            floor_index += 1            
    
    # print(f'>> Levels completed')

    return expanded_levels_data


def evaluate_floor_data(input_node_name):
    """
    Evaluate floors data: how we place modules based of floor rule

    module_placements = {module_index: {module_name: "A", position: 0.0, module_width: 2.0, module_scale: 1.0}}
    """

    # print(f'>> Evaluating floor data...')   

    
    floor_data = {}

    building_style = hou.node(f"../{input_node_name}").geometry().prim(0).attribValue("building_style")
    level_index = hou.node(f"../{input_node_name}").geometry().prim(0).attribValue("level_index")
    P0 = hou.Vector3(hou.node(f"../{input_node_name}").geometry().prim(0).attribValue("P0"))
    P1 = hou.Vector3(hou.node(f"../{input_node_name}").geometry().prim(0).attribValue("P1"))
    split_axis = hou.Vector3(hou.node(f"../{input_node_name}").geometry().prim(0).attribValue("X"))
    facade_orientation = hou.node(f"../{input_node_name}").geometry().prim(0).attribValue("facade_orientation")
    facade_scale = hou.node(f"../{input_node_name}").geometry().prim(0).attribValue("facade_scale")
    facade_rule_token = f'{facade_orientation}{facade_scale}'
    
    module_placements = evaluate_floor_rule(building_style, level_index, facade_rule_token, P0, P1)

    if not module_placements:
        return floor_data

    for module_index, module_data in module_placements.items():
        module_name = module_data['module_name']
        position = module_data['position']
        world_position = P0 + split_axis * position
        floor_data[str(module_index)] = {"module_name": module_name, 
                                         "module_scale": module_data['module_scale'],
                                         "x": world_position[0], 
                                         "y": world_position[1], 
                                         "z": world_position[2]}
    
    # print(f'>> Floors completed')

    return floor_data
   
