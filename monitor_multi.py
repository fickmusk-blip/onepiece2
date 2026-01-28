import requests
import time
import json
import os
import hashlib

# === CONFIG ===
TOKEN = "7661547464:AAHCLqjOTDlgPRqSFIvL84r613XALAwE_1A"
CHAT_ID = "429753902"

# Shops to monitor
SHOPS = [
    "threestonesgames.com",
    "oupi.eu",
    "4xtrading.eu",
    "infiniterealmtcg.com",
    "www.tf-robots.nl",
    "tcgshop.eu",
    "games-island.eu",
    "poke-power.eu",
    "zadoys.at",
    "playingcardshop.eu",
    "bazaarofmagic.eu",
    "totalcards.net",
    "tcgcorner.eu",
    "GameRoom.lt",
    "Padis-Store.com",
    "Yonko-TCG.de",
    "EuropeTCG.com",
    "BESCards.com",
    "Games-Island.eu",
    "FantasiaCards.de",
    "EvolutionTCG.com",
    "Spieltraum-shop.de",
    "Play-In.com",
    "FantasyWelt.de",
    "Spielwaren-Kontor24.de",
    "OtakuWorld.de",
    "Spielzeugwelten.de",
    "Pokecardsstore.it",
    "CrispyCards.de",
    "tcgshop-moers.eu",
    "https://oupi.eu/en/413-pre-order-one-piece",
    "https://4xtrading.eu/brand/one-piece",
    "https://threestonesgames.com/collections/one-piece-tcg",
    "https://infiniterealmtcg.com/collections/pre-order",
    "https://www.tf-robots.nl/de_DE/c-7151954/one-piece-dragon-ball-pokemon-lorcana-and-other-tcg/?filter=W3sibGVmdE9wZXJhbmQiOnsidHlwZSI6IkZJTFRFUiIsInZhbHVlIjoiMGFjY2VjOGEtZmFhNy00OGNiLTgwMTYtM2VhNzk5N2JkOThjIn0sIm9wZXJhdG9yIjoiSU4iLCJyaWdodE9wZXJhbmQiOnsidHlwZSI6IlNDQUxBUiIsInZhbHVlcyI6WyIyMTk1NjAiXX19XQ%3D%3D"
]

CHECK_EVERY = 60  # seconds (1 minutes)

# Load persistent state
if os.path.exists("seen_multi.json"):
    with open("seen_multi.json", "r") as f:
        seen_state = json.load(f)
else:
    seen_state = {}

# Initialize state for each shop
for shop in SHOPS:
    seen_state.setdefault(shop, {"ids": [], "hash": ""})

def notify(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg,
        "disable_web_page_preview": True
    })

def hash_content(text):
    return hashlib.md5(text.encode()).hexdigest()

notify("📡 Multi-shop TCG monitor started")

print("Monitor running...")

while True:
    for shop in SHOPS:
        base = f"https://{shop}"
        json_url = base + "/products.json"

        try:
            # Try Shopify JSON API first
            r = requests.get(json_url, timeout=10)
            data = r.json()

            if "products" in data:
                current_ids = [p["id"] for p in data["products"]]
                new_items = [p for p in data["products"] if p["id"] not in seen_state[shop]["ids"]]

                for p in new_items:
                    title = p.get("title", "")
                    handle = p.get("handle", "")
                    # Filter for One Piece only
                    if "one piece" in title.lower():
                        notify(f"🛒 {shop} NEW: {title}\n{base}/products/{handle}")

                seen_state[shop]["ids"] = current_ids
            else:
                raise ValueError("No products key")

        except Exception:
            # Fallback: HTML hash detection
            try:
                html = requests.get(base, timeout=10).text
                current_hash = hash_content(html)
                if seen_state[shop]["hash"] and current_hash != seen_state[shop]["hash"]:
                    notify(f"🆕 CHANGE DETECTED on {shop}")
                seen_state[shop]["hash"] = current_hash
            except Exception as e:
                print(f"Error fetching {shop}: {e}")

    # Save state to disk
    with open("seen_multi.json", "w") as f:
        json.dump(seen_state, f)

    time.sleep(CHECK_EVERY)







