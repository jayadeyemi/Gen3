#!/usr/bin/env python3
"""
driver.py

Orchestrate your Terraform→YAML pipeline:
  1) tf_organiser.py   (re-organise .tf blocks)
  2) cleaner.py        (delete unwanted files)
  3) tf2yaml.py        (convert .tf → .yaml)
  4) post-proc.py      (strip leading '- ', etc.)
  5) traverser.py      (final layout/export)
  6) combine.py        (merge YAML outputs)
  7) (optional) cleaner.py (cleanup temp files)

Usage:
   driver.py [--work-dir WORK_DIR] [--clean]

  --work-dir: copy 'origin' into this folder first
  --clean:    append the cleaner.py step with CLEANUP_PATHS
"""
import os
import sys
import shutil
import argparse
import subprocess
import logging

# --------------------
# Configuration
# --------------------
origin = "gen3-terraform"       # Your original Terraform directory
temps = ["temp1", "temp2", "temp3"]
final = "yaml_dir"                  # Final intermediate output folder
script_dir = "scripts"          # Where your helper .py scripts live

# Paths to clean when --clean is specified
CLEANUP_PATHS = temps
COMBINED_FOLDER = "yaml_combined"  # Final output folder for combined YAML

# --------------------
# Build the base sequence
# --------------------
scripts = [
    (os.path.join(script_dir, 'tf_organiser.py'), [origin, temps[0]]),
    (os.path.join(script_dir, 'tf2yaml.py')     , [temps[0], temps[1], '--auto', '--no-notebook']),
    (os.path.join(script_dir, 'post-proc.py')   , [temps[1], temps[2]]),
    (os.path.join(script_dir, 'traverser.py')   , [temps[2], final]),
    (os.path.join(script_dir, 'combine.py')     , [final,   COMBINED_FOLDER]),
     (os.path.join(script_dir, 'parse_values_list.py'), [final, COMBINED_FOLDER + '/test.yaml'])
]

# --------------------
# CLI: workspace override and cleanup flag
# --------------------
parser = argparse.ArgumentParser(description="Run Terraform→YAML pipeline")
parser.add_argument(
    '--work-dir',
    help="If given, copy 'origin' here first and run everything in that folder"
)
parser.add_argument(
    '--clean',
    action='store_true',
    help="Run cleaner.py on CLEANUP_PATHS after the main pipeline"
)
args = parser.parse_args()

# --------------------
# Prepare workspace
# --------------------
if args.work_dir:
    work = os.path.abspath(args.work_dir)
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(origin, work)
    origin = work
    temps = [os.path.join(work, d) for d in temps]
    final = os.path.join(work, final)

# Append cleanup step if requested
if args.clean:
    scripts.append((os.path.join(script_dir, 'cleaner.py'), CLEANUP_PATHS))

# --------------------
# Setup logging & dirs
# --------------------
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

if not os.path.isdir(origin):
    logger.error(f"Source directory '{origin}' does not exist.")
    sys.exit(1)

for d in temps + [final] + [COMBINED_FOLDER]:
    os.makedirs(d, exist_ok=True)

# --------------------
# Execute the pipeline
# --------------------
for script_path, script_args in scripts:
    if not os.path.isfile(script_path):
        logger.error(f"Script not found: {script_path}")
        sys.exit(1)

    cmd = [sys.executable, script_path] + script_args
    logger.info(f"[RUN] {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {script_path} exited with {e.returncode}")
        sys.exit(e.returncode)

logger.info("Pipeline complete!")
