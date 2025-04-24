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


def expand_bucket(bucket, ast):
    """
    Build an abstract syntax tree (AST) from a bucket (inside | |).

    if we find a "matches", then token is a macro (e.g. "(A)"), otherwise it is a module (e.g. "A")

    ast_macro =[{'type': 'macro', 'parts': ['A'], 'star': False, 'max_rep': None}]
    ast_module =[{'type': 'module', 'parts': ['A'], 'star': False, 'max_rep': 1}]
    """

    matches = re.match(r"^\(([^)]+)\)(?:\*|(?:\[(\d+)\]))?$", bucket)

    if matches:
        inner = matches.group(1)     # e.g. 'A' or 'W-A'
        star  = bucket.endswith("*")
        cap   = matches.group(2)
        max_rep = int(cap) if cap else None
        parts = inner.split("-")
        ast.append({"type":"macro", "parts":parts, "star":star, "max_rep":max_rep}) 
    else:
        key = bucket.strip()
        if key:
            ast.append({ "type":"module", "parts":[key], "star": False, "max_rep":1})


def evaluate_shape_grammar(level_index, facade_rule_token, P0, P1,):
    """
    Parse a single floor shape grammar rule string and
    return a list of world space split positions (Vector3).
    """

    levels_data = read_bdf_data()['levels']
    modules_data = read_bdf_data()['modules']

    rule_varialtion = 0
    floor_rule = levels_data[str(level_index)]['floor_rule'][facade_rule_token][rule_varialtion]

    facade_length = (P1 - P0).length()
    axis  = (P1 - P0).normalized()

    # Tokenize buckets (tokens)
    buckets = floor_rule.split("|")

    # For each bucket, build a minimal Abstract Syntax Tree
    ast = []
    for bucket in buckets:
        expand_bucket(bucket, ast)

    print(ast)

    # 4) First pass: place mandatory copies and collect loop-macros
    placements = []
    loopers    = []
    cursor     = 0.0

    for bucket in ast:
        w_macro = sum(modules_data[module_code]['width'] for module_code in bucket["parts"])
        # mandatory: at least one
        for i in range(1):
            for module_code in bucket["parts"]:
                placements.append((module_code, cursor, modules_data[module_code]['width']))
                cursor += modules_data[module_code]['width']
        # mark loops
        if bucket["type"]=="macro" and bucket["max_rep"] is None:
            loopers.append(bucket)

    # 5) Loop-append phase
    remaining = facade_length - cursor
    for bucket in loopers:
        w_macro = sum(modules_data[module_code]['width'] for module_code in bucket["parts"])
        # how many full copies fit?
        count = int( remaining // w_macro )
        # cap if fixed max_rep
        if bucket["max_rep"] is not None:
            count = min(count, bucket["max_rep"])
        for i in range(count):
            for k in bucket["parts"]:
                placements.append((k, cursor, modules_data[k]['width']))
                cursor += modules_data[k]['width']
            remaining -= w_macro

    # 6) (optional) star-scale last macro to absorb final slack
    if ast and ast[-1]["star"]:
        slack = facade_length - cursor
        if slack>1e-4:
            # scale every part proportionally
            total_nom = sum(modules_data[module_code]['width'] for module_code in ast[-1]["parts"])
            ratio = (slack + total_nom)/total_nom
            for module_code in ast[-1]["parts"]:
                w0 = modules_data[module_code]['width']*ratio
                placements.append((module_code, cursor, w0))
                cursor += w0

    # Build world-space points
    split_positions = []
    for key, x0, w0 in placements:
        pt = P0 + axis * x0
        split_positions.append(pt)
        print(x0)
    
    # Extract x, y, z coordinates into separate lists. Houdini does not allow lists of Vectors.
    split_position_x = [pos[0] for pos in split_positions]
    split_position_y = [pos[1] for pos in split_positions]
    split_position_z = [pos[2] for pos in split_positions]

    return split_position_x, split_position_y, split_position_z
