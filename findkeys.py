import os
import re
import sys
from colorama import Fore, Style, init

# Define all the regex patterns with capturing groups for the key parts
regex_patterns = {
    "Cloudinary": r"cloudinary://([a-zA-Z0-9]+)",
    "Firebase URL": r"(https?://[a-zA-Z0-9\-]+\.firebaseio\.com)",
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
    "Google API Key": r"(AIza[0-9A-Za-z\-_]{35})",
    "Google Cloud Platform API Key": r"(AIza[0-9A-Za-z\-_]{35})",
    "Google Cloud Platform OAuth": r"([0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com)",
    "Google Drive API Key": r"(AIza[0-9A-Za-z\-_]{35})",
    "Google Drive OAuth": r"([0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com)",
    "Google (GCP) Service-account": r"\"type\": \"service_account\"",
    "Google Gmail API Key": r"(AIza[0-9A-Za-z\-_]{35})",
    "Google Gmail OAuth": r"([0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com)",
    "Google OAuth Access Token": r"(ya29\.[0-9A-Za-z\-_]+)",
    "Google YouTube API Key": r"(AIza[0-9A-Za-z\-_]{35})",
    "Google YouTube OAuth": r"([0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com)",
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

def find_all_files(root_dir):
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def findkeys(all_files):
    keysfound = set()
    for file in all_files:
        with open(file, 'r', errors='ignore') as f:
            content = f.read()
            for name, pattern in regex_patterns.items():
                matches = re.findall(pattern, content)
                for match in matches:
                    if match not in keysfound:
                        keysfound.add(match)
                        print(Fore.CYAN + Style.BRIGHT + f"KEY FOUND ({name}): {match}" + Style.RESET_ALL)
    return keysfound

def main(root_dir):
    all_files = find_all_files(root_dir)
    findkeys(all_files)

if __name__ == "__main__":
    init(autoreset=True)

    if len(sys.argv) != 2:
        print(Fore.RED + "Usage: python findkeys.py <path_to_directory>")
        sys.exit(1)

    path = sys.argv[1]
    root_directory = path
    main(root_directory)