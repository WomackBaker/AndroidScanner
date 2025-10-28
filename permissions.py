import re
import sys
from colorama import Fore, Style, init

def find_permissions(manifest_content):
    # Improved regex pattern with better handling of attribute order and spacing
    permission_pattern = re.compile(r'<permission\s+(?:[^>]*\s+)?android:name="([^"]*)"(?:[^>]*\s+)?(?:android:protectionLevel="([^"]*)")?[^>]*>')

    permissions = []

    # Find all permissions in the manifest
    permission_matches = permission_pattern.findall(manifest_content)
    for name, protection_level in permission_matches:
        # Add if no protection level is set or if it's not signature/dangerous
        if not protection_level or ('signature' not in protection_level.lower() and 'dangerous' not in protection_level.lower()):
            permissions.append((name, protection_level if protection_level else "not set"))

    return permissions

def print_permissions(permissions):
    if permissions:
        for name, protection_level in permissions:
            print(f"{Style.BRIGHT}{Fore.YELLOW}PERMISSION FOUND: {name} (protectionLevel: {protection_level}){Style.RESET_ALL}")
if __name__ == "__main__":
    init(autoreset=True)  # Initialize colorama

    if len(sys.argv) != 2:
        print("Usage: python permissions.py <path_to_directory>")
        sys.exit(1)

    path = sys.argv[1]
    manifest_file_path = f'{path}/AndroidManifest.xml'

    try:
        with open(manifest_file_path, 'r') as file:
            manifest_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {manifest_file_path}")
        sys.exit(1)

    permissions = find_permissions(manifest_content)
    print_permissions(permissions)