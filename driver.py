#!/usr/bin/env python3
"""
driver.py

Orchestrate your Terraform→YAML pipeline:
  1) tf_organiser.py   (re-organise .tf blocks)
  2) cleaner.py        (delete unwanted files)
  3) tf2yaml.py        (convert .tf → .yaml)
  4) post-proc.py      (strip leading '- ', etc.)
  5) traverser.py      (final layout/export)

Usage (no args): adjusts built-in config.
   With --work-dir: copies 'origin' into that folder first, then processes there.
"""
import os
import sys
import shutil
import argparse
import subprocess
import logging
import tempfile

# --------------------
# Configuration
# --------------------
origin = "gen3-terraform"       # Your original Terraform directory
temps = ["temp1", "temp2", "temp3"]
final = "temp4"                  # Final output folder
script_dir = "scripts"          # Where your helper .py scripts live

# If you only want to post-process specific YAML files (relative to temp2), list them:
CLEANUP_PATHS = temps
CLEANUP_FILES = ["kubernete.tf"]

# --------------------
# Build the sequence
# --------------------
#  1) tf_organiser.py  : (source_dir, dest_dir)
#  2) cleaner.py       : (one or more relative paths to remove)
#  3) tf2yaml.py       : (source_dir, dest_dir, --auto, --no-notebook)
#  4) post-proc.py     : (source_dir, dest_dir, [optional file list...])
#  5) traverser.py     : (source_dir, final_dir)
#  6) cleaner.py       : (list of folders to delete)
# --------------------

# Prepend temp[0] to each cleanup path:
cleanup_files = [os.path.join(temps[0], p) for p in CLEANUP_FILES]



scripts = [
    # (os.path.join(script_dir, 'tf_organiser.py'), [origin, temps[0]]),
    # (os.path.join(script_dir, 'cleaner.py')     ,  cleanup_files),
    # (os.path.join(script_dir, 'tf2yaml.py')     , [temps[0], temps[1], '--auto', '--no-notebook']),
    # (os.path.join(script_dir, 'post-proc.py')   , [temps[1], temps[2]]),
    # (os.path.join(script_dir, 'traverser.py')   , [temps[2], final]),
    (os.path.join(script_dir, 'cleaner.py')   , CLEANUP_PATHS),
]

# --------------------
# CLI: optional workspace override
# --------------------
parser = argparse.ArgumentParser(description="Run Terraform→YAML pipeline")
parser.add_argument(
    '--work-dir',
    help="If given, copy 'origin' here first and run everything in that folder"
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
    logger_root = f"(workspace={work})"
    # adjust paths to operate inside work
    origin = work
    temps = [os.path.join(work, d) for d in temps]
    final = os.path.join(work, final)
else:
    logger_root = ""

# --------------------
# Setup logging & dirs
# --------------------
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

if not os.path.isdir(origin):
    logger.error(f"Source directory '{origin}' does not exist.")
    sys.exit(1)

for d in temps + [final]:
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

logger.info(f"{logger_root} Pipeline complete!")
