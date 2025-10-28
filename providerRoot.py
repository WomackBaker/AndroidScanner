import os
import sys
import xml.etree.ElementTree as ET
from colorama import Fore, Style, init

def find_xml_files(root_dir):
    """
    Recursively find all .xml files in the given directory.
    """
    xml_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.xml'):
                xml_files.append(os.path.join(dirpath, filename))
    return xml_files

def check_for_path_slash(xml_file):
    """
    Parse the XML file and check for any tags that have path="/".
    Returns a list of (tag, attributes) where path="/" was found.
    """
    vulnerabilities = []
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        # Iterate over all elements in the XML
        for elem in root.iter():
            # Check if the element has a 'path' attribute
            path_attr = elem.get('path')
            if path_attr == '/':
                # Store the tag and full element attributes for reporting
                vulnerabilities.append((elem.tag, elem.attrib))
    except ET.ParseError:
        # If the file isn't valid XML, just skip it
        pass
    except Exception as e:
        # Catch-all for any other issues (permissions, etc.)
        print(Fore.RED + f"Error reading {xml_file}: {e}" + Style.RESET_ALL)
    
    return vulnerabilities

def main(root_dir):
    """
    Main function to scan the directory and report any path="/".
    """
    xml_files = find_xml_files(root_dir)
    found_any = False

    for xml_file in xml_files:
        vulnerabilities = check_for_path_slash(xml_file)
        if vulnerabilities:
            found_any = True
            for (tag, attribs) in vulnerabilities:
                print(
                    Fore.RED + Style.BRIGHT +
                    f"FOUND '{tag}' WITH PATH='/' IN {xml_file}" +
                    Style.RESET_ALL
                )


if __name__ == "__main__":
    init(autoreset=True)

    if len(sys.argv) != 2:
        print(Fore.RED + "Usage: python check_fileproviders.py <path_to_directory>" + Style.RESET_ALL)
        sys.exit(1)

    directory_path = sys.argv[1]
    main(directory_path)
