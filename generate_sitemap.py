#!/usr/bin/env python3
"""
SA Bin Finder — Sitemap Generator
Reads enriched_stores.json and outputs sitemap.xml

Usage:
    python3 generate_sitemap.py

Output:
    sitemap.xml  (in same directory as this script)
"""

import json
import os
from urllib.parse import quote
from datetime import date

BASE_URL  = "https://sabinfinder.com"
TODAY     = date.today().isoformat()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH  = os.path.join(SCRIPT_DIR, "js", "enriched_stores.json")
OUT_PATH   = os.path.join(SCRIPT_DIR, "sitemap.xml")

# ---------------------------------------------------------------------------
# Load enriched store data
# ---------------------------------------------------------------------------
with open(JSON_PATH, encoding="utf-8") as f:
    stores = json.load(f)

# Build unique state slugs from data
def state_to_slug(name):
    return name.lower().replace(" ", "-")

states = sorted({state_to_slug(s["state"]) for s in stores if s.get("state")})

# ---------------------------------------------------------------------------
# Build URL entries
# ---------------------------------------------------------------------------
urls = []

def url_entry(loc, priority, changefreq="weekly"):
    return f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""

# Static pages
urls.append(url_entry(f"{BASE_URL}/",              "1.0", "weekly"))
urls.append(url_entry(f"{BASE_URL}/states.html",   "0.8", "monthly"))
urls.append(url_entry(f"{BASE_URL}/submit.html",   "0.4", "monthly"))

# State pages
for slug in states:
    urls.append(url_entry(
        f"{BASE_URL}/state.html?state={slug}",
        "0.8",
        "weekly"
    ))

# Store pages
for store in stores:
    pid = store.get("place_id", "")
    if not pid:
        continue
    encoded = quote(pid, safe="")
    urls.append(url_entry(
        f"{BASE_URL}/store.html?pid={encoded}",
        "0.6",
        "monthly"
    ))

# ---------------------------------------------------------------------------
# Write sitemap.xml
# ---------------------------------------------------------------------------
xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
xml_lines.extend(urls)
xml_lines.append("</urlset>")

sitemap = "\n".join(xml_lines)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"sitemap.xml generated: {len(urls)} URLs")
print(f"  Static pages : 3")
print(f"  State pages  : {len(states)}")
print(f"  Store pages  : {len(stores)}")
print(f"  Output       : {OUT_PATH}")
