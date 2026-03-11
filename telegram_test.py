import os
import requests

# Read secrets from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

    print("Status Code:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    
    # Debug checks
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN is missing")
    if not CHAT_ID:
        print("❌ CHAT_ID is missing")

    print("BOT_TOKEN loaded:", bool(BOT_TOKEN))
    print("CHAT_ID loaded:", bool(CHAT_ID))

    send_telegram("✅ Test message from GitHub Action bot")
