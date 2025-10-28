import os
import re
import xml.etree.ElementTree as ET
import sys
from colorama import Fore, Style, init

def extract_app_name(manifest_path):
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    return root.get('package')

def find_smali_files(root_dir):
    smali_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.smali'):
                smali_files.append(os.path.join(dirpath, filename))
    return smali_files

def find_custom_actions(smali_files, app_name):
    custom_actions = set()
    app_name_parts = app_name.split('.')
    if len(app_name_parts) >= 2:
        app_name_prefix = '.'.join(app_name_parts[:2])
    else:
        app_name_prefix = app_name

    action_pattern_full = re.compile(r'const-string\s+[vp]\d+,\s+"(' + re.escape(app_name) + r'\.[A-Z_]+)"')
    action_pattern_prefix = re.compile(r'const-string\s+[vp]\d+,\s+"(' + re.escape(app_name_prefix) + r'\.[A-Z_]+)"')

    for smali_file in smali_files:
        with open(smali_file, 'r') as file:
            for line in file:
                match_full = action_pattern_full.search(line)
                match_prefix = action_pattern_prefix.search(line)
                if match_full:
                    action = match_full.group(1)
                    custom_actions.add(action)
                elif match_prefix:
                    action = match_prefix.group(1)
                    custom_actions.add(action)
    return custom_actions

def main(root_dir):
    manifest_path = os.path.join(root_dir, 'AndroidManifest.xml')
    if not os.path.exists(manifest_path):
        print(Fore.RED + "AndroidManifest.xml not found.")
        return

    app_name = extract_app_name(manifest_path)
    smali_files = find_smali_files(root_dir)
    custom_actions = find_custom_actions(smali_files, app_name)

    if custom_actions:
        for action in custom_actions:
            print(Fore.MAGENTA + Style.BRIGHT + f"CUSTOM ACTION FOUND: {action}" + Style.RESET_ALL)

if __name__ == "__main__":
    init(autoreset=True)

    if len(sys.argv) != 2:
        print(Fore.RED + "Usage: python customactions.py <path_to_directory>")
        sys.exit(1)

    path = sys.argv[1]
    root_directory = path
    main(root_directory)