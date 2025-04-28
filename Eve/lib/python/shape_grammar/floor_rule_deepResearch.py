"""
The 1 working solution from Deep Research GPT conversation
"""


# Rule Parsing: shape grammar magic
def evaluate_bucket(bucket, evaluated_buckets):
    """
    Build an abstract syntax tree (AST) from a bucket (inside | |).

    if we find a "matches", then token is a macro (e.g. "(A)"), otherwise it is a module (e.g. "A")

    ast_macro =[{'type': 'macro', 'parts': ['A'], 'star': False, 'max_rep': None}]
    ast_module =[{'type': 'module', 'parts': ['A'], 'star': False, 'max_rep': 1}]
    """

    bucket_is_macro = re.match(r"^\(([^)]+)\)(?:\*|(?:\[(\d+)\]))?$", bucket)
    print(f'>> bucket_is_macro: {bucket_is_macro}')

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


def evaluate_shape_grammar(building_style, level_index, facade_rule_token, P0, P1):
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
    
    levels_data = read_bdf_data(building_style)['levels']
    modules_data = read_bdf_data(building_style)['modules']

    rule_varialtion = 0
    floor_rule = levels_data[str(level_index)]['floor_rule'][facade_rule_token][rule_varialtion]
    print(f'>> floor_rule: {floor_rule}')

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

    # # Build world-space points from local cursor positions
    # placement_positions = []
    # for module_placement in module_placements.values():
    #     cursor = module_placement['cursor']
    #     world_position = P0 + split_axis * cursor
    #     placement_positions.append(world_position)

    # print(f'module_placements: {module_placements}')

    return module_placements

