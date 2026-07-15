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
    "https://oupi.eu/en/new-products",
    "https://oupi.eu/en/413-pre-order-one-piece",
    "https://4xtrading.eu/brand/one-piece",
    "https://threestonesgames.com/collections/one-piece-tcg",
    "https://infinit
