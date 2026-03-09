# =============================================================================
# log_architect.py
#
# Author  : Jose M. Beato
# Created : March 9, 2026
# Built with the assistance of Claude (Anthropic) — claude.ai
#
# Description:
#   Organizes ATM branch log files into regional subdirectories based
#   on a naming convention (ATM_<id>_<region>_<year>.log). Supports a
#   dry-run mode that previews moves without executing them. Generates
#   a CSV archive manifest on every run.
#
# Project Setup (run in terminal before opening VS Code):
# ─────────────────────────────────────────────────────
#   1. cd /Users/jmb/PythonProjects
#   2. uv init directory-archiving
#   3. cd directory-archiving
#   4. code .
#   5. python3 -m venv .venv
#   6. source .venv/bin/activate
#   # No extra packages — 100% Python standard library
#   # Create this file as: log_architect.py
#
# GitHub Commit (after completing):
# ──────────────────────────────────
#   git add log_architect.py
#   git commit -m "refactor: standardize log_architect.py header and structure"
#   git push origin main
#
# Usage:
#   python3 log_architect.py             # Execute archive
#   python3 log_architect.py --dry-run   # Preview only, no files moved
# =============================================================================

import os       # Built-in: file and directory operations
import shutil   # Built-in: file move operations
import argparse # Built-in: CLI argument parsing
import csv      # Built-in: CSV manifest generation
from datetime import datetime  # Built-in: timestamp for manifest entries


# =============================================================================
# SECTION 1 — CONFIGURATION
# Best Practice: Keep directory paths and file names at the top so they're
# easy to update without searching through the script logic.
# =============================================================================

SOURCE_DIR   = "unprocessed_logs"        # Input directory of raw log files
DEST_BASE    = "organized_infrastructure" # Root destination for sorted logs
MANIFEST_CSV = "archive_report.csv"      # Output CSV listing all actions taken


# =============================================================================
# SECTION 2 — SAMPLE DATA SETUP
# Best Practice: When building a new script, generate synthetic test data
# if the real source directory doesn't exist. This lets you run and test
# the pipeline immediately without waiting for live data.
# =============================================================================


def create_sample_logs():
    """
    Creates dummy ATM log files in the source directory for testing.
    Only runs if the source directory is empty or missing.
    """
    os.makedirs(SOURCE_DIR, exist_ok=True)
    test_files = [
        "ATM_001_NY_2026.log",
        "ATM_002_TX_2026.log",
        "ATM_003_CA_2026.log",
        "ATM_004_NY_2026.log",
    ]
    for filename in test_files:
        filepath = os.path.join(SOURCE_DIR, filename)
        with open(filepath, "w") as f:
            f.write("Sample ATM Log Data Content")
    print(f"[INFO] Created {len(test_files)} sample log files in '{SOURCE_DIR}'")


# =============================================================================
# SECTION 3 — ARCHIVE LOGIC
# Best Practice: Keep the archive logic separate from CLI parsing.
# organize_logs() can be called directly by other scripts or tests.
# =============================================================================


def organize_logs(dry_run=False):
    """
    Scans the source directory for .log files and organizes them into
    regional subdirectories based on the filename convention:
        ATM_<id>_<REGION>_<year>.log

    Args:
        dry_run (bool): If True, previews moves without executing them.

    Returns:
        tuple[int, list[dict]]: (moved_count, manifest)
            moved_count — number of files actually moved (0 in dry-run)
            manifest    — list of action records for CSV report
    """
    # Generate sample data if source directory is empty
    if not os.path.exists(SOURCE_DIR) or not os.listdir(SOURCE_DIR):
        create_sample_logs()

    print()
    print("=" * 60)
    print("  log_architect.py — Starting...")
    print(f"  Mode: {'DRY RUN (preview only)' if dry_run else 'LIVE (files will be moved)'}")
    print("=" * 60)
    print(f"\n[INFO] Scanning '{SOURCE_DIR}'...\n")

    files      = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".log")]
    manifest   = []
    moved_count = 0

    for filename in files:
        parts = filename.split("_")
        if len(parts) >= 3:
            region        = parts[2]
            target_folder = os.path.join(DEST_BASE, region)
            target_path   = os.path.join(target_folder, filename)

            manifest.append({
                "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename"  : filename,
                "region"    : region,
                "action"    : "PREVIEW" if dry_run else "MOVED",
            })

            if dry_run:
                print(f"  [DRY RUN] Would move: {filename} → {region}/")
            else:
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(os.path.join(SOURCE_DIR, filename), target_path)
                moved_count += 1
                print(f"  [INFO]    Moved: {filename} → {region}/")

    return moved_count, manifest


# =============================================================================
# SECTION 4 — MANIFEST OUTPUT
# Best Practice: Separate file-writing from processing logic.
# =============================================================================


def write_manifest(manifest, filepath):
    """
    Writes the archive action manifest to a CSV file.

    Args:
        manifest (list[dict]): All archive action records.
        filepath (str):        Output CSV path.
    """
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["timestamp", "filename", "region", "action"]
        )
        writer.writeheader()
        writer.writerows(manifest)
    print(f"[INFO] Manifest written → '{filepath}'")


# =============================================================================
# SECTION 5 — SUMMARY PRINT
# Best Practice: Always print a human-readable summary to the console
# so you know what happened when you run the script.
# =============================================================================


def print_summary(moved_count, manifest, dry_run):
    """
    Prints a formatted archive summary to the console.

    Args:
        moved_count (int):       Number of files actually moved.
        manifest    (list[dict]): All action records.
        dry_run     (bool):       Whether the run was a preview.
    """
    print()
    print("=" * 60)
    print("  LOG ARCHITECT — SUMMARY REPORT")
    print("  Jose M. Beato | March 9, 2026")
    print("=" * 60)
    print(f"  Mode            : {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"  Files scanned   : {len(manifest)}")
    print(f"  Files moved     : {moved_count if not dry_run else 'N/A (dry run)'}")
    print(f"  Manifest        : {MANIFEST_CSV}")
    print("=" * 60)
    print()


# =============================================================================
# SECTION 6 — MAIN ENTRY POINT
# Best Practice: Always use `if __name__ == "__main__"` to protect your
# main logic. This allows other scripts to import organize_logs() without
# automatically running the pipeline.
# =============================================================================


def main():
    """
    Parses CLI arguments and orchestrates the full pipeline:
    Organize Logs → Write Manifest → Print Summary
    """
    parser = argparse.ArgumentParser(
        description="Archive ATM logs by region with a CSV audit manifest."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview file movements without executing them.",
    )
    args = parser.parse_args()

    moved_count, manifest = organize_logs(dry_run=args.dry_run)
    write_manifest(manifest, MANIFEST_CSV)
    print_summary(moved_count, manifest, args.dry_run)


if __name__ == "__main__":
    main()

