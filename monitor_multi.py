import requests
import time
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ================================
# 🔑 DISCORD WEBHOOK
# ================================

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1526899002606489680/I8T1Hr0aIGldsmyls7S5PzRMM4NOsG7alLJseepTJkaQz5nnFi29aez1_Que8XJYZtQp"

# ================================

CHECK_INTERVAL = 60
SEEN_FILE = "seen_multi.json"

URLS = [
    # your URLs unchanged...
]

KEYWORDS = ["one piece"]
BLOCK_WORDS = ["sold out", "out of stock"]


# ---------------- DISCORD ---------------- #

def send_discord_message(message):
    if not DISCORD_WEBHOOK:
        print("❌ Discord webhook missing.")
        return

    payload = {
        "content": message
    }

    try:
        r = requests.post(DISCORD_WEBHOOK, json=payload, timeout=15)
        print("Discord response:", r.text)
    except Exception as e:
        print("Discord error:", e)


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
