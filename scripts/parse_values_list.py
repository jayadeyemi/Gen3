#!/usr/bin/env python3
"""
merge_yaml_tree.py

Recursively walk a directory, find all .yaml/.yml files, and merge them into a single YAML tree.

Usage:
    python merge_yaml_tree.py /path/to/input_dir host.yaml
If you omit the output filename, it defaults to 'host.yaml'.
"""

import os
import argparse
import yaml

def merge_trees(a, b):
    """
    Recursively merge two YAML nodes a and b:
    - dict + dict → merge per key
    - list + list → merge via merge_lists()
    - else → b replaces a
    """
    if isinstance(a, dict) and isinstance(b, dict):
        for key, b_val in b.items():
            if key in a:
                a[key] = merge_trees(a[key], b_val)
            else:
                a[key] = b_val
        return a

    if isinstance(a, list) and isinstance(b, list):
        return merge_lists(a, b)

    # For scalars or mismatched types, override with b
    return b

def merge_lists(a_list, b_list):
    """
    Merge two lists:
    - If an element is a single-key dict, merge children when the key matches;
      otherwise append unique items.
    - Non-dict or multi-key-dict items are appended if not already present.
    """
    for b_item in b_list:
        if isinstance(b_item, dict) and len(b_item) == 1:
            b_key, b_val = next(iter(b_item.items()))
            merged = False
            for a_item in a_list:
                if isinstance(a_item, dict) and b_key in a_item:
                    a_item[b_key] = merge_trees(a_item[b_key], b_val)
                    merged = True
                    break
            if not merged:
                a_list.append({b_key: b_val})
        else:
            if b_item not in a_list:
                a_list.append(b_item)
    return a_list

def load_and_merge(root_dir):
    """Walk root_dir for all YAML files and merge their documents."""
    merged: dict = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.lower().endswith(('.yaml', '.yml')):
                path = os.path.join(dirpath, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    docs = list(yaml.safe_load_all(f))
                for doc in docs:
                    if isinstance(doc, dict):
                        merged = merge_trees(merged, doc)
    return merged

def main():
    parser = argparse.ArgumentParser(
        description="Merge all YAML files under a directory into one tree."
    )
    parser.add_argument(
        "input_dir",
        help="Root directory to search for .yaml/.yml files."
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="host.yaml",
        help="Filename for the merged YAML (default: host.yaml)."
    )
    args = parser.parse_args()

    merged_tree = load_and_merge(args.input_dir)

    with open(args.output, 'w', encoding='utf-8') as out_f:
        yaml.safe_dump(
            merged_tree,
            out_f,
            default_flow_style=False,
            sort_keys=False
        )

    print(f"✅ Merged YAML written to {args.output}")

if __name__ == "__main__":
    main()
