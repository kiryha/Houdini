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

    facade_rule_token:: string code of the facade rule key (F0, S0, R1, etc)
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


def get_mass_model_attributes(input_node_name):
    """
    Get attributes from current Mass Model.
    
    Assume each facade of mass model i a primitive. Get data from current prim attributes
        Facade orientation (F, S, R, ...) + 
        Facade scale factor (0-small, 1-medium, ...)
        Facade rule token: facade orientation + facade scale factor (F0, S0)
    """
    
    # Read current Mass Model data
    input_node = hou.node(f"../{input_node_name}")  
    mass_model_geo = input_node.geometry()
    facade_prim = mass_model_geo.prim(0)

    building_style = facade_prim.attribValue("building_style")
    facade_height = facade_prim.attribValue("facade_height")

    return building_style, facade_height


def populate_levels_data(levels_data):
    """
    Populate levels data to scene: store dictionary on Detail attribute of facade
    """

    geo = hou.pwd().geometry()

    geo.addAttrib(hou.attribType.Global, "levels_data", {})
    geo.setGlobalAttribValue("levels_data", levels_data)
    

# Rule parsing logic
def get_number_of_floors(facade_height, floor_height, current_level_index, levels_data):
    """
    Calculate how many floors can fit within the facade height while maintaining fixed floor heights.
    Each repeating level will get the same number of floors to maintain pattern consistency.
    The total height may be less than facade height to preserve floor heights.
    
    Args:
        facade_height (float): Total height of the facade
        floor_height (float): Height of a single floor (must remain fixed)
        current_level_index (str): Current level being processed
        levels_data (dict): Complete levels data from BDF
        
    Returns:
        int: Number of floors for the current level
    """
    
    if floor_height <= 0:
        print(">> WARNING: Floor height is zero or negative, defaulting to 1 floor")
        return 1

    # First pass: Calculate fixed height and identify repeating levels
    fixed_height = 0
    repeating_levels = []
    
    # Go through all levels in order
    for level_idx, level_data in levels_data.items():
        if level_data['floor_repeat'] == "*":
            repeating_levels.append({
                'index': level_idx,
                'height': level_data['floor_height']
            })
        else:
            fixed_height += level_data['floor_height'] * level_data['floor_repeat']

    # Available height for repeating levels
    available_height = facade_height - fixed_height
    
    if available_height <= 0:
        # print(">> WARNING: No space left for repeating floors after accounting for fixed levels")
        return 1

    # Find current level in repeating levels
    current_level = next((level for level in repeating_levels 
                         if level['index'] == current_level_index), None)
    
    if not current_level:
        print(">> ERROR: Current level not found in repeating levels")
        return 1

    # Calculate how many complete sets of repeating floors can fit
    # Each repeating level must have the same number of floors to maintain pattern
    floors_per_level = available_height // (sum(level['height'] for level in repeating_levels))
    
    return max(1, int(floors_per_level))


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
    pattern_width = sum(modules_data[m]["width"] for m in module_names)

    return pattern_width


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

    # print(f'>> building_style: {building_style}')
    # print(f'>> level_index: {level_index}')
    # print(f'>> facade_rule_token: {facade_rule_token}')

    # Read BDF data
    rule_varialtion = 0
    facade_length = round((P1 - P0).length(), 4)  # Round to 4 decimal places to avoid floating point issues
    levels_data = read_bdf_data(building_style)['levels']  
    modules_data = read_bdf_data(building_style)['modules']
    floor_rule = get_floor_rule(levels_data, level_index, facade_rule_token, rule_varialtion)

    # print(f'>> facade_length: {facade_length}')

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
                    module_width = modules_data[module_name]["width"]
                    set_module_placement(module_placements, idx, module_name, x, module_width, scale)
                    x += module_width * scale
                    idx += 1
            
            current_macro_region += 1

    return module_placements


