import os
import requests
import hashlib
from datetime import datetime

# ----------------------------
# CONFIGURATION
# ----------------------------

# List of websites to monitor
URLS = [
    "https://example.com/news",
    "https://anotherwebsite.com/updates",
    "https://yetanother.com/blog"
]

# Telegram bot token and chat ID (from GitHub Secrets)
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------

def send_telegram(msg):
    """Send a message to your Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_page_hash(url):
    """Download the page and return its MD5 hash."""
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        content = r.text
        return hashlib.md5(content.encode()).hexdigest()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def sanitize_filename(url):
    """Convert URL into a safe filename by hashing it."""
    return "hash_" + hashlib.md5(url.encode()).hexdigest() + ".txt"

# ----------------------------
# MAIN LOGIC
# ----------------------------

updates = []

for site in URLS:
    new_hash = get_page_hash(site)
    if new_hash is None:
        continue  # skip if fetch failed

    filename = sanitize_filename(site)

    # Read the previous hash
    try:
        with open(filename, "r") as f:
            old_hash = f.read()
    except FileNotFoundError:
        old_hash = ""

    # Compare hashes
    if new_hash != old_hash:
        updates.append(site)

    # Save the new hash for next run
    with open(filename, "w") as f:
        f.write(new_hash)

# ----------------------------
# SEND TELEGRAM MESSAGE
# ----------------------------

if updates:
    message = "🚨 Websites updated:\n" + "\n".join(updates)
else:
    message = f"✅ Bot ran at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. No updates."
    
send_telegram(message)
