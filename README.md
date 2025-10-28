# AndroidScanner

AndroidScanner is a small collection of Python and shell/PowerShell helper scripts to perform automated, static checks against Android APKs. It decompiles APKs (via apktool) and searches the decompiled output for common issues such as exported components, hardcoded secrets, API endpoints, provider misconfigurations, and unsafe Intent handling.

## Quick start (Windows / PowerShell)

1. Install Python 3.7+ and Java (JDK) if you don't already have them.
2. From the project root, install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the scanner on a single APK (PowerShell):

```powershell
# analyze single APK
python apk_scanner.py "C:\path\to\app.apk"

# analyze all APKs in a folder
python apk_scanner.py "C:\path\to\apks\folder"

# write report to file
python apk_scanner.py --report security_report.txt "C:\path\to\app.apk"
```

Notes:
- The repository includes `apktool.bat` and `apktool.jar` for convenience on Windows. Ensure Java is on your PATH.
- The scripts are cross-platform; on Linux/macOS use `python3` and the included `apk_scanner.sh` when preferred.

## What this repo contains

- `apk_scanner.py` — Python entry-point that orchestrates decompilation and runs the small scanners
- `apktool.bat` / `apktool.jar` — helper files for decompiling APKs on Windows
- `exported.py` — finds exported Activities/Services/Receivers/Providers
- `customactions.py` — finds custom Intent actions
- `findkeys.py` — heuristics for hardcoded keys/secrets in code and resources
- `findendpoints.py` — extracts URLs and API endpoints
- `permissions.py` — analyzes requested Android permissions
- `providerRoot.py` — detects insecure FileProvider path configs (e.g., path="/")
- `findTests.py` — checks for unsafe Intent handling patterns
- `requirements.txt` — Python dependencies

## Design / contract (very small)

- Input: a single APK file path or a directory containing APK files.
- Output: console output with findings; optional report file when `--report` is used.
- Error modes: missing Java/apktool or malformed APKs will surface clear error messages.

Edge cases to be aware of:
- Large APKs may take longer to decompile; run-time depends on system CPU and disk.
- False positives: heuristic searches (keys, endpoints) should be verified manually.
- Permission to scan: only analyze APKs you own or are authorized to test.

## Development & contribution

- Run individual modules directly for development/testing, e.g.

```powershell
python findkeys.py "C:\path\to\decompiled\folder"
```

- Add unit tests or detection rules as new modules or extend existing ones.

## License & legal

Use this tool for legitimate security research, auditing, or educational purposes only. The authors provide no warranty. Make sure you have authorization before analyzing any APKs.

---

If you'd like, I can also:
- add a brief example output section,
- add a `CONTRIBUTING.md` and a small test harness for one scanner module.
Let me know which you'd prefer next.
