import re
import sys
import os
import xml.etree.ElementTree as ET
from colorama import Fore, Style, init

def find_extra(exported_activities, base_path):
        
    for activity in exported_activities:
        name_match = re.search(r'android:name="([^"]*)"', activity)
        if not name_match:
            continue
            
        class_name = name_match.group(1)
        relative_path = class_name.replace('.', '/') + '.smali'
        
        # Search for the file in the base directory
        found_files = []
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".smali") and os.path.join(root, file).endswith(relative_path):
                    found_files.append(os.path.join(root, file))
        
        # Process found files
        for smali_file_path in found_files:
            with open(smali_file_path, 'r', encoding='utf-8') as smali_file:
                smali_content = smali_file.read()
                onCreate_match = re.search(r'\.method\s+.*?\bonCreate\b.*?\(.*?\).*?\n((?:.|\n)*?)\.end\s+method', smali_content, re.DOTALL)
                
                if not onCreate_match:
                    continue
                
                onCreate_content = onCreate_match.group(1)
                checks = [ 
                    "getIntent()",
                    "getAction()",
                    "getData()",
                    "getCategories()",
                    "getFlags()",
                    "getComponent()",
                    "getComponent().getClassName()",
                    "getStringExtra()",
                    "getBooleanExtra()",
                    "getIntExtra()",
                    "getLongExtra()",
                    "getFloatExtra()",
                    "getDoubleExtra()",
                    "getByteExtra()",
                    "getShortExtra()",
                    "getCharExtra()",
                    "getStringArrayExtra()",
                    "getBooleanArrayExtra()",
                    "getIntArrayExtra()",
                    "getLongArrayExtra()",
                    "getFloatArrayExtra()",
                    "getDoubleArrayExtra()",
                    "getByteArrayExtra()",
                    "getShortArrayExtra()",
                    "getCharArrayExtra()",
                    "getStringArrayListExtra()",
                    "getIntegerArrayListExtra()",
                    "getCharSequenceArrayListExtra()",
                    "getParcelableExtra()",
                    "getParcelableArrayExtra()",
                    "getParcelableArrayListExtra()",
                    "getSerializableExtra()",
                    "getBundleExtra()",
                    "getDataString()",
                    "getType()",
                    "getClipData()",
                    "getSourceBounds()",
                    "getSelector()"
                ]

                for check in checks:
                    if check in smali_content:
                        print(f"{Fore.RED}{check}: {smali_file_path}{Style.RESET_ALL}")


if __name__ == "__main__":
    init(autoreset=True)

    if len(sys.argv) != 2:
        print("Usage: python findTests.py <path_to_directory>")
        sys.exit(1)

    path = sys.argv[1]
    manifest_file_path = f'{path}/AndroidManifest.xml'

    try:
        with open(manifest_file_path, 'r', encoding='utf-8') as file:
            manifest_content = file.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File not found: {manifest_file_path}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error reading manifest file: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

    pattern = re.compile(r'<activity[^>]*(?:android:exported="true"|android:exported="1")[^>]*>')
    exported_activities = pattern.findall(manifest_content)
    find_extra(exported_activities, path)