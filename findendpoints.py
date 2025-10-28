import os
import re
import sys
from colorama import Fore, Style, init

# Define patterns to find URLs and API endpoints
url_patterns = {
    "HTTP URL": re.compile(r"https?://[^\s<>\"'`\]},\)]+"),
    "API Endpoint": re.compile(r"/api/[^\s<>\"'`\]},\)]+", re.IGNORECASE),
    "REST API": re.compile(r"/(v\d+/)?(api|rest)/[^\s<>\"'`\]},\)]+", re.IGNORECASE),
    "GraphQL Endpoint": re.compile(r"/graphql[^\s<>\"'`\]},\)]*", re.IGNORECASE),
    "Base URL": re.compile(r"base[_\-]?url\s*[=:]\s*['\"](https?://[^'\"]+)['\"]", re.IGNORECASE),
    "API Key in URL": re.compile(r"[\?&](api[_\-]?key|apikey|key)=([^&\s]+)", re.IGNORECASE),
}

def find_all_files(directory):
    """Recursively find all files in the directory."""
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def clean_url(url):
    """Remove common trailing characters and clean up URLs."""
    if not url:
        return None
    
    # Remove trailing punctuation that might have been captured
    url = url.rstrip('.,;:!?)}\]]')
    
    # Remove HTML entities and tags
    url = url.replace('&#47;', '/').replace('&amp;', '&')
    url = re.sub(r'<[^>]+>', '', url)
    
    # Filter out known false positives
    false_positives = [
        'http://schemas.android.com',
        'http://schemas.xmlsoap.org',
        'http://www.w3.org',
        'http://www.apple.com/DTDs',
        'http://java.sun.com',
        'xmlns:android'
    ]
    
    for fp in false_positives:
        if fp in url.lower():
            return None
    
    return url if len(url) > 3 else None

def extract_urls_from_content(content, file_path):
    """Extract URLs and endpoints from file content."""
    results = {}
    
    for pattern_name, pattern in url_patterns.items():
        matches = pattern.findall(content)
        if matches:
            for match in matches:
                # Clean up the match (remove trailing punctuation, parentheses, etc.)
                clean_match = clean_url(match)
                if clean_match and clean_match not in results.get(pattern_name, set()):
                    if pattern_name not in results:
                        results[pattern_name] = set()
                    results[pattern_name].add(clean_match)
    
    return results

def scan_file(file_path):
    """Scan a single file for URLs and endpoints."""
    results = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            results = extract_urls_from_content(content, file_path)
    except PermissionError:
        print(Fore.RED + f"Permission denied: {file_path}" + Style.RESET_ALL)
        return {}
    except UnicodeDecodeError:
        # Try reading as binary
        try:
            with open(file_path, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
                results = extract_urls_from_content(content, file_path)
        except Exception:
            return {}
    except Exception as e:
        return {}
    
    return results

def is_interesting_file(file_path):
    """Check if a file is likely to contain URLs (skip binary and library files)."""
    # Skip common binary/library files
    skip_extensions = ['.so', '.aar', '.class', '.dex', '.zip', '.jar', '.png', '.jpg', 
                      '.jpeg', '.gif', '.ico', '.webp', '.mp3', '.mp4', '.ogg']
    
    if any(file_path.lower().endswith(ext) for ext in skip_extensions):
        return False
    
    # Skip if in specific directories
    skip_dirs = ['build', 'bin', 'libs', 'res/drawable', 'res/mipmap', 'assets/fonts']
    if any(skip_dir in file_path.replace('\\', '/').lower() for skip_dir in skip_dirs):
        return False
    
    # Skip Android namespace XML files
    if 'schemas' in file_path.lower() and 'xml' in file_path.lower():
        return False
    
    return True

def main(directory):
    """Main function to scan directory for URLs and endpoints."""
    all_results = {}
    scanned_files = 0
    
    if os.path.isfile(directory):
        if is_interesting_file(directory):
            results = scan_file(directory)
            if results:
                all_results[directory] = results
    elif os.path.isdir(directory):
        all_files = find_all_files(directory)
        
        for file_path in all_files:
            if is_interesting_file(file_path):
                results = scan_file(file_path)
                if results:
                    all_results[file_path] = results
                scanned_files += 1
                
                # Progress indicator every 100 files (disabled)
                # if scanned_files % 100 == 0:
                #     print(Fore.YELLOW + f"Scanning... {scanned_files} files processed" + Style.RESET_ALL, end='\r')
    else:
        print(Fore.RED + "Invalid path provided. Please provide a valid file or directory path." + Style.RESET_ALL)
        sys.exit(1)
    
    # Print results
    if all_results:
        print(Fore.CYAN + Style.BRIGHT + "\n=== URLS AND API ENDPOINTS FOUND ===" + Style.RESET_ALL)
        
        for file_path, file_results in all_results.items():
            for pattern_name, urls in file_results.items():
                for url in urls:
                    # Truncate long file paths for display
                    display_path = file_path if len(file_path) < 80 else "..." + file_path[-77:]
                    print(f"{Fore.GREEN}{pattern_name}:{Style.RESET_ALL} {Fore.WHITE}{url}{Style.RESET_ALL}")
                    print(f"  {Fore.YELLOW}Found in: {display_path}{Style.RESET_ALL}")
        
        print(Fore.CYAN + Style.BRIGHT + "=====================================" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "No URLs or API endpoints found." + Style.RESET_ALL)

if __name__ == "__main__":
    init(autoreset=True)  # Initialize colorama

    if len(sys.argv) < 2:
        print(Fore.RED + "Usage: python findendpoints.py <path>" + Style.RESET_ALL)
        sys.exit(1)

    target_path = sys.argv[1]
    main(target_path)

