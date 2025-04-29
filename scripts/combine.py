#!/usr/bin/env python3

import os
import yaml

def load_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

def merge_trees(dest, source):
    """
    Merge source tree into destination tree recursively.
    If keys match and both are dicts, recurse merge.
    Otherwise, overwrite.
    """
    for key, value in source.items():
        if key in dest:
            if isinstance(dest[key], dict) and isinstance(value, dict):
                merge_trees(dest[key], value)
            else:
                # If types are incompatible, overwrite
                dest[key] = value
        else:
            dest[key] = value

def walk_and_merge_yaml(source_dir):
    merged_tree = {}

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.yaml'):
                filepath = os.path.join(root, file)
                print(f"Loading: {filepath}")
                yaml_content = load_yaml_file(filepath)
                if isinstance(yaml_content, dict):
                    merge_trees(merged_tree, yaml_content)
                else:
                    print(f"Skipping non-dict YAML file: {filepath}")

    return merged_tree

def main():
    source_dir = "./your-source-folder"  # <- Set your source directory here
    destination_file = "host.yaml"

    merged_yaml = walk_and_merge_yaml(source_dir)

    with open(destination_file, 'w', encoding='utf-8') as f:
        yaml.dump(merged_yaml, f, sort_keys=False, default_flow_style=False)

    print(f"Merged YAML written to {destination_file}")

if __name__ == "__main__":
    main()
