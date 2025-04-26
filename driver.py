#!/usr/bin/env python3
"""
Driver script to:
  1) Convert Terraform to YAML
  2) Post-process YAML (e.g. strip leading '- ')
  3) Final traversal/export

No CLI arguments: adjust the configuration variables below.
"""
import subprocess
import sys
import os
import logging

# --------------------
# Configuration
# --------------------
# Source directory containing Terraform files
origin = "gen3-terraform"
# Intermediate output directories
temps = ["temp1", "temp2", "temp3", "temp4", ] 
# Final output directory
final = "helm"
# Directory where the helper scripts reside
script_dir = "scripts"

# To post-process specific files only, list relative paths here (from temp1).
# Leave empty to enable full folder-walk mode in post_proc.
PROBLEM_FILE_PATHS = [
    # "aws/modules/aurora/main.yaml",
    # "aws/modules/eks/asg.yaml",
    # "aws/modules/commons-vpc-es/cloud.yaml",
    # "aws/aurora_db/data.yaml",
    # "aws/modules/generic-bucket/cloud.yaml",
    # "aws/modules/waf/main.yaml",
]

# --------------------
# Setup logging
# --------------------
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# --------------------
# Validate source and prepare directories
# --------------------
if not os.path.isdir(origin):
    logger.error(f"Source directory '{origin}' does not exist.")
    sys.exit(1)
for d in temps + [final]:
    os.makedirs(d, exist_ok=True)

# --------------------
# Determine processing mode
# --------------------
if PROBLEM_FILE_PATHS:
    logger.info(f"Post-processing only specified files: {PROBLEM_FILE_PATHS}")
else:
    logger.info("No specific files listed: running folder-walk mode in post_proc")

# --------------------
# Define script sequence and their arguments
# --------------------

scripts = [
    # # tf_organiser.py: (source_dir, dest_dir)
    # (os.path.join(script_dir, 'tf_organiser.py'), [origin, temps[0]]), # for reorganising tf blocks in different files
    # # tf2yaml.py: (source_dir, dest_dir, --auto)
    # (os.path.join(script_dir, 'tf2yaml.py'), [temps[0], temps[1], '--auto', '--no-notebook']), # for converting tf to yaml
    # # post_proc.py: (source_dir, dest_dir, optional file list)
    # (os.path.join(script_dir, 'post-proc.py'), [temps[1], temps[2]] + PROBLEM_FILE_PATHS), # for post-processing yaml files
    # traverser.py: (source_dir, final_dir)
    (os.path.join(script_dir, 'traverser.py'), [temps[2], final]), # for reorganising folder structure
]

# --------------------
# Execute each script in order
# --------------------
for script_path, args in scripts:
    if not os.path.isfile(script_path):
        logger.error(f"Required script '{script_path}' not found.")
        sys.exit(1)

    cmd = [sys.executable, script_path] + args
    logger.info(f"[RUN] {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        logger.error(f"Script '{script_path}' failed with exit code {e.returncode}")
        sys.exit(e.returncode)
