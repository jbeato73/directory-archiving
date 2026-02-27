# Logger Cleaner

A specialized sanitization utility designed for infrastructure security and auditing. This tool processes raw connection logs to remove malformed entries and extract high-value data for cleaner reporting.

## 🚀 Key Features
* **Automated Sanitization:** Identifies and filters out lines with missing IP addresses or corrupted timestamps.
* **Security Focused:** Ensures that only well-formed connection data is passed on to downstream analytics tools.
* **UV-Powered:** Optimized for fast, isolated execution using the `uv` Python toolchain.

## 🛠️ Usage
1. **Prepare Data:** Place your `raw_connections.log` in the root directory.
2. **Execute Cleanup:**
   ```bash
   uv run clean