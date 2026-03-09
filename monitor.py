import requests
import hashlib
import os

URL = "http://www.kt-so.com/"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def get_page_hash():
    r = requests.get(URL)
    content = r.text
    return hashlib.md5(content.encode()).hexdigest()


def main():
    new_hash = get_page_hash()

    try:
        with open("last_hash.txt", "r") as f:
            old_hash = f.read()
    except:
        old_hash = ""

    if new_hash != old_hash:
        send_telegram("🚨 Website updated!")

    with open("last_hash.txt", "w") as f:
        f.write(new_hash)


if __name__ == "__main__":
    main()
