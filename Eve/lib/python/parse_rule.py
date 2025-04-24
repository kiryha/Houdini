# save as shape_grammar.py and import in your Python SOP
import hou
import re
import json

# TEMP
def read_bdf_data():
    """
    Read BDF data
    """
    
    bdf_file_path = "C:/Users/kko8/OneDrive/projects/procedural_city/PROD/3D/lib/grammar/BDF.json"
    with open(bdf_file_path, 'r') as f:
        bdf_data = json.load(f)

    return bdf_data


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


def evaluate_shape_grammar(level_index, facade_rule_token, P0, P1, split_axis):
    """
    Parse a single floor shape grammar rule string ("C|(W)|C") and
    return a list of world space split positions (Vector3).

    level_index: number of current level (0, 1, 2, ...)
    facade_rule_token: facade orientation + facade sacale factor (F0, S0, F1, etc) - comes from mass model
    P0: Facade start point
    P1: Facade end point
    split_axis: Facade local X axis

    # Data example
    floor_rule = "(A)"
    modules_data = {"A": {"width": 1.0}}

    AST for "C|(W)|C" ([]):

        {"type":"module", "parts":["C"], "star":False, "max_rep":1},
        {"type":"macro",  "parts":["W"], "star":False, "max_rep":None},
        {"type":"module", "parts":["C"], "star":False, "max_rep":1}

    """

    levels_data = read_bdf_data()['levels']
    modules_data = read_bdf_data()['modules']

    rule_varialtion = 0
    floor_rule = levels_data[str(level_index)]['floor_rule'][facade_rule_token][rule_varialtion]

    facade_length = (P1 - P0).length()
    print(f'split_axis: {split_axis}, facade_length: {facade_length}')

    # Tokenize buckets (tokens)
    buckets = floor_rule.split("|")

    # For each bucket, build a minimal Abstract Syntax Tree
    evaluated_buckets = []
    for bucket in buckets:
        evaluate_bucket(bucket, evaluated_buckets)

    print(f'evaluated_buckets: {evaluated_buckets}')

    # First pass: place mandatory copies and collect loop-macros
    module_placements = {}  # [(module_code, cursor, module_width)]
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

    print(f'module_placements 1: {module_placements}')
    print(f'loopers: {loopers}')

    # Loop-append phase
    remaining = facade_length - cursor
    print(f'remaining: {remaining}')
    for bucket in loopers:
        macro_width = sum(modules_data[module_code]['width'] for module_code in bucket["parts"])
        full_copies = int( remaining // macro_width )  # how many full copies fit?
        
        if bucket["max_rep"] is not None: # cap if fixed max_rep
            full_copies = min(full_copies, bucket["max_rep"])
            
        for i in range(full_copies+1):
            for module_code in bucket["parts"]:
                module_width = modules_data[module_code]['width']
                placement = {"module_code": module_code, "cursor": cursor, "module_width": module_width}
                module_placements[str(module_index)] = placement

                cursor += module_width
                module_index += 1
           
            remaining -= macro_width

    # print(f'module_placements: {module_placements}')
    
    # (optional) star-scale last macro to absorb final slack
    # if ast and ast[-1]["star"]:
    #     slack = facade_length - cursor
    #     if slack>1e-4:
    #         # scale every part proportionally
    #         total_nom = sum(modules_data[module_code]['width'] for module_code in ast[-1]["parts"])
    #         ratio = (slack + total_nom)/total_nom
    #         for module_code in ast[-1]["parts"]:
    #             w0 = modules_data[module_code]['width']*ratio
    #             placements.append((module_code, cursor, w0))
    #             cursor += w0

    # # Build world-space points
    # split_positions = []
    # for key, cursor, width in placements:
    #     pt = P0 + split_axis * cursor
    #     split_positions.append(pt)
    #     # split_positions.append([x0, 0.0, 0.0])

    return module_placements
