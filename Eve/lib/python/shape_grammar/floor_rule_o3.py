# facade_grammar.py
"""
Minimal Houdini-side evaluator for the first three bucket-grammar patterns:
    "(A)"         – repeat whole modules
    "(A)*"        – repeat, scale to fill
    "C|(W)|C"     – fixed modules + repeating bucket
The code is written for Houdini’s Python environment (imports hou) but has
no other external dependencies.
"""

from typing import Dict, List, Tuple
import math
import hou


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tokenize(rule: str) -> List[str]:
    """Split a bucket grammar rule into tokens separated by ‘|’."""
    return [t for t in rule.split("|") if t]


def _classify(token: str) -> str:
    """Return one of: 'module', 'macro', 'macro_star'."""
    if token.startswith("(") and token.endswith(")*"):
        return "macro_star"
    if token.startswith("(") and token.endswith(")"):
        return "macro"
    return "module"


def _pattern_width(pattern: str, modules: Dict[str, Dict]) -> float:
    """Width of the pattern inside a (…) bucket."""
    inner = pattern.strip("()*")
    return sum(modules[m]["width"] for m in inner)


# ---------------------------------------------------------------------------
# Core evaluator
# ---------------------------------------------------------------------------

def evaluate_bucket_rule(
    rule: str,
    facade_length: float,
    modules: Dict[str, Dict],
) -> Tuple[List[float], Dict[int, Dict]]:
    """
    Return split positions (local X) and a per-module dictionary
    {index: {'module_name', 'position', 'module_width', 'module_scale'}}.
    Supports the three patterns requested.
    """
    tokens = _tokenize(rule)
    token_types = [_classify(t) for t in tokens]

    # Only one repeating bucket in the requested cases
    repeating_idx = next((i for i, typ in enumerate(token_types)
                          if typ.startswith("macro")), None)

    # Sum all fixed widths (regular modules)
    fixed_width = 0.0
    for t, typ in zip(tokens, token_types):
        if typ == "module":
            fixed_width += modules[t]["width"]

    # Pattern data for the repeating bucket (if any)
    if repeating_idx is not None:
        pattern = tokens[repeating_idx]
        p_width = _pattern_width(pattern, modules)
        leftover = facade_length - fixed_width
        if token_types[repeating_idx] == "macro":
            count = int(math.floor(leftover / p_width))
            scale = 1.0
        else:  # macro_star
            count = int(max(1, math.floor(leftover / p_width)))
            scale = leftover / (count * p_width)
    else:
        count = scale = 0.0  # not used

    # ---------------------------------------------------------------------
    # Emit positions
    # ---------------------------------------------------------------------
    x = 0.0
    splits: List[float] = []
    meta: Dict[int, Dict] = {}
    idx = 0

    for i, (tok, typ) in enumerate(zip(tokens, token_types)):
        if typ == "module":
            splits.append(x)
            w = modules[tok]["width"]
            meta[idx] = {
                "module_name": tok,
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
                    splits.append(x)
                    w = modules[m]["width"] * scale
                    meta[idx] = {
                        "module_name": m,
                        "position": x,
                        "module_width": w,
                        "module_scale": scale,
                    }
                    x += w
                    idx += 1

    return splits, meta


# ---------------------------------------------------------------------------
# World-space conversion
# ---------------------------------------------------------------------------

def local_x_to_world(p0, p1, x_values):
    """
    Convert local-X offsets to world positions along the P0-P1 vector
    """

    axis = (p1 - p0).normalized()
    return [p0 + axis * v for v in x_values]


# ---------------------------------------------------------------------------
# Example & quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # -- example BDF subset
    MODULES = {
        "C": {"width": 1.0},
        "A": {"width": 3.0},
        "W": {"width": 4.0},
        "R": {"width": 0.5},
    }

    P0 = hou.Vector3(0, 0, 0)
    P1 = hou.Vector3(11, 0, 0)
    façade_len = (P1 - P0).length()

    for rule in ["(A)", "(A)*", "C|(W)|C"]:
        splits, info = evaluate_bucket_rule(rule, façade_len, MODULES)
        w_points = local_x_to_world(P0, P1, splits)

        print(f"\nRule: {rule}")
        print("split positions (local X):", splits)
        print("module dict:", info)
        print("world points:", [tuple(p) for p in w_points])
