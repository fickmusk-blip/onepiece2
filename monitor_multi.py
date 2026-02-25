import requests
import time
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CHECK_INTERVAL = 60  # seconds

URLS = [
    "https://threestonesgames.com",
    "https://oupi.eu",
    "https://4xtrading.eu",
    "https://oupi.eu/en/new-products",
    "https://infiniterealmtcg.com",
    "https://www.tf-robots.nl",
    "https://tcgshop.eu",
    "https://games-island.eu",
    "https://poke-power.eu",
    "https://zadoys.at",
    "https://playingcardshop.eu",
    "https://bazaarofmagic.eu",
    "https://totalcards.net",
    "https://tcgcorner.eu",
    "https://GameRoom.lt",
    "https://Padis-Store.com",
    "https://Yonko-TCG.de",
    "https://EuropeTCG.com",
    "https://BESCards.com",
    "https://Games-Island.eu",
    "https://FantasiaCards.de",
    "https://EvolutionTCG.com",
    "https://Spieltraum-shop.de",
    "https://Play-In.com",
    "https://FantasyWelt.de",
    "https://Spielwaren-Kontor24.de",
    "https://OtakuWorld.de",
    "https://Spielzeugwelten.de",
    "https://Pokecardsstore.it",
    "https://CrispyCards.de",
    "https://tcgshop-moers.eu",
    "https://oupi.eu/en/413-pre-order-one-piece",
    "https://4xtrading.eu/brand/one-piece",
    "https://threestonesgames.com/collections/one-piece-tcg",
    "https://infiniterealmtcg.com/collections/pre-order",
    "https://poke-power.eu/en/collections/one-piece-card-game",
    "https://tcgshop.eu/onepiece",
    "https://zadoys.at/collections/preorder-one-piece"
]

KEYWORDS = ["one piece", "pre-order", "preorder"]


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


def load_seen():
    try:
        with open("seen_multi.json", "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_seen(seen):
    with open("seen_multi.json", "w") as f:
        json.dump(list(seen), f)


def contains_keywords(text):
    text = text.lower()
    return any(keyword in text for keyword in KEYWORDS)


def scan_site(url, seen):
    print(f"Scanning: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "lxml")

        links = soup.find_all("a", href=True)

        for link in links:
            title = link.get_text(strip=True)
            href = link["href"]

            if not title:
                continue

            if contains_keywords(title):
                full_url = urljoin(url, href)

                if full_url not in seen:
                    print("NEW PRODUCT:", title)
                    message = f"🔥 <b>New One Piece Product Found!</b>\n\n<b>{title}</b>\n{full_url}"
                    send_telegram_message(message)
                    seen.add(full_url)

    except Exception as e:
        print(f"Error scanning {url}: {e}")


def main():
    seen = load_seen()
    print("Bot started...")

    while True:
        for url in URLS:
            scan_site(url, seen)

        save_seen(seen)
        print(f"Sleeping {CHECK_INTERVAL} seconds...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
