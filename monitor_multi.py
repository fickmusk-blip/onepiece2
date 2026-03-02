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
"https://zadoys.at/collections/preorder-one-piece",
"https://www.playingcardshop.eu/one-piece.html",
"https://fantasiacards.de/en/collections/one-piece",
"https://cardcosmos.de/en-eu/collections/one-piece-karten-kaufen",
"https://www.escamon.de/collections/one-piece",
"https://yonko-tcg.de/collections/one-piece",
"https://games-island.eu/en/c/Card-Games/One-Piece-TCG",
"https://carteonepiece.com/en/pages/articles-en-precommandes",
"https://www.vendiloshop.it/en/10887-one-piece-tcg",
"https://pokecardsstore.it/en/collections/one-piece",
"https://otakura.com/en/collections/one-piece-card-game",
"https://teamrocketitalia.com/collections/one-piece",
"https://www.ilnuovomondoshop.it/en/trading-cards/one-piece-tcg",
"https://senpaimangashop.com/en/collections/one-piece-card-game-eng",
"https://fantasiastore.it/it/550-one-piece-card-game",
"https://www.primegame.it",
"https://www.inksouls.it/product-category/tcg-one-piece",
"https://www.gametrade.it/Category/One_Piece",
"https://www.monodejuegos.shop/categoria-producto/trading-cards/one-piece-trading-card-game",
"https://www.padis-store.com/en",
"https://masterofgames.es/en/67-one-piece",
"https://www.colossalstore.es/en/product-category/tcg/one-piece",
"https://templarsarena.com",
"https://bigcards.eu",
"https://baroncollections.fr/en/collections/one-piece-tcg-francais",
"https://www.poke-geek.fr/en/collections/one-piece",
"https://tcgmikaeru.com/collections/one-piece-fr",
"https://www.opecards.fr",
"https://ludotrotter.fr/categorie-produit/magasin/cartes/one-piece",
"https://maxireves.fr/selection-jeux/jeux-de-cartes-tcg/one-piece-tcg",
"https://www.cardshunter.fr/categorie-produit/autres-tcg/one-piece/one-piece-tcg-scelle",
"https://worldoftcg.fr",
"https://www.lerepairedudragon.fr",
"https://www.destocktcg.fr/jeux-de-cartes-a-collectionner/one-piece-card-game",
"https://reperegeek.fr/jeux-de-cartes/6342-one-piece-tcg-premium-card-collection-bandai-card-games-fest-23-24-edition.html",
"https://www.ultrajeux.fr",
"https://co-lector.fr",
"https://www.trader-online.de/One-Piece-Card-Game",
"https://www.gate-to-the-games.de/One-Piece-Card-Game",
"https://www.fantasywelt.de/One-Piece-Card-Game",
"https://www.kutami.de/One-Piece-Card-Game",
"https://www.philibertnet.com/en/15080-one-piece-card-game",
"https://www.parkage.com/en/one-piece-card-game",
"https://www.bazaarofmagic.eu/en-WW/c/one-piece-card-game",
"https://www.spellenwinkel.nl/nl-NL/c-5781251/one-piece-card-game",
"https://www.alphaspel.se/one-piece-card-game",
"https://www.lautapelit.fi/category/444/one-piece-card-game",
"https://www.poromagia.com/en/catalogue/one-piece-card-game_2019",
"https://www.mysticgames.be/en/one-piece-card-game",
"https://www.goblintrader.es/en/87-one-piece-card-game",
"https://www.dungeonmarvels.com/en/one-piece-card-game",
"https://www.tcgcorner.at/collections/one-piece",
"https://spielraum.co.at/collections/one-piece",
"https://www.bazaarofmagic.eu/en/one-piece-tcg",
"https://merchversum.de/produkt-kategorie/trading-cards/one-piece",
"https://comicgalerie.at/collections/one-piece",
"https://www.cardmarket.com/en/OnePiece",
"https://www.cardgame-club.de/collections/one-piece",
"https://www.cardicuno.de/collections/one-piece",
"https://www.cardstore.at/collections/one-piece",
"https://www.cardgamefactory.de/collections/one-piece",
"https://www.cardgame-shop.eu/one-piece",
"https://www.kartenwelt.at/collections/one-piece",
"https://www.carduniverse.eu/collections/one-piece",
"https://www.cardcollector.de/collections/one-piece",
"https://www.cardstorefrance.fr/collections/one-piece",
"https://www.tf-robots.nl/en_GB/c-7113482/one-piece-tcg",
"https://card-binder.com/pages/one-piece-trading-card-game-tcg-shop",
"https://aquitaz.se/en/collections/one-piece-trading-card-game",
"https://onepiece-cards.com/en",
"https://gamersheaven.de/one-piece-tcg",
"https://jk-events.de/en/One-Piece-Card-Game",
"https://baruzcard.it/collections/one-piece",
"https://www.onytcg.it/en-us",
"https://www.azcardtrading.it/collections/one-piece-trading-card-game",
"https://akatsukianime.com/en/product-category/trading-cards/one-piece-tcg",
"https://www.lastlevel.es/distribucion/juegos-cartas-piece-c-331_2108.html",
"https://www.spellenwinkel.nl/en-WW/c/one-piece-tcg/1000538",
"https://cardstore.nl/en/collections/one-piece",
"https://www.tcgcenter.nl/en/67-one-piece-tcg",
"https://www.coolcard.se/en/category/one-piece-card-game-2"  
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





