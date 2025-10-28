# APK Security Scanner

A comprehensive security analysis tool for Android APK files that performs automated static analysis to identify common security vulnerabilities and misconfigurations.

## 🎯 Overview

This scanner automatically decompiles APK files and performs multiple security checks to identify:

- **Exported Components** - Activities, Services, Receivers, and Content Providers with the `exported="true"` attribute
- **Custom Actions** - Custom Intent actions that could be used maliciously
- **Hardcoded Secrets** - API keys, tokens, credentials, private keys, and other sensitive data
- **API Endpoints** - URLs and API endpoints that might leak sensitive information
- **Permissions** - Application permissions and their protection levels
- **File Provider Misconfigurations** - Content providers with vulnerable path configurations
- **Intent Security** - Insecure handling of Intent data in exported activities

## 🚀 Features

- **Automated Analysis** - One command to perform comprehensive security analysis
- **Batch Processing** - Analyze single APK files or entire directories of APKs
- **Report Generation** - Save results to a file for documentation
- **Color-Coded Output** - Easy-to-read terminal output with color highlighting
- **Cross-Platform** - Native Python version that works on Windows, Linux, and macOS
- **Multiple Interfaces** - PowerShell (Windows), Bash (Linux/macOS), and Python (all platforms)

## 📋 Prerequisites

Before using this scanner, ensure you have the following installed:

### Required Software

1. **Python 3.7+** - Install from [python.org](https://www.python.org/downloads/)
2. **Java** - Required for apktool
   - Windows: Install from [Oracle](https://www.oracle.com/java/technologies/downloads/)
   - Linux: `sudo apt-get install default-jdk`
   - macOS: `brew install openjdk`
3. **apktool** - Already included in this repository

### Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## 📦 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/AndroidScanner.git
cd AndroidScanner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure `apktool` is accessible:
   - The repository includes `apktool.jar` and `apktool.bat` for Windows
   - For Linux/macOS, install apktool globally or add it to your PATH

## 🎮 Usage

### Cross-Platform (Python) - Recommended

The Python version works on both Windows and Linux/macOS:

#### Analyze a single APK:
```bash
# Windows
python apk_scanner.py "C:\path\to\app.apk"

# Linux/macOS
python3 apk_scanner.py /path/to/app.apk
```

#### Analyze all APKs in a directory:
```bash
# Windows
python apk_scanner.py "C:\path\to\apk\folder"

# Linux/macOS
python3 apk_scanner.py /path/to/apk/folder
```

#### Generate a report file:
```bash
# Windows
python apk_scanner.py --report security_report.txt "C:\path\to\app.apk"

# Linux/macOS
python3 apk_scanner.py -r security_report.txt /path/to/app.apk
```

### Windows (PowerShell)

#### Analyze a single APK:
```powershell
.\apk_scanner.ps1 -TARGET C:\path\to\app.apk
```

#### Analyze all APKs in a directory:
```powershell
.\apk_scanner.ps1 -TARGET C:\path\to\apk\folder
```

#### Generate a report file:
```powershell
.\apk_scanner.ps1 -TARGET C:\path\to\app.apk -Report security_report.txt
```

### Linux/macOS (Bash)

#### Analyze a single APK:
```bash
./apk_scanner.sh /path/to/app.apk
```

#### Analyze all APKs in a directory:
```bash
./apk_scanner.sh /path/to/apk/folder
```

#### Generate a report file:
```bash
./apk_scanner.sh -r security_report.txt /path/to/app.apk
```

## 🔍 What Each Scanner Module Does

### 1. `exported.py`
Identifies exported components (Activities, Services, Receivers, Providers) that could be accessed by other apps without permission.

**Risk**: Malicious apps can trigger exported components, potentially leading to information disclosure or unauthorized actions.

### 2. `customactions.py`
Discovers custom Intent actions that the app defines and uses.

**Risk**: Custom actions can be exploited by malicious apps to trigger unexpected app behavior.

### 3. `findkeys.py`
Searches for hardcoded secrets, API keys, tokens, and credentials throughout the decompiled code.

**Detects**:
- AWS credentials
- API keys (Stripe, PayPal, etc.)
- OAuth tokens
- Private keys (RSA, SSH, PGP)
- Cloudinary URLs
- Social media tokens
- Database credentials

**Risk**: Exposed credentials can lead to unauthorized access, data breaches, and financial losses.

### 4. `findendpoints.py`
Extracts URLs and API endpoints from the decompiled application.

**Detects**:
- HTTP/HTTPS URLs
- API endpoints
- REST API paths
- GraphQL endpoints
- Base URLs

**Risk**: Endpoints might leak internal infrastructure or be vulnerable to attacks.

### 5. `permissions.py`
Analyzes Android permissions requested by the app and flags potentially dangerous permissions.

**Risk**: Excessive or dangerous permissions can compromise user privacy and security.

### 6. `providerRoot.py`
Identifies FileProvider configurations with `path="/"` that expose the entire filesystem.

**Risk**: Path traversal vulnerability allowing access to sensitive files.

### 7. `findTests.py`
Analyzes exported activities for insecure Intent handling.

**Detects**:
- Usage of Intent data without validation
- Direct use of Intent extras without checking
- Potential for Intent-based attacks

**Risk**: Malicious apps can inject unexpected data through Intents, leading to crashes or unexpected behavior.

## 📊 Sample Output

```
╔═══════════════════════════════════════════════╗
║             APK SECURITY SCANNER              ║
╚═══════════════════════════════════════════════╝

[+] Processing single APK: myapp.apk...
[*] Decompiling APK...

EXPORTED ACTIVITY FOUND: com.example.MainActivity
EXPORTED SERVICE FOUND: com.example.BackgroundService
CUSTOM ACTION FOUND: com.example.app.CUSTOM_ACTION

KEY FOUND (AWS API Key in smali): AKIAIOSFODNN7EXAMPLE
KEY FOUND (Stripe API Key in Java): sk_live_51AbCdEfG...

=== URLS AND API ENDPOINTS FOUND ===
HTTP URL: https://api.example.com/v1/users
API Endpoint: /api/data/fetch

PERMISSION FOUND: android.permission.READ_EXTERNAL_STORAGE (protectionLevel: dangerous)

FOUND 'root-path' WITH PATH='/' IN res/xml/provider_paths.xml

[✓] Completed analysis for myapp.apk
```

## ⚠️ Security Considerations

- **Legal Use Only**: Only scan APK files that you own or have explicit permission to analyze
- **Educational Purpose**: This tool is designed for security research and educational purposes
- **No Warranty**: Use at your own risk. Always verify findings manually before taking action

## 🛠️ Project Structure

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
