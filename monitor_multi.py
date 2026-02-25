import requests
import time
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ================================
# 🔑 PUT YOUR TELEGRAM DATA HERE
# ================================

HARDCODED_BOT_TOKEN = "8668770872:AAGU38d0xGm11lJzSsqD7dR1X_eprX86f7g"
HARDCODED_CHAT_ID = "1504540900"

# ================================

# Railway variables (if they exist)
ENV_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ENV_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Use Railway variable if available, otherwise fallback to hardcoded
TELEGRAM_BOT_TOKEN = ENV_BOT_TOKEN if ENV_BOT_TOKEN else HARDCODED_BOT_TOKEN
TELEGRAM_CHAT_ID = ENV_CHAT_ID if ENV_CHAT_ID else HARDCODED_CHAT_ID

CHECK_INTERVAL = 60
SEEN_FILE = "seen_multi.json"

URLS = [
    "https://oupi.eu/en/new-products",
    "https://oupi.eu/en/413-pre-order-one-piece",
    "https://4xtrading.eu/brand/one-piece",
    "https://threestonesgames.com/collections/one-piece-tcg",
    "https://infiniterealmtcg.com/collections/pre-order",
    "https://poke-power.eu/en/collections/one-piece-card-game",
    "https://tcgshop.eu/onepiece",
    "https://zadoys.at/collections/preorder-one-piece"
]

KEYWORDS = ["one piece"]
BLOCK_WORDS = ["sold out", "out of stock"]


# ---------------- TELEGRAM ---------------- #

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram still missing.")
        return

    print("Using BOT TOKEN:", TELEGRAM_BOT_TOKEN[:10], "...")
    print("Using CHAT ID:", TELEGRAM_CHAT_ID)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        r = requests.post(url, data=payload, timeout=15)
        print("Telegram response:", r.text)
    except Exception as e:
        print("Telegram error:", e)


# ---------------- STORAGE ---------------- #

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


# ---------------- FILTER ---------------- #

def contains_keywords(text):
    text = text.lower()
    if not any(keyword in text for keyword in KEYWORDS):
        return False
    if any(block in text for block in BLOCK_WORDS):
        return False
    return True


def looks_like_product_link(href):
    if not href:
        return False
    if href.startswith("#") or "javascript:" in href:
        return False
    return "/product" in href.lower() or "/products" in href.lower()


# ---------------- SCRAPER ---------------- #

def scan_site(url, seen, first_run=False):
    print(f"🔍 Scanning: {url}")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=25)

        if response.status_code != 200:
            print("Status:", response.status_code)
            return

        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all("a", href=True)

        for link in links:
            title = link.get_text(strip=True)
            href = link["href"]

            if not title or len(title) < 4:
                continue

            if not contains_keywords(title):
                continue

            if not looks_like_product_link(href):
                continue

            full_url = urljoin(url, href)

            if full_url in seen:
                continue

            if first_run:
                seen.add(full_url)
                continue

            print("✅ NEW PRODUCT:", title)

            message = (
                f"🔥 <b>New One Piece Product Found!</b>\n\n"
                f"<b>{title}</b>\n{full_url}"
            )

            send_telegram_message(message)
            seen.add(full_url)

    except Exception as e:
        print("Error:", e)


# ---------------- MAIN ---------------- #

def main():
    print("🚀 Bot starting...")
    print("ENV BOT:", ENV_BOT_TOKEN)
    print("ENV CHAT:", ENV_CHAT_ID)

    seen = load_seen()

    if not seen:
        print("⚠️ First run — storing products silently...")
        for url in URLS:
            scan_site(url, seen, first_run=True)
        save_seen(seen)
        print("✅ Initial store complete.")

    send_telegram_message("🤖 One Piece Monitor Bot is now running!")

    while True:
        for url in URLS:
            scan_site(url, seen)

        save_seen(seen)
        print("⏳ Sleeping 60 seconds...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

