import os
import re
import sys
from colorama import Fore, Style, init

# Define all the regex patterns with capturing groups for the key parts
regex_patterns = {
    "Cloudinary": r"cloudinary://([a-zA-Z0-9]+)",
    "Slack Token": r"(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
    "RSA private key": r"(-----BEGIN RSA PRIVATE KEY-----.*?-----END RSA PRIVATE KEY-----)",
    "SSH (DSA) private key": r"(-----BEGIN DSA PRIVATE KEY-----.*?-----END DSA PRIVATE KEY-----)",
    "SSH (EC) private key": r"(-----BEGIN EC PRIVATE KEY-----.*?-----END EC PRIVATE KEY-----)",
    "PGP private key block": r"(-----BEGIN PGP PRIVATE KEY BLOCK-----.*?-----END PGP PRIVATE KEY BLOCK-----)",
    "Amazon AWS Access Key ID": r"(AKIA[0-9A-Z]{16})",
    "Amazon MWS Auth Token": r"(amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    "AWS API Key": r"(AKIA[0-9A-Z]{16})",
    "Facebook Access Token": r"(EAACEdEose0cBA[0-9A-Za-z]+)",
    "Facebook OAuth": r"[f|F][a|A][c|C][e|E][b|B][o|O][k|K].*['|\"]([0-9a-f]{32})['|\"]",
    "GitHub": r"[g|G][i|I][t|T][h|H][u|U][b|B].*['|\"]([0-9a-zA-Z]{35,40})['|\"]",
    "Generic API Key": r"[a|A][p|P][i|I][_]?[k|K][e|E][y|Y].*['|\"]([0-9a-zA-Z]{32,45})['|\"]",
    "Generic Secret": r"[s|S][e|E][c|C][r|R][e|E][t|T].*['|\"]([0-9a-zA-Z]{32,45})['|\"]",
    "Heroku API Key": r"[h|H][e|E][r|R][o|O][k|K][u|U].*([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})",
    "MailChimp API Key": r"([0-9a-f]{32}-us[0-9]{1,2})",
    "Mailgun API Key": r"(key-[0-9a-zA-Z]{32})",
    "Password in URL": r"[a-zA-Z]{3,10}://[^/\s:@]{3,20}:[^/\s:@]{3,20}@.{1,100}[\"'\s]",
    "PayPal Braintree Access Token": r"(access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32})",
    "Picatic API Key": r"(sk_live_[0-9a-z]{32})",
    "Slack Webhook": r"(https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24})",
    "Stripe API Key": r"(sk_live_[0-9a-zA-Z]{24})",
    "Stripe Restricted API Key": r"(rk_live_[0-9a-zA-Z]{24})",
    "Square Access Token": r"(sq0atp-[0-9A-Za-z\-_]{22})",
    "Square OAuth Secret": r"(sq0csp-[0-9A-Za-z\-_]{43})",
    "Twilio API Key": r"(SK[0-9a-fA-F]{32})",
    "Twitter Access Token": r"[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*([1-9][0-9]+-[0-9a-zA-Z]{40})",
    "Twitter OAuth": r"[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*['|\"]([0-9a-zA-Z]{35,44})['|\"]",
    "Base64": r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
}

def find_all_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def findkeys(file_paths):
    for file_path in file_paths:
        findkeys_in_file(file_path)

def findkeys_in_file(file_path):
    keysfound = set()
    try:
        with open(file_path, 'r', errors='ignore') as f:
            content = f.read()
            for name, pattern in regex_patterns.items():
                matches = re.findall(pattern, content, flags=re.DOTALL)
                for match in matches:
                    if match not in keysfound:
                        keysfound.add(match)
                        print(Fore.CYAN + Style.BRIGHT + f"KEY FOUND ({name} in {file_path}): {match}" + Style.RESET_ALL)
    except PermissionError:
        print(Fore.RED + f"Permission denied: {file_path}" + Style.RESET_ALL)
    except UnicodeDecodeError:
        print(Fore.RED + f"Cannot decode file: {file_path}" + Style.RESET_ALL)
    return keysfound

def main(path):
    if os.path.isfile(path):
        findkeys_in_file(path)
    elif os.path.isdir(path):
        all_files = find_all_files(path)
        findkeys(all_files)
    else:
        print(Fore.RED + "Invalid path provided. Please provide a valid file or directory path." + Style.RESET_ALL)
        sys.exit(1)

if __name__ == "__main__":
    init(autoreset=True)

    if len(sys.argv) < 2:
        print(Fore.RED + "Usage: python findkeys.py <path>" + Style.RESET_ALL)
        sys.exit(1)

    target_path = sys.argv[1]
    main(target_path)
