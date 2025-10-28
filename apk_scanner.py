#!/usr/bin/env python3
"""
APK Security Scanner - Cross-platform Python version
Works on both Windows and Linux/Unix systems
"""

import os
import sys
import re
import subprocess
import argparse
import shutil
from pathlib import Path
from typing import Optional


# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[1;34m'
    MAGENTA = '\033[1;35m'
    CYAN = '\033[1;36m'


def strip_ansi_codes(text: str) -> str:
    """Remove ANSI escape codes from text"""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


def robust_remove_directory(path: Path):
    """Robustly remove a directory, handling Windows-specific issues"""
    if not path.exists():
        return
    
    try:
        shutil.rmtree(path)
    except (OSError, PermissionError):
        # On Windows, try to remove individual files first
        import stat
        def remove_readonly(func, path_str, exc):
            """Handle read-only files on Windows"""
            if os.path.exists(path_str):
                os.chmod(path_str, stat.S_IWRITE)
                func(path_str)
        try:
            shutil.rmtree(path, onerror=remove_readonly)
        except Exception:
            pass  # Continue even if cleanup fails


def print_output(message: str, report_file: Optional[str] = None):
    """Print message with or without color codes based on report file"""
    if report_file:
        stripped = strip_ansi_codes(message)
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(stripped)
    else:
        print(message, end='')


def print_banner(report_file: Optional[str] = None):
    """Print the banner"""
    # Use simple ASCII characters for cross-platform compatibility
    if sys.platform == 'win32':
        # Windows-friendly banner
        banner = [
            "===============================================",
            "       APK SECURITY SCANNER",
            "==============================================="
        ]
    else:
        # Unicode characters for Linux/macOS
        banner = [
            "╔═══════════════════════════════════════════════╗",
            "║             APK SECURITY SCANNER              ║",
            "╚═══════════════════════════════════════════════╝"
        ]
    
    if report_file:
        for line in banner:
            with open(report_file, 'a', encoding='utf-8') as f:
                f.write(line + "\n")
    else:
        try:
            print(f"{Colors.CYAN}{banner[0]}{Colors.RESET}")
            print(f"{Colors.CYAN}{banner[1]}{Colors.RESET}")
            print(f"{Colors.CYAN}{banner[2]}{Colors.RESET}")
        except UnicodeEncodeError:
            # Fallback for terminals that don't support Unicode
            banner_ascii = [
                "===============================================",
                "       APK SECURITY SCANNER",
                "==============================================="
            ]
            print(f"{Colors.CYAN}{banner_ascii[0]}{Colors.RESET}")
            print(f"{Colors.CYAN}{banner_ascii[1]}{Colors.RESET}")
            print(f"{Colors.CYAN}{banner_ascii[2]}{Colors.RESET}")


def display_progress(current: int, total: int, report_file: Optional[str] = None):
    """Display a progress bar"""
    width = 50
    percentage = round(current * 100 / total)
    completed = round(width * current / total)
    remaining = width - completed
    
    progress_bar = '#' * completed + '-' * remaining
    message = f"\r[{progress_bar}] {current}/{total} ({percentage}%)"
    
    if report_file:
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(strip_ansi_codes(message) + "\n")
    else:
        print(message, end='', flush=True)


def check_apktool():
    """Check if apktool is available"""
    try:
        subprocess.run(['apktool'], capture_output=True, check=False)
        return True
    except FileNotFoundError:
        return False


def check_command(command: str) -> bool:
    """Check if a command exists in PATH"""
    return shutil.which(command) is not None


def decompile_apk(apk_path: str, output_dir: str) -> bool:
    """Decompile APK using apktool"""
    try:
        # Check for Java (apktool requires Java)
        if not check_command('java'):
            print(f"{Colors.RED}[-] Error: Java is required to run apktool. Please install Java.{Colors.RESET}")
            return False
        
        # Try apktool.jar first (bundled with the tool)
        jar_path = Path(__file__).parent / 'apktool.jar'
        if jar_path.exists():
            result = subprocess.run(
                ['java', '-jar', str(jar_path), 'd', '-f', apk_path, '-o', output_dir],
                capture_output=False,  # Let output go to console
                text=True
            )
            return result.returncode == 0
        # Try standard apktool command if jar is not available
        elif check_command('apktool'):
            result = subprocess.run(
                ['apktool', 'd', '-f', apk_path, '-o', output_dir],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        else:
            print(f"{Colors.RED}[-] Error: apktool not found. Please install apktool.{Colors.RESET}")
            return False
    except Exception as e:
        print(f"{Colors.RED}[-] Error during decompilation: {e}{Colors.RESET}")
        return False


def run_analysis_scripts(app_dir: str, report_file: Optional[str] = None) -> list:
    """Run all analysis scripts on the decompiled app"""
    scripts = [
        'exported.py',
        'customactions.py',
        'findkeys.py',
        'findendpoints.py',
        'permissions.py',
        'providerRoot.py',
        'findTests.py'
    ]
    
    script_dir = Path(__file__).parent
    
    for script in scripts:
        script_path = script_dir / script
        if not script_path.exists():
            print_output(f"{Colors.YELLOW}[!] Warning: {script} not found, skipping...{Colors.RESET}\n", report_file)
            continue
        
        try:
            python_cmd = sys.executable
            
            if report_file:
                with open(report_file, 'a', encoding='utf-8') as f:
                    subprocess.run(
                        [python_cmd, str(script_path), app_dir],
                        stdout=f,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
            else:
                subprocess.run([python_cmd, str(script_path), app_dir], check=False)
        except Exception as e:
            print_output(f"{Colors.RED}[-] Error running {script}: {e}{Colors.RESET}\n", report_file)


def process_single_apk(apk_path: str, report_file: Optional[str] = None):
    """Process a single APK file"""
    base_name = Path(apk_path).stem
    apk_name = Path(apk_path).name
    
    print_output(f"{Colors.GREEN}[+] Processing single APK: {apk_name}...{Colors.RESET}\n", report_file)
    
    # Create temp directory in current working directory
    current_dir = Path.cwd()
    target_app_dir = current_dir / f'.temp_{base_name}'
    
    # Remove existing directory if it exists
    robust_remove_directory(target_app_dir)
    
    # Decompile APK
    print_output(f"{Colors.BLUE}[*] Decompiling APK...{Colors.RESET}\n", report_file)
    
    if not decompile_apk(apk_path, str(target_app_dir)):
        print_output(f"{Colors.RED}[-] Error: Failed to decompile {apk_name}{Colors.RESET}\n", report_file)
        print_output(f"{Colors.CYAN}----------------------------------------{Colors.RESET}\n", report_file)
        return
    
    # Check if decompilation succeeded
    manifest_path = target_app_dir / 'AndroidManifest.xml'
    
    if not manifest_path.exists():
        print_output(f"{Colors.RED}[-] Error: Failed to decompile {apk_name}{Colors.RESET}\n", report_file)
        print_output(f"{Colors.CYAN}----------------------------------------{Colors.RESET}\n", report_file)
        return
    
    # Run analysis scripts
    if report_file:
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(f"Analyzing {apk_name}...\n")
    
    run_analysis_scripts(str(target_app_dir), report_file)
    
    if report_file:
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write("Analysis complete!\n")
    
    # Cleanup
    print_output(f"{Colors.BLUE}[*] Cleaning up decompiled files...{Colors.RESET}\n", report_file)
    robust_remove_directory(target_app_dir)
    
    print_output(f"{Colors.GREEN}[+] Completed analysis for {apk_name}{Colors.RESET}\n", report_file)
    print_output(f"{Colors.CYAN}----------------------------------------{Colors.RESET}\n", report_file)


def process_folder(folder_path: str, report_file: Optional[str] = None):
    """Process a folder containing APK files"""
    folder = Path(folder_path)
    
    print_output(f"{Colors.GREEN}[+] Processing folder: {folder_path}{Colors.RESET}\n", report_file)
    
    # Find all APK files
    apk_files = list(folder.glob('*.apk'))
    
    if not apk_files:
        print_output(f"{Colors.RED}[-] No APK files found in the specified folder.{Colors.RESET}\n", report_file)
        return
    
    apk_count = len(apk_files)
    print_output(f"{Colors.BLUE}[*] Found {apk_count} APK files to process{Colors.RESET}\n", report_file)
    
    current = 0
    
    for apk_file in apk_files:
        current += 1
        base_name = apk_file.stem
        apk_name = apk_file.name
        
        print_output(f"{Colors.GREEN}[+] Processing {apk_name} ({current}/{apk_count})...{Colors.RESET}\n", report_file)
        
        # Create temp directory in current working directory
        current_dir = Path.cwd()
        target_app_dir = current_dir / f'.temp_{base_name}'
        
        # Remove existing directory if it exists
        robust_remove_directory(target_app_dir)
        
        # Decompile APK
        print_output(f"{Colors.BLUE}[*] Decompiling APK...{Colors.RESET}\n", report_file)
        
        if not decompile_apk(str(apk_file), str(target_app_dir)):
            print_output(f"{Colors.RED}[-] Error: Failed to decompile {apk_name}{Colors.RESET}\n", report_file)
            print_output(f"{Colors.CYAN}----------------------------------------{Colors.RESET}\n", report_file)
            continue
        
        # Check if decompilation succeeded
        manifest_path = target_app_dir / 'AndroidManifest.xml'
        
        if not manifest_path.exists():
            print_output(f"{Colors.RED}[-] Error: Failed to decompile {apk_name}{Colors.RESET}\n", report_file)
            print_output(f"{Colors.CYAN}----------------------------------------{Colors.RESET}\n", report_file)
            continue
        
        # Run analysis scripts
        if report_file:
            display_progress(current, apk_count)
        
        run_analysis_scripts(str(target_app_dir), report_file)
        
        # Cleanup
        print_output(f"{Colors.BLUE}[*] Cleaning up decompiled files...{Colors.RESET}\n", report_file)
        robust_remove_directory(target_app_dir)
        
        print_output(f"{Colors.GREEN}[+] Completed analysis for {apk_name}{Colors.RESET}\n", report_file)
        print_output(f"{Colors.CYAN}----------------------------------------{Colors.RESET}\n", report_file)
    
    if report_file:
        print_output("\nProgress complete!\n", report_file)


def main():
    parser = argparse.ArgumentParser(
        description='APK Security Scanner - Cross-platform Python version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python apk_scanner.py path/to/app.apk
  python apk_scanner.py path/to/apk/folder
  python apk_scanner.py --report report.txt path/to/app.apk
  python apk_scanner.py -r report.txt path/to/apk/folder
        """
    )
    
    parser.add_argument('target', help='APK file or folder containing APK files')
    parser.add_argument('-r', '--report', metavar='FILE', help='Save output to specified report file')
    
    args = parser.parse_args()
    
    # Initialize report file
    report_file = args.report
    if report_file:
        # Clear report file
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('')
        print(f"Output will be saved to {report_file}")
    
    # Print banner
    print_banner(report_file)
    
    target_path = Path(args.target)
    
    # Validate target exists
    if not target_path.exists():
        print_output(f"{Colors.RED}[-] Error: '{args.target}' does not exist{Colors.RESET}\n", report_file)
        sys.exit(1)
    
    # Process based on target type
    if target_path.is_file():
        if target_path.suffix.lower() != '.apk':
            print_output(f"{Colors.RED}[-] Error: '{args.target}' is not a valid APK file{Colors.RESET}\n", report_file)
            sys.exit(1)
        
        process_single_apk(str(target_path), report_file)
    
    elif target_path.is_dir():
        process_folder(str(target_path), report_file)
    
    else:
        print_output(f"{Colors.RED}[-] Error: '{args.target}' is not a valid APK file or directory{Colors.RESET}\n", report_file)
        sys.exit(1)
    
    print_output(f"{Colors.GREEN}[+] All APK scanning operations completed!{Colors.RESET}\n", report_file)
    
    if report_file:
        print(f"\nReport saved to: {report_file}")


if __name__ == '__main__':
    main()

