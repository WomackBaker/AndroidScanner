import re
import sys
from colorama import Fore, Style, init

def find_exported_components(manifest_content):
    # Regex patterns to match exported components
    patterns = {
        'activity': re.compile(r'<activity[^>]*android:exported="true"[^>]*android:name="(?!com\.google\.|com\.android\.|androidx\.|com\.amazon\.)([^"]*)"[^>]*>'),
        'service': re.compile(r'<service[^>]*android:exported="true"[^>]*android:name="(?!com\.google\.|com\.android\.|androidx\.|com\.amazon\.)([^"]*)"[^>]*>'),
        'receiver': re.compile(r'<receiver[^>]*android:exported="true"[^>]*android:name="(?!com\.google\.|com\.android\.|androidx\.|com\.amazon\.)([^"]*)"[^>]*>'),
        'provider': re.compile(r'<provider[^>]*android:exported="true"[^>]*android:name="(?!com\.google\.|com\.android\.|androidx\.|com\.amazon\.)([^"]*)"[^>]*>')
    }

    results = {
        'activity': [],
        'service': [],
        'receiver': [],
        'provider': []
    }

    # Find all matches for each component type
    for component, pattern in patterns.items():
        matches = pattern.findall(manifest_content)
        results[component].extend(matches)

    return results

def print_results(results):
    colors = {
        'activity': Fore.RED,
        'service': Fore.GREEN,
        'receiver': Fore.WHITE,
        'provider': Fore.BLUE
    }

    for component, names in results.items():
        for name in names:
            print(f'{Style.BRIGHT}{colors[component]}{component.upper()} FOUND: {name}{Style.RESET_ALL}')

if __name__ == "__main__":
    init(autoreset=True)  # Initialize colorama

    if len(sys.argv) != 2:
        print("Usage: python exported.py <path_to_directory>")
        sys.exit(1)

    path = sys.argv[1]
    manifest_file_path = f'{path}/AndroidManifest.xml'

    try:
        with open(manifest_file_path, 'r') as file:
            manifest_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {manifest_file_path}")
        sys.exit(1)

    results = find_exported_components(manifest_content)
    print_results(results)