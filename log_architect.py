import os
import shutil
import argparse
import csv
from datetime import datetime


def organize_logs(dry_run=False):
    """
    Main logic to organize ATM logs into regional folders and generate a report.
    """
    source_dir = "unprocessed_logs"
    base_dest = "organized_infrastructure"
    report_file = "archive_report.csv"
    manifest = []

    # 1. Setup: Ensure dummy files exist for testing if the folder is empty
    if not os.path.exists(source_dir) or not os.listdir(source_dir):
        os.makedirs(source_dir, exist_ok=True)
        test_files = [
            "ATM_001_NY_2026.log",
            "ATM_002_TX_2026.log",
            "ATM_003_CA_2026.log",
            "ATM_004_NY_2026.log",
        ]
        for f in test_files:
            with open(os.path.join(source_dir, f), "w") as dummy:
                dummy.write("Sample ATM Log Data Content")
        print(f"🛠️ Created dummy test files in {source_dir}")

    print(f"🚀 Scanning {source_dir}... (Dry Run: {dry_run})")

    # 2. Process Files
    files = [f for f in os.listdir(source_dir) if f.endswith(".log")]
    moved_count = 0

    for filename in files:
        parts = filename.split("_")
        if len(parts) >= 3:
            region = parts[2]
            target_folder = os.path.join(base_dest, region)
            target_path = os.path.join(target_folder, filename)

            # Record for the manifest
            manifest.append(
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "filename": filename,
                    "region": region,
                    "action": "PREVIEW" if dry_run else "MOVED",
                }
            )

            if dry_run:
                print(f"🔍 [DRY RUN] Would move {filename} -> {region}/")
            else:
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(os.path.join(source_dir, filename), target_path)
                moved_count += 1

    # 3. Generate CSV Report
    with open(report_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["timestamp", "filename", "region", "action"]
        )
        writer.writeheader()
        writer.writerows(manifest)

    if not dry_run:
        print(f"✅ Successfully archived {moved_count} logs.")
    print(f"📊 Audit report generated: {report_file}")


def main():
    """
    Entry point for 'uv run archive'. Handles CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Archive ATM logs by region with audit reporting."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the file movements without actually executing them.",
    )
    args = parser.parse_args()

    organize_logs(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
