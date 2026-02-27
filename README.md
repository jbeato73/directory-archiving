### 2. Repository: `jbeato73/directory-archiving`
**Goal:** Demonstrate your ability to manage large-scale file systems (like the 4,800 ATMs you managed at BoA).

```markdown
# Directory Archiver

An infrastructure automation tool designed to manage large-scale log distribution. It dynamically organizes flat file structures into regional hierarchies, making it ideal for managing logs from distributed assets like ATMs or SD-WAN hubs.

## 🚀 Key Features
* **Regional Sorting:** Automatically parses filenames (e.g., `ATM_001_NY.log`) and moves them into region-specific folders (`/NY/`, `/TX/`).
* **Dry Run Safety:** Includes a `--dry-run` flag to preview file movements before they happen—essential for risk mitigation in production.
* **Audit Manifest:** Generates an `archive_report.csv` after every run to provide a permanent audit trail.

## 🛠️ Installation & Usage
1. **Sync Environment:**
   ```bash
   uv sync
Execute Archive:

Bash
uv run archive
📁 Output Structure
Plaintext
organized_infrastructure/
├── NY/
│   └── ATM_001_NY_2026.log
├── TX/
│   └── ATM_002_TX_2026.log
└── archive_report.csv