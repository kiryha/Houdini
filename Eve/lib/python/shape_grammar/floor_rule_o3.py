# facade_grammar.py
"""
Minimal Houdini-side evaluator for the first three bucket-grammar patterns:
    "(A)"         – repeat whole modules
    "(A)*"        – repeat, scale to fill
    "C|(W)|C"     – fixed modules + repeating bucket
    "[A]n"        – repeat module A exactly n times (treated as a macro)
    "A-B-C"       - place modules A, B, C in sequence
The code is written for Houdini's Python environment (imports hou) but has
no other external dependencies.
"""

from typing import Dict, List, Tuple
import math
import re
import hou


def _tokenize(rule):
    """
    Split and clean from empty stringsa bucket grammar rule (separated by '|') into tokens
    """

    return [t for t in rule.split("|") if t]


def _preprocess_tokens(tokens):
    """
    Preprocess tokens to handle [A]n syntax by converting them to macro form

    Converts [A]2 to (AA) for processing by the existing macro logic.
    """

    result = []
    for token in tokens:
        # Check if the token matches [X]n pattern
        match = re.match(r'\[(.+)\](\d+)$', token)
        if match:
            module = match.group(1)
            count = int(match.group(2))
            # Convert to a standard macro with repeated modules
            result.append('(' + module * count + ')')
        else:
            result.append(token)
    return result


def _classify(token):
    """
    Return one of: 'module', 'macro', 'macro_star'
    """

    if token.startswith("(") and token.endswith(")*"):
        return "macro_star"
    if token.startswith("(") and token.endswith(")"):
        return "macro"

    return "module"


def _pattern_width(pattern, modules):
    """
    Width of the pattern inside a (…) bucket
    """
    inner = pattern.strip("()*")
    return sum(modules[m]["width"] for m in inner)


def _expand_hyphenated_modules(module_token, modules):
    """
    Expand hyphenated module names like "A-B-C" into individual modules ["A", "B", "C"]
    Returns a list of individual module names
    """
    if "-" in module_token:
        return module_token.split("-")
    return [module_token]


def _get_module_width(module_token, modules):
    """
    Get the width of a module token, handling both simple and hyphenated names
    """
    if "-" in module_token:
        module_names = module_token.split("-")
        return sum(modules[name]["width"] for name in module_names)
    return modules[module_token]["width"]


def local_x_to_world(p0, p1, x_values):
    """
    Convert local-X offsets to world positions along the P0-P1 vector
    """

    axis = (p1 - p0).normalized()
    return [p0 + axis * v for v in x_values]


def evaluate_floor_rule(rule, facade_length, modules):
    """
    Return a dictionary with module placements information:
    {module_index: {'module_name', 'position', 'module_width', 'module_scale'}}
    
    Supports several patterns:
    - "(A)"     - repeat whole modules
    - "(A)*"    - repeat, scale to fill
    - "C|(W)|C" - fixed modules + repeating bucket
    - "[A]n"    - repeat module A exactly n times (converted to macro)
    - "A-B-C"   - place modules A, B, C in sequence
    """
    
    tokens = _tokenize(rule)
    # Preprocess [A]n syntax into macro form
    tokens = _preprocess_tokens(tokens)
    token_types = [_classify(t) for t in tokens]

    # Find the index of the first macro token (repeating bucket)
    repeating_bucket_index = next((i for i, typ in enumerate(token_types) if typ.startswith("macro")), None)

    # Sum all fixed widths (regular modules)
    fixed_width = 0.0
    for t, typ in zip(tokens, token_types):
        if typ == "module":
            fixed_width += _get_module_width(t, modules)

    # Pattern data for the repeating bucket (if any)
    if repeating_bucket_index is not None:
        pattern = tokens[repeating_bucket_index]
        pattern_width = _pattern_width(pattern, modules)
        leftover = facade_length - fixed_width
        if token_types[repeating_bucket_index] == "macro":
            count = int(leftover // pattern_width)
            scale = 1.0
        else:  # macro_star
            count = max(1, int(leftover // pattern_width))
            scale = leftover / (count * pattern_width)
    else:
        count = scale = 0.0  # not used

    # Emit positions
    x = 0.0
    module_placements = {}
    idx = 0

    for i, (tok, typ) in enumerate(zip(tokens, token_types)):
        if typ == "module":
            # Handle hyphenated modules (A-B-C)
            module_names = _expand_hyphenated_modules(tok, modules)
            for module_name in module_names:
                w = modules[module_name]["width"]
                module_placements[idx] = {
                    "module_name": module_name,
                    "position": x,
                    "module_width": w,
                    "module_scale": 1.0,
                }
                x += w
                idx += 1

        elif typ.startswith("macro"):
            inner = tok.strip("()*")
            inner_w = _pattern_width(tok, modules) * scale
            for _ in range(count):
                for m in inner:
                    w = modules[m]["width"] * scale
                    module_placements[idx] = {
                        "module_name": m,
                        "position": x,
                        "module_width": w,
                        "module_scale": scale,
                    }
                    x += w
                    idx += 1

    return module_placements


if __name__ == "__main__":

    # -- example BDF subset
    MODULES = {
        "C": {"width": 1.0},
        "A": {"width": 3.0},
        "B": {"width": 2.0},
        "W": {"width": 4.0},
        "R": {"width": 0.5},
    }

    P0 = hou.Vector3(0, 0, 0)
    P1 = hou.Vector3(11, 0, 0)
    façade_len = (P1 - P0).length()

    for rule in ["A", "A|B", "[A]2", "(C)", "(C)*", "C|(W)|C",  "C|A-B|(A)*|A-B|C"]:
        # building_style, level_index, facade_rule_token, P0, P1
        module_placements = evaluate_floor_rule(rule, façade_len, MODULES)
        
        # Extract positions from the module placements dictionary for world conversion
        positions = [data["position"] for data in module_placements.values()]
        w_points = local_x_to_world(P0, P1, positions)

        print(f"\nRule: {rule}")
        print("module_placements:", module_placements)
        print("world points:", [tuple(p) for p in w_points])
