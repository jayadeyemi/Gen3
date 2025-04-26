#!/usr/bin/env python3
import os
import argparse

def list_all_filenames(root_dir: str):
    """
    Walks root_dir recursively and yields only the filenames of all files found.
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            print(fname)

def main():
    parser = argparse.ArgumentParser(
        description="Recursively list all files in a directory, showing only filenames."
    )
    parser.add_argument(
        "directory",
        help="Path to the directory to walk"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found or not a directory: {args.directory}")
        return

    list_all_filenames(args.directory)

if __name__ == "__main__":
    main()