# Houdini Calls
def evaluate_levels_data(mass_model_node_name, facade_bottom):
    """
    Evaluate levels data for Vertical split building into floors

    levels_data = {floor_index: {level_index: 0, floor_index: 0, position: (0.0, 0.0, 0.0)}}
    """

    # print(f'>> Evaluating levels...')

    # Get facade attributes
    building_style, facade_height = get_mass_model_attributes(mass_model_node_name)
    
    bdf_data = read_bdf_data(building_style)
    levels_data = bdf_data['levels']

    # First pass: Calculate total fixed height and identify repeatable levels
    fixed_height = 0
    repeatable_height = 0
    repeatable_levels = []
    
    for level_index, level_data in levels_data.items():
        floor_height = level_data['floor_height']
        floor_repeat = level_data['floor_repeat']
        
        if floor_repeat == "*":
            # For repeatable levels, calculate how many floors and store info
            number_of_floors = get_number_of_floors(facade_height, floor_height, level_index, levels_data)
            repeatable_levels.append({
                'level_index': level_index,
                'floor_height': floor_height,
                'number_of_floors': number_of_floors
            })
            # Add to repeatable height separately
            repeatable_height += floor_height * number_of_floors
        else:
            # For fixed levels, add to fixed height
            fixed_height += floor_height * floor_repeat
    
    # Calculate scale factor for repeatable levels
    floor_scale = 1.0
    if repeatable_levels and repeatable_height > 0:
        # Available height after accounting for fixed floors
        available_height = facade_height - fixed_height
        
        # Calculate scale factor to fit repeatable floors in available height
        if available_height > 0:
            floor_scale = available_height / repeatable_height
    
    # Second pass: Build expanded levels data
    floor_index = 0
    floor_coordinates = [facade_bottom]  # List to store Y coordinates of each floor
    expanded_levels_data = {}

    for level_index, level_data in levels_data.items():
        floor_height = level_data['floor_height']
        floor_repeat = level_data['floor_repeat']
        
        # Determine number of floors and scale for this level
        if floor_repeat == "*":
            number_of_floors = get_number_of_floors(facade_height, floor_height, level_index, levels_data)
            level_floor_scale = floor_scale  # Use the calculated scale for repeatable levels
        else:
            number_of_floors = floor_repeat
            level_floor_scale = 1.0  # No scaling for fixed floors
        
        scaled_floor_height = floor_height * level_floor_scale
        
        for _ in range(number_of_floors):
            # Store expanded floor data
            expanded_floor_data = {"level_index": level_index, 
                                  "floor_index": floor_index,
                                  "floor_height": floor_height,
                                  "floor_scale": level_floor_scale,
                                  "floor_coordinate": floor_coordinates[-1]}
            
            expanded_levels_data[str(floor_index)] = expanded_floor_data

            # Update counters
            floor_coordinate = scaled_floor_height + floor_coordinates[-1]
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

    prim = hou.node(f"../{input_node_name}").geometry().prim(0)

    building_style = prim.attribValue("building_style")
    level_index = prim.attribValue("level_index")
    P0 = hou.Vector3(prim.attribValue("P0"))
    P1 = hou.Vector3(prim.attribValue("P1"))
    split_axis = hou.Vector3(prim.attribValue("X"))
    facade_orientation = prim.attribValue("facade_orientation")
    facade_scale = prim.attribValue("facade_scale")
    facade_rule_token = f'{facade_orientation}{facade_scale}'
   
    module_placements = evaluate_floor_rule(building_style, level_index, facade_rule_token, P0, P1)
    # print(f'>> module_placements: {module_placements}')

    if not module_placements:
        return floor_data

    for module_index, module_data in module_placements.items():
        module_name = module_data['module_name']
        position = module_data['position']
        world_position = P0 + split_axis * position
        floor_data[str(module_index)] = {"module_name": module_name, 
                                         "module_width": module_data['module_width'],
                                         "module_scale": module_data['module_scale'],
                                         "x": world_position[0], 
                                         "y": world_position[1], 
                                         "z": world_position[2]}
    
    # # print(f'>> Floors completed')
    # print(f'>> floor_data: {floor_data}')

    return floor_data
   

def set_module_index(building_style):
    """
    Set module_index attribute for each modyle placement point when assemble buildings
    A1 > 0, E1 > 1, etc

    We sort list of modules by name and assign corresponding index from sorted list to each module
    We need to use same procedure when connecting all assets to SWITCH node
    (when copy modules to modyle placement points)
    """

    modules_data = read_bdf_data(building_style)['modules']

    module_names = list(modules_data.keys())
    module_names.sort()

    geo = hou.pwd().geometry()
    building_style = geo.point(0).attribValue("building_style")
    module_name = geo.point(0).attribValue("module_name")
    geo.addAttrib(hou.attribType.Point, "module_index", 256)

    for index, _module_name in enumerate(module_names):
        if module_name == _module_name:
            geo.points()[0].setAttribValue("module_index", index)


def get_floor_coordinates(levels_data):
    """
    Get list of floor coordinates for current level (to calculate floor indexes of split facade)
    Set resuld as detail attribute
    """

    # Convert string keys to integers for numerical sorting instead of lexicographical
    floor_dict = {}
    for key in levels_data:
        floor_dict[int(key)] = levels_data[key]
    
    # Sort keys numerically
    sorted_keys = sorted(floor_dict.keys())
    floor_coordinates = [floor_dict[key]["floor_coordinate"] for key in sorted_keys]

    geo = hou.pwd().geometry()
    geo.addArrayAttrib(hou.attribType.Global, "floor_coordinates", hou.attribData.Float)
    geo.setGlobalAttribValue("floor_coordinates", floor_coordinates)


def populate_floor_attributes(input_node_name, iterator_node_name):
    """
    Set level number for each facade primitive
    """

    geo = hou.pwd().geometry()

    levels_data = hou.node(f"../{input_node_name}").geometry().attribValue("levels_data")
    floor_index = hou.node(f"../{iterator_node_name}").geometry().attribValue("iteration")
    floor_index = str(floor_index)

    level_index = levels_data[floor_index]['level_index']
    floor_scale = levels_data[floor_index]['floor_scale']
    floor_height = levels_data[floor_index]['floor_height']

    # Assign values to each primitive
    for prim in geo.prims():
        prim.setAttribValue("level_index", int(level_index))
        prim.setAttribValue("floor_index", int(floor_index))
        prim.setAttribValue("floor_scale", floor_scale)
        prim.setAttribValue("floor_height", floor_height)


def populate_floor_data(floor_data):

    geo = hou.pwd().geometry()

    geo.addAttrib(hou.attribType.Global, "floor_data", {})
    geo.setGlobalAttribValue("floor_data", floor_data)


def populate_module_data(input_node_name, iterator_node_name):
    """
    Evaluate floor modules parameters and store them on primitives
    """

    geo = hou.pwd().geometry()

    floor_data = hou.node(f"../{input_node_name}").geometry().attribValue("floor_data")
    module_index = hou.node(f"../{iterator_node_name}").geometry().attribValue("iteration")
    module_index = str(module_index)
    
    # Skip if floor_data is wrong
    if not floor_data.get(module_index):
        return

    module_name = floor_data[module_index]['module_name']
    module_scale = floor_data[module_index]['module_scale']
    module_width = floor_data[module_index]['module_width']

    # Assign values to each primitive
    for prim in geo.prims():
        prim.setAttribValue("module_name", module_name)
        prim.setAttribValue("module_scale", module_scale)
        prim.setAttribValue("module_width", module_width)