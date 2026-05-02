#!/usr/bin/env python3
"""
Generate static HTML store detail pages for Donation Center Finder.

Why this exists:
- store.html is a JavaScript-rendered shell.
- Crawlers that do not execute JavaScript see weak/empty store pages.
- This script pre-generates one crawlable HTML page per store from
  js/enriched_stores_clean.json, plus crawlable directory pages.

Features:
- Individual store pages (1,181+ pages)
- State-level landing pages (50 pages)
- City-level landing pages (top 50 cities)
- All Locations hub page
- Sitemap.xml and robots.txt

Run:
    python3 generate_static_stores.py
"""

import json
import re
import html
from pathlib import Path
from datetime import date
from urllib.parse import quote
from collections import defaultdict

# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://donationcenterfinder.com"
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "js" / "enriched_stores_clean.json"
STORES_DIR = ROOT / "stores"
STATES_DIR = ROOT / "states"
CITIES_DIR = ROOT / "cities"
SITEMAP_PATH = ROOT / "sitemap.xml"
STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/thrift-stores", "0.9", "weekly"),
    ("/food-pantries", "0.9", "weekly"),
    ("/rehab-centers", "0.9", "weekly"),
    ("/submit", "0.4", "monthly"),
]

STATE_SLUGS = {
    "Alabama": "alabama", "Alaska": "alaska", "Arizona": "arizona", "Arkansas": "arkansas",
    "California": "california", "Colorado": "colorado", "Connecticut": "connecticut", "Delaware": "delaware",
    "Florida": "florida", "Georgia": "georgia", "Hawaii": "hawaii", "Idaho": "idaho",
    "Illinois": "illinois", "Indiana": "indiana", "Iowa": "iowa", "Kansas": "kansas",
    "Kentucky": "kentucky", "Louisiana": "louisiana", "Maine": "maine", "Maryland": "maryland",
    "Massachusetts": "massachusetts", "Michigan": "michigan", "Minnesota": "minnesota", "Mississippi": "mississippi",
    "Missouri": "missouri", "Montana": "montana", "Nebraska": "nebraska", "Nevada": "nevada",
    "New Hampshire": "new-hampshire", "New Jersey": "new-jersey", "New Mexico": "new-mexico", "New York": "new-york",
    "North Carolina": "north-carolina", "North Dakota": "north-dakota", "Ohio": "ohio", "Oklahoma": "oklahoma",
    "Oregon": "oregon", "Pennsylvania": "pennsylvania", "Rhode Island": "rhode-island", "South Carolina": "south-carolina",
    "South Dakota": "south-dakota", "Tennessee": "tennessee", "Texas": "texas", "Utah": "utah",
    "Vermont": "vermont", "Virginia": "virginia", "Washington": "washington", "West Virginia": "west-virginia",
    "Wisconsin": "wisconsin", "Wyoming": "wyoming",
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def truncate_title(title, max_length=60):
    """Return title as-is - no truncation needed"""
    return title

def clean_canonical_url(url):
    """Ensure canonical URL has no trailing slash - clean URLs only"""
    if not url:
        return url
    
    # Only remove trailing slash
    if url.endswith('/') and url != '/':
        url = url[:-1]
    
    return url

def esc(value):
    return html.escape(str(value or ""), quote=True)

def slugify(value):
    value = str(value or "").lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "store"

def short_id(store):
    pid = str(store.get("place_id") or store.get("id") or "")
    compact = re.sub(r"[^a-zA-Z0-9]", "", pid)
    return compact[-8:] if len(compact) >= 8 else compact

def store_slug(store):
    base = " ".join(
        str(part) for part in [
            store.get("name"),
            store.get("city"),
            store.get("state_abbr") or store.get("state"),
            store.get("zip"),
        ] if part
    )
    suffix = short_id(store)
    return f"{slugify(base)}-{suffix}" if suffix else slugify(base)

def store_path(store):
    return f"/stores/{store_slug(store)}"

def state_slug(state_name):
    return STATE_SLUGS.get(state_name, slugify(state_name))

def city_slug(city, state_abbr):
    """Create SEO-friendly slug for city pages"""
    base = f"{city}-{state_abbr}".lower()
    base = base.replace(" ", "-")
    base = re.sub(r"[^a-z0-9-]", "", base)
    return base

def category_label(category):
    return {
        "thrift": "Thrift Store & Donation Center",
        "food": "Food Pantry",
        "rehab": "Rehabilitation Center",
    }.get(str(category or "").lower(), "Donation Center")

# ============================================================
# IMAGE FUNCTIONS (FROM WORKING SCRIPT - MERGED)
# ============================================================

def placeholder_image(store):
    category = str(store.get("category") or "").lower()
    if category == "food":
        return "../images/placeholder-food.jpg"
    if category == "rehab":
        return "../images/placeholder-rehab.jpg"
    return "../images/placeholder-thrift.jpg"

def display_image(store):
    """Display store image - prioritizes Google Photos URLs, then local images"""
    photo = str(store.get("photo") or "")
    
    # Case 1: Full HTTP/HTTPS URL (Google Photos, etc.)
    if photo.startswith("http"):
        return photo
    
    # Case 2: Relative path starting with images/
    if photo.startswith("images/"):
        return "../" + photo
    
    # Case 3: Absolute path starting with /images/
    if photo.startswith("/images/"):
        return ".." + photo
    
    # Case 4: No valid image found - use placeholder
    return placeholder_image(store)
def schema_image(store):
    """For JSON-LD structured data - uses absolute URLs"""
    photo = str(store.get("photo") or "")
    if photo.startswith("images/"):
        return BASE_URL + "/" + photo
    if photo.startswith("/images/"):
        return BASE_URL + photo

    category = str(store.get("category") or "").lower()
    if category == "food":
        return BASE_URL + "/images/placeholder-food.jpg"
    if category == "rehab":
        return BASE_URL + "/images/placeholder-rehab.jpg"
    return BASE_URL + "/images/placeholder-thrift.jpg"

# ============================================================
# HOURS & RATING FUNCTIONS
# testing
# ============================================================

def split_hours(working_hours):
    if not working_hours:
        return []
    rows = []
    for entry in str(working_hours).split("|"):
        entry = entry.strip()
        if not entry:
            continue
        if ":" in entry:
            day, hours = entry.split(":", 1)
            rows.append((day.strip(), hours.strip()))
        else:
            parts = [p.strip() for p in entry.split(",")]
            if len(parts) >= 2:
                open_time = parts[1]
                close_time = parts[2] if len(parts) > 2 else ""
                rows.append((parts[0], f"{open_time} – {close_time}" if close_time else open_time))
    return rows

def hours_html(store):
    rows = split_hours(store.get("working_hours") or store.get("working_hours_csv"))
    if not rows:
        return ""
    body = "\n".join(
        f'              <div class="hours-day">{esc(day)}</div><div class="hours-time">{esc(hours)}</div>'
        for day, hours in rows
    )
    return f"""
          <div class="detail-section">
            <div class="detail-section-title">Hours</div>
            <div class="hours-grid">
{body}
            </div>
          </div>"""

def rating_html(store):
    try:
        rating = float(store.get("rating") or 0)
    except (TypeError, ValueError):
        rating = 0
    try:
        reviews = int(store.get("review_count") or 0)
    except (TypeError, ValueError):
        reviews = 0
    if rating <= 0:
        return ""
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = max(0, 5 - full - half)
    stars = '<span class="stars-row">' + \
        '<span class="star-f">★</span>' * full + \
        ('<span class="star-h">★</span>' if half else '') + \
        '<span class="star-e">★</span>' * empty + \
        '</span>'
    return f"""
              <div class="detail-rating">
                {stars}
                <span class="detail-rating-num">{rating:.1f}</span>
                <span class="detail-rating-cnt">&nbsp;({reviews:,} Google reviews)</span>
              </div>"""

# ============================================================
# JSON-LD STRUCTURED DATA
# ============================================================

def json_ld(store):
    path = store_path(store)
    
    # Clean the store name - remove prefixes
    store_name = store.get("name") or ""
    prefixes_to_remove = [
        "The Salvation Army - ",
        "The Salvation Army ",
        "Salvation Army - ",
        "Salvation Army ",
        "The Salvation Army's ",
    ]
    for prefix in prefixes_to_remove:
        if store_name.startswith(prefix):
            store_name = store_name[len(prefix):]
            break
    
    # Remove suffixes
    store_name = store_name.replace(" — Donation Center", "")
    store_name = store_name.replace(" — Thrift Store", "")
    store_name = store_name.replace(" — Food Pantry", "")
    store_name = store_name.replace(" - Donation Center", "")
    store_name = store_name.replace(" - Thrift Store", "")
    store_name = store_name.replace(" - Food Pantry", "")
    
    schema = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "Store"],
        "name": store_name,
        "url": BASE_URL + path,
        "image": schema_image(store),
        "telephone": store.get("phone"),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": store.get("street") or store.get("address"),
            "addressLocality": store.get("city"),
            "addressRegion": store.get("state_abbr") or store.get("state"),
            "postalCode": store.get("zip"),
            "addressCountry": "US",
        },
    }
    try:
        rating = float(store.get("rating") or 0)
        reviews = int(store.get("review_count") or 0)
        if rating > 0 and reviews > 0:
            schema["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": f"{rating:.1f}",
                "reviewCount": reviews,
            }
    except (TypeError, ValueError):
        pass

    hours_specs = []
    for day, hours in split_hours(store.get("working_hours")):
        if hours and "closed" not in hours.lower():
            hours_specs.append({
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": day,
                "description": hours,
            })
    if hours_specs:
        schema["openingHoursSpecification"] = hours_specs

    schema = {k: v for k, v in schema.items() if v}
    if "address" in schema:
        schema["address"] = {k: v for k, v in schema["address"].items() if v}
    return json.dumps(schema, ensure_ascii=False, separators=(",", ":"))

# ============================================================
# PAGE SHELL (MASTER TEMPLATE)
# ============================================================

def page_shell(title, description, canonical_path, body, extra_head=""):
    if not canonical_path.startswith('/'):
        canonical_path = '/' + canonical_path
    
    canonical = clean_canonical_url(BASE_URL + canonical_path)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(truncate_title(title))}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Donation Center Finder">
  <meta property="og:title" content="{esc(truncate_title(title))}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{BASE_URL}/images/og-home.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="../css/styles.css">
{extra_head}</head>
<body>
  <nav class="nav">
    <div class="container">
      <div class="nav-inner">
        <a href="{BASE_URL}/" class="nav-logo"><div class="nav-logo-icon">DC</div><span>Donation Center Finder</span></a>
        <ul class="nav-links">
          <li><a href="{BASE_URL}/">Home</a></li>
          <li><a href="{BASE_URL}/thrift-stores">Thrift Stores</a></li>
          <li><a href="{BASE_URL}/food-pantries">Food Pantries</a></li>
          <li><a href="{BASE_URL}/rehab-centers">Rehab Centers</a></li>
          <li><a href="{BASE_URL}/states/">States</a></li>
          <li><a href="{BASE_URL}/cities/">Top Cities</a></li>
          <li><a href="{BASE_URL}/all-locations">All Locations</a></li>
        </ul>
      </div>
    </div>
  </nav>

{body}

   <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="{BASE_URL}/" class="footer-logo">
            <div class="nav-logo-icon">DC</div>
            <span>Donation Center Finder</span>
          </a>
          <p>
            The #1 community directory for donation centers — thrift stores,
            food pantries, and rehabilitation centers — across all 50 states.
            Free, always.
          </p>
        </div>

        <div class="footer-column">
          <h3>Services</h3>
          <ul>
            <li><a href="{BASE_URL}/thrift-stores">Thrift &amp; Donation Stores</a></li>
            <li><a href="{BASE_URL}/food-pantries">Food Pantries</a></li>
            <li><a href="{BASE_URL}/rehab-centers">Rehabilitation Centers</a></li>
            <li><a href="{BASE_URL}/states/">Browse All States</a></li>
            <li><a href="{BASE_URL}/cities/">Top Cities</a></li>
            <li><a href="{BASE_URL}/submit">Submit a Location</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h3>Popular States</h3>
          <ul>
            <li><a href="{BASE_URL}/states/california">California</a></li>
            <li><a href="{BASE_URL}/states/texas">Texas</a></li>
            <li><a href="{BASE_URL}/states/florida">Florida</a></li>
            <li><a href="{BASE_URL}/states/new-york">New York</a></li>
            <li><a href="{BASE_URL}/states/illinois">Illinois</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2025 Donation Center Finder — Community-powered directory. Not affiliated with The Salvation Army.</p>
      </div>
    </div>
  </footer>
</body>
</html>
"""

# ============================================================
# STORE PAGE RENDERER
# ============================================================
def render_store_page(store):
    path = store_path(store)
    state = store.get("state") or ""
    state_link = f"/states/{state_slug(state)}"
    city = store.get("city") or ""
    category = category_label(store.get("category"))
    
    # Clean the store name - remove prefixes
    store_name = store.get('name') or ""
    prefixes_to_remove = [
        "The Salvation Army - ",
        "The Salvation Army ",
        "Salvation Army - ",
        "Salvation Army ",
        "The Salvation Army's ",
    ]
    for prefix in prefixes_to_remove:
        if store_name.startswith(prefix):
            store_name = store_name[len(prefix):]
            break
    
    # Remove suffixes
    store_name = store_name.replace(" — Donation Center", "")
    store_name = store_name.replace(" — Thrift Store", "")
    store_name = store_name.replace(" — Food Pantry", "")
    store_name = store_name.replace(" - Donation Center", "")
    store_name = store_name.replace(" - Thrift Store", "")
    store_name = store_name.replace(" - Food Pantry", "")
    
    # Create clean title - FIXED INDENTATION
    if store_name and city and state:
        raw_title = f"{store_name}, {city}, {state}"
    elif store_name:
        raw_title = store_name
    else:
        raw_title = f"{city}, {state}"
    
    title = truncate_title(raw_title, 60)
    
    rating_snippet = ""
    try:
        rating = float(store.get("rating") or 0)
        reviews = int(store.get("review_count") or 0)
        if rating > 0:
            rating_snippet = f" Rated {rating:.1f}/5 by {reviews:,} reviewers."
    except (TypeError, ValueError):
        pass
    
    description = (
        f"Visit {store_name} in {city}, {state}."
        f"{rating_snippet} Get address, phone number, hours, directions, and service details."
    )[:155]

    website = store.get("website")
    phone = store.get("phone")
    maps = store.get("location_link")
    street = store.get("street") or store.get("address") or ""
    address_line = f"{street}, {city}, {store.get('state_abbr') or state} {store.get('zip') or ''}".strip()
    img = display_image(store)

    body = f"""  <div class="page-header">
    <div class="container">
      <div class="breadcrumb">
        <a href="{BASE_URL}/">Home</a>
        <span class="sep">›</span>
        <a href="{BASE_URL}/states/">States</a>
        <span class="sep">›</span>
        <a href="{BASE_URL}{state_link}">{esc(state)}</a>
        <span class="sep">›</span>
        <span>{esc(store_name)}</span>
      </div>
    </div>
  </div>

  <main class="store-detail">
    <div class="container">
      <div class="store-detail-card">
        <div class="store-detail-photo"><img src="{esc(img)}" alt="{esc(store_name)}" loading="eager"></div>
        <div class="store-detail-header">
          <div class="store-detail-logo">SA</div>
          <div class="store-detail-title">
            <h1>{esc(store_name)}</h1>
            <div class="city-state">{esc(city)}, {esc(state)} {esc(store.get('zip'))}</div>
            {rating_html(store)}
          </div>
        </div>
        <div class="store-detail-body">
          <div class="detail-section">
            <div class="detail-section-title">Contact &amp; Location</div>
            <div class="info-row"><span class="icon">📍</span><span>{esc(address_line)}</span></div>
            {f'<div class="info-row"><span class="icon">📞</span><a href="tel:{esc(phone)}">{esc(phone)}</a></div>' if phone else ''}
            {f'<div class="info-row"><span class="icon">🌐</span><a href="{esc(website)}" target="_blank" rel="noopener nofollow">{esc(re.sub(r"^https?://", "", website).rstrip("/"))}</a></div>' if website else ''}
            {f'<div style="margin-top:12px;"><a href="{esc(maps)}" target="_blank" rel="noopener nofollow" class="btn btn-outline">🗺️ View on Google Maps</a></div>' if maps else ''}
          </div>

{hours_html(store)}

          <div class="detail-section">
            <div class="detail-section-title">Service Type</div>
            <span class="tag" style="font-size:0.95rem;">{esc(category)}</span>
          </div>

          <div class="detail-section">
            <div class="detail-section-title">About This Location</div>
            <p style="color:var(--muted); font-size:0.95rem;">
              {esc(store_name)} is listed in our directory as a {esc(category.lower())}
              serving {esc(city)}, {esc(state)}. Use the contact details above to confirm current hours,
              donation guidelines, services, and availability before visiting.
            </p>
          </div>

          <div style="text-align:center; padding-top:8px; font-size:0.83rem; color:var(--muted);">
            <a href="{BASE_URL}/submit" style="color:var(--muted);">✏️ Suggest a correction</a>
          </div>
        </div>
      </div>
      <p style="margin-top:20px;"><a href="{BASE_URL}{state_link}" class="btn btn-outline">← All {esc(state)} stores</a> <a href="{BASE_URL}/all-locations" class="btn btn-outline">All locations</a></p>
    </div>
  </main>
"""
    extra_head = f'  <script type="application/ld+json">{json_ld(store)}</script>\n'
    return page_shell(title, description, path, body, extra_head)
# ============================================================
# STORES INDEX PAGE
# ============================================================

def render_stores_index_page(stores):
    by_state = {}
    for store in stores:
        by_state.setdefault(store.get("state") or "Other", []).append(store)

    sections = []
    for state in sorted(by_state):
        links = "\n".join(
            f'          <li><a href="{esc(store_path(s))}">{esc(s.get("name"))}</a> <span style="color:var(--muted);">— {esc(s.get("city"))}, {esc(s.get("state_abbr") or s.get("state"))}</span></li>'
            for s in sorted(by_state[state], key=lambda x: (x.get("city") or "", x.get("name") or ""))
        )
        sections.append(f"""
      <div class="detail-section">
        <div class="detail-section-title">{esc(state)} Donation Centers</div>
        <ul style="columns:2; line-height:1.8; padding-left:20px;">
{links}
        </ul>
      </div>""")

    body = f"""  <main class="section">
    <div class="container">
      <h1 class="section-title">All Donation Center Locations</h1>
      <p class="section-subtitle">Browse all {len(stores):,} donation center location pages by state, including thrift stores, food pantries, and rehabilitation centers.</p>
      {''.join(sections)}
    </div>
  </main>
"""
    return page_shell(
        "All Donation Center Locations | Donation Center Finder",
        f"Browse all {len(stores):,} donation center location pages by state.",
        "/stores",
        body
    )

# ============================================================
# STATE PAGES
# ============================================================

def render_state_page(state_name, state_stores):
    slug = state_slug(state_name)
    state_link = f"/states/{slug}"
    
    sorted_stores = sorted(state_stores, key=lambda x: (x.get("city") or "", x.get("name") or ""))
    
    stores_html = ""
    for store in sorted_stores:
        stores_html += f"""
          <li style="margin-bottom: 8px;">
            <a href="{BASE_URL}{store_path(store)}">{esc(store.get('name'))}</a>
            <span style="color:var(--muted); font-size:0.85rem;"> — {esc(store.get('city'))}, {esc(store.get('zip'))}</span>
          </li>"""
    
    body = f"""  <div class="page-header">
    <div class="container">
      <div class="breadcrumb">
        <a href="{BASE_URL}/">Home</a>
        <span class="sep">›</span>
        <a href="{BASE_URL}/states/">States</a>
        <span class="sep">›</span>
        <span>{esc(state_name)}</span>
      </div>
      <h1>{esc(state_name)} Donation Centers</h1>
      <p>Find thrift stores, food pantries, and rehabilitation centers in {esc(state_name)}.</p>
    </div>
  </div>

  <main class="section">
    <div class="container">
      <div class="detail-section">
        <div class="detail-section-title">All Locations in {esc(state_name)} ({len(state_stores)} stores)</div>
        <ul style="columns:2; line-height:1.8; padding-left:20px;">
{stores_html}
        </ul>
      </div>
      <p style="margin-top:20px;"><a href="{BASE_URL}/states/" class="btn btn-outline">← Back to all states</a></p>
    </div>
  </main>
"""
    
    title = f"{state_name} Donation Centers | Thrift Stores & Food Pantries"
    description = f"Browse {len(state_stores)} donation centers in {state_name}, including Salvation Army thrift stores, food pantries, and rehabilitation centers."
    
    return page_shell(title, description, state_link, body)

def render_states_index_page(stores):
    by_state = defaultdict(list)
    for store in stores:
        state = store.get("state")
        if state:
            by_state[state].append(store)
    
    states_html = ""
    for state_name in sorted(by_state.keys()):
        slug = state_slug(state_name)
        count = len(by_state[state_name])
        states_html += f"""
          <li style="margin-bottom: 12px;">
           <a href="{BASE_URL}/states/{slug}" style="font-weight:600;">{esc(state_name)}</a>
            <span style="color:var(--muted); font-size:0.85rem;"> ({count} locations)</span>
          </li>"""
    
    body = f"""  <div class="page-header">
    <div class="container">
      <div class="breadcrumb">
        <a href="{BASE_URL}/">Home</a>
        <span class="sep">›</span>
        <span>States</span>
      </div>
      <h1>All States Directory</h1>
      <p>Browse donation centers by state across the United States.</p>
    </div>
  </div>

  <main class="section">
    <div class="container">
      <div class="detail-section">
        <div class="detail-section-title">Select a State</div>
        <ul style="columns:3; line-height:1.8; padding-left:20px;">
{states_html}
        </ul>
      </div>
    </div>
  </main>
"""
    
    title = "All States Directory | Donation Center Locations by State"
    description = "Browse donation centers in all 50 states. Find Salvation Army thrift stores, food pantries, and rehabilitation centers near you."
    
    return page_shell(title, description, "/states/", body)

# ============================================================
# CITY PAGES (TOP 50)
# ============================================================

def get_top_cities(stores, limit=50):
    """Get top 50 cities by number of stores"""
    city_count = defaultdict(int)
    city_data = {}
    
    for store in stores:
        city = store.get("city")
        state = store.get("state")
        state_abbr = store.get("state_abbr")
        
        if not state_abbr and state:
            state_abbr = state[:2].upper()
        
        if city and state:
            key = f"{city}|{state}"
            city_count[key] += 1
            
            if key not in city_data:
                city_data[key] = {
                    "city": city,
                    "state": state,
                    "state_abbr": state_abbr,
                    "slug": city_slug(city, state_abbr),
                    "stores": []
                }
    
    top_cities = sorted(city_count.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    for key, _ in top_cities:
        city_key, state = key.split("|")
        city_info = city_data[key]
        
        for store in stores:
            if store.get("city") == city_key and store.get("state") == state:
                city_info["stores"].append(store)
    
    return [city_data[key] for key, _ in top_cities]

def render_city_page(city_info):
    city = city_info["city"]
    state = city_info["state"]
    state_abbr = city_info["state_abbr"]
    stores = city_info["stores"]
    city_slug_name = city_info["slug"]
    
    title = f"Donation Centers in {city}, {state_abbr} | Thrift Stores & Food Pantries"
    description = f"Find {len(stores)} donation centers in {city}, {state_abbr}. Locations include Salvation Army thrift stores, food pantries, and rehabilitation centers."
    
    stores_html = ""
    for store in sorted(stores, key=lambda x: x.get("name", "")):
        rating_stars = ""
        try:
            rating = float(store.get("rating") or 0)
            if rating > 0:
                full = int(rating)
                rating_stars = f'<span class="stars-row">{"★" * full}{"☆" * (5-full)}</span> <span class="rating-num">{rating:.1f}</span>'
        except:
            pass
        
        stores_html += f"""
          <div class="city-store-item">
            <h3><a href="{BASE_URL}{store_path(store)}">{esc(store.get('name'))}</a></h3>
            <div class="city-store-address">{esc(store.get('address') or store.get('street') or '')}</div>
            {f'<div class="city-store-phone">📞 {esc(store.get("phone"))}</div>' if store.get("phone") else ''}
            <div class="city-store-rating">{rating_stars}</div>
            <a href="{BASE_URL}{store_path(store)}" class="btn-details">View Details →</a>
          </div>
          <hr class="store-divider">"""
    
    body = f"""  <div class="page-header">
    <div class="container">
      <div class="breadcrumb">
        <a href="{BASE_URL}/">Home</a>
        <span class="sep">›</span>
        <a href="{BASE_URL}/states/">States</a>
        <span class="sep">›</span>
        <a href="{BASE_URL}/states/{state_slug(state)}">{esc(state)}</a>
        <span class="sep">›</span>
        <span>{esc(city)}</span>
      </div>
      <h1>Donation Centers in {esc(city)}, {esc(state_abbr)}</h1>
      <p>Browse {len(stores)} donation centers including thrift stores, food pantries, and rehabilitation centers in {esc(city)}.</p>
    </div>
  </div>

  <main class="city-page">
    <div class="container">
      <div class="city-stats">
        <div class="stat-box"><div class="stat-number">{len(stores)}</div><div class="stat-label">Donation Centers</div></div>
        <div class="stat-box"><div class="stat-number">{len([s for s in stores if s.get('category') == 'thrift'])}</div><div class="stat-label">Thrift Stores</div></div>
        <div class="stat-box"><div class="stat-number">{len([s for s in stores if s.get('category') == 'food'])}</div><div class="stat-label">Food Pantries</div></div>
        <div class="stat-box"><div class="stat-number">{len([s for s in stores if s.get('category') == 'rehab'])}</div><div class="stat-label">Rehab Centers</div></div>
      </div>
      
      <div class="city-stores-list">
        <h2>All Donation Centers in {esc(city)}, {esc(state_abbr)}</h2>
        {stores_html if stores_html else '<p>No stores found in this city.</p>'}
      </div>
      
      <div class="city-nearby">
        <h3>Explore More Locations</h3>
        <p><a href="{BASE_URL}/states/{state_slug(state)}">View all {esc(state)} donation centers</a> | <a href="{BASE_URL}/states/">Browse all states</a> | <a href="{BASE_URL}/cities/">View top cities</a></p>
      </div>
    </div>
  </main>
"""
    
    extra_head = """
  <style>
    .city-stats { display: flex; gap: 20px; margin: 30px 0; justify-content: center; flex-wrap: wrap; }
    .stat-box { background: var(--navy); color: white; padding: 20px 30px; border-radius: 12px; text-align: center; min-width: 120px; }
    .stat-number { font-size: 2rem; font-weight: 800; }
    .stat-label { font-size: 0.85rem; opacity: 0.8; }
    .city-store-item { margin: 25px 0; padding: 20px; background: var(--white); border-radius: 8px; box-shadow: var(--shadow-sm); }
    .city-store-item h3 { margin: 0 0 8px 0; }
    .city-store-item h3 a { color: var(--navy); text-decoration: none; }
    .city-store-item h3 a:hover { color: var(--red); }
    .city-store-address { color: var(--muted); margin-bottom: 8px; }
    .city-store-phone { margin-bottom: 8px; }
    .btn-details { display: inline-block; margin-top: 10px; color: var(--red); text-decoration: none; font-weight: 600; }
    .store-divider { margin: 20px 0; border: none; border-top: 1px solid var(--border); }
    .city-nearby { margin-top: 40px; padding: 20px; background: var(--area); border-radius: 8px; text-align: center; }
    @media (max-width: 768px) { .city-stats { flex-direction: column; align-items: center; } }
  </style>
"""
    
    return page_shell(title, description, f"/cities/{city_slug_name}", body, extra_head)

def generate_city_pages(stores, limit=50):
    top_cities = get_top_cities(stores, limit)
    CITIES_DIR.mkdir(exist_ok=True)
    
    for city_info in top_cities:
        slug = city_info["slug"]
        city_file = CITIES_DIR / f"{slug}.html"
        city_file.write_text(render_city_page(city_info), encoding="utf-8")
        print(f"  ✅ Generated city page: cities/{slug}.html ({len(city_info['stores'])} stores)")
    
    # Generate cities index page
    cities_index_html = """  <div class="page-header"><div class="container"><div class="breadcrumb"><a href="{BASE_URL}/">Home</a><span class="sep">›</span><span>Top Cities</span></div><h1>Top US Cities for Donation Centers</h1><p>Find donation centers in America's largest cities.</p></div></div>
  <main class="section"><div class="container"><div class="cities-grid">"""
    
    for city_info in top_cities:
        cities_index_html += f"""
        <div class="city-card"><a href="{BASE_URL}/cities/{city_info['slug']}"><h3>{esc(city_info['city'])}, {esc(city_info['state_abbr'])}</h3><p>{len(city_info['stores'])} donation centers</p><span class="city-card-link">View Centers →</span></a></div>"""
    
    cities_index_html += """</div><p style="text-align:center;margin-top:40px;"><a href="{BASE_URL}/states/" class="btn btn-outline">Browse by State</a> <a href="{BASE_URL}/stores/" class="btn btn-outline">View All Locations</a></p></div></main>
  <style>.cities-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;margin-top:30px;}.city-card{background:var(--white);border-radius:12px;padding:24px;text-align:center;transition:transform .2s;box-shadow:var(--shadow-sm);border:1px solid var(--border);}.city-card:hover{transform:translateY(-4px);box-shadow:var(--shadow);}.city-card a{text-decoration:none;color:var(--text);display:block;}.city-card h3{color:var(--navy);margin-bottom:8px;}.city-card p{color:var(--muted);margin-bottom:12px;}.city-card-link{color:var(--red);font-weight:600;}</style>"""
    
    (CITIES_DIR / "index.html").write_text(
        page_shell("Top 50 US Cities for Donation Centers", "Browse donation centers in America's largest cities.", "/cities", cities_index_html),
        encoding="utf-8"
    )
    
    print(f"✅ Generated {len(top_cities)} city pages in cities/ directory")
    return len(top_cities)

# ============================================================
# ALL LOCATIONS HUB PAGE
# ============================================================

    
   
def render_all_locations_hub(stores):
    """Generate the main All Locations hub page"""
    top_cities = get_top_cities(stores, 15)
    
    state_counts = defaultdict(int)
    for store in stores:
        state = store.get("state")
        if state:
            state_counts[state] += 1
    top_states = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)[:12]
    
    body = f"""  <div class="page-header">
    <div class="container">
      <div class="breadcrumb">
        <a href="{BASE_URL}/">Home</a>
        <span class="sep">›</span>
        <span>All Locations</span>
      </div>
      <h1>Find Donation Centers Near You</h1>
      <p>Browse {len(stores):,} donation centers across the United States by city, state, or category.</p>
    </div>
  </div>

  <main class="all-locations-hub">
    <div class="container">
      <div class="hub-section">
        <h2>📍 Top Cities</h2>
        <div class="cities-grid-hub">"""
    
    for city_info in top_cities:
        body += f"""
          <a href="{BASE_URL}/cities/{city_info['slug']}" class="hub-card">
            <h3>{esc(city_info['city'])}, {esc(city_info['state_abbr'])}</h3>
            <p>{len(city_info['stores'])} donation centers</p>
          </a>"""
    
    body += f"""
        </div>
        <div class="view-all"><a href="{BASE_URL}/cities/" class="btn btn-outline">View All Cities →</a></div>
      </div>

      <div class="hub-section">
        <h2>🗺️ Popular States</h2>
        <div class="states-grid-hub">"""
    
    for state, count in top_states:
        slug = state_slug(state)
        body += f"""
          <a href="{BASE_URL}/states/{slug}" class="hub-card">
            <h3>{esc(state)}</h3>
            <p>{count} locations</p>
          </a>"""
    
    body += f"""
        </div>
        <div class="view-all"><a href="{BASE_URL}/states/" class="btn btn-outline">View All States →</a></div>
      </div>

      <div class="hub-section">
        <h2>🏷️ Browse by Category</h2>
        <div class="categories-grid-hub">
          <a href="{BASE_URL}/thrift-stores" class="category-hub-card">
            <div class="category-icon">🛍️</div>
            <h3>Thrift Stores</h3>
            <p>Find second-hand stores & donation centers</p>
          </a>
          <a href="{BASE_URL}/food-pantries" class="category-hub-card">
            <div class="category-icon">🍎</div>
            <h3>Food Pantries</h3>
            <p>Free food assistance programs</p>
          </a>
          <a href="{BASE_URL}/rehab-centers" class="category-hub-card">
            <div class="category-icon">💪</div>
            <h3>Rehab Centers</h3>
            <p>Recovery & rehabilitation services</p>
          </a>
        </div>
      </div>

      <div class="hub-section">
        <h2>📊 Quick Stats</h2>
        <div class="stats-grid-hub">
          <div class="stat-hub-card"><div class="stat-number">{len(stores):,}</div><div class="stat-label">Total Locations</div></div>
          <div class="stat-hub-card"><div class="stat-number">50</div><div class="stat-label">States Covered</div></div>
          <div class="stat-hub-card"><div class="stat-number">{len(top_cities)}+</div><div class="stat-label">Cities</div></div>
        </div>
      </div>
    </div>
  </main>

  <style>
    .all-locations-hub {{ padding: 40px 0; }}
    .hub-section {{ margin-bottom: 50px; }}
    .hub-section h2 {{ font-size: 1.5rem; color: var(--navy); margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid var(--red); display: inline-block; }}
    .cities-grid-hub, .states-grid-hub {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; margin: 20px 0; }}
    .hub-card {{ background: var(--white); padding: 20px; border-radius: 8px; text-decoration: none; text-align: center; transition: all 0.2s; box-shadow: var(--shadow-sm); border: 1px solid var(--border); }}
    .hub-card:hover {{ transform: translateY(-2px); box-shadow: var(--shadow); }}
    .hub-card h3 {{ color: var(--navy); margin-bottom: 8px; font-size: 1rem; }}
    .hub-card p {{ color: var(--muted); font-size: 0.85rem; }}
    .categories-grid-hub {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin: 20px 0; }}
    .category-hub-card {{ background: var(--white); padding: 30px; border-radius: 12px; text-decoration: none; text-align: center; transition: all 0.2s; box-shadow: var(--shadow-sm); border: 1px solid var(--border); }}
    .category-hub-card:hover {{ transform: translateY(-3px); box-shadow: var(--shadow); }}
    .category-icon {{ font-size: 2.5rem; margin-bottom: 12px; }}
    .category-hub-card h3 {{ color: var(--navy); margin-bottom: 8px; }}
    .category-hub-card p {{ color: var(--muted); font-size: 0.85rem; }}
    .stats-grid-hub {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin: 20px 0; }}
    .stat-hub-card {{ background: var(--navy); color: white; padding: 30px; border-radius: 12px; text-align: center; }}
    .stat-hub-card .stat-number {{ font-size: 2rem; font-weight: 800; }}
    .stat-hub-card .stat-label {{ font-size: 0.85rem; opacity: 0.8; }}
    .view-all {{ text-align: center; margin-top: 20px; }}
    @media (max-width: 768px) {{
      .categories-grid-hub, .stats-grid-hub {{ grid-template-columns: 1fr; }}
    }}
  </style>
"""
    
    return page_shell("All Donation Center Locations | Find Thrift Stores & Food Pantries", f"Find {len(stores):,} donation centers across the United States. Browse by city, state, or category.", "/all-locations", body)

# ============================================================
# SITEMAP & ROBOTS.TXT
# ============================================================

def build_sitemap(stores):
    today = date.today().isoformat()
    states = sorted({state_slug(s.get("state")) for s in stores if s.get("state")})
    top_cities = get_top_cities(stores, 50)

    entries = []
    for path, priority, changefreq in STATIC_PAGES:
        entries.append((BASE_URL + path, priority, changefreq))
    
    entries.append((f"{BASE_URL}/states", "0.9", "weekly"))
    entries.append((f"{BASE_URL}/cities", "0.9", "weekly"))
    entries.append((f"{BASE_URL}/stores", "0.8", "weekly"))
    entries.append((f"{BASE_URL}/all-locations", "0.9", "weekly"))
    
    for slug in states:
        entries.append((f"{BASE_URL}/states/{slug}", "0.8", "weekly"))
    
    for city_info in top_cities:
        entries.append((f"{BASE_URL}/cities/{city_info['slug']}", "0.7", "weekly"))
    
    for store in stores:
        entries.append((BASE_URL + store_path(store), "0.6", "monthly"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, priority, changefreq in entries:
        lines.append(f"""  <url>
    <loc>{esc(loc)}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    lines.append("</urlset>")
    SITEMAP_PATH.write_text("\n".join(lines), encoding="utf-8")
    return len(entries)

def generate_robots_txt():
    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(robots_content, encoding="utf-8")
    print("✅ Generated robots.txt")

# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    print("🚀 Starting static site generation...")
    
    stores = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    print(f"📦 Loaded {len(stores):,} stores from JSON")
    
    # Create directories
    STORES_DIR.mkdir(exist_ok=True)
    STATES_DIR.mkdir(exist_ok=True)
    CITIES_DIR.mkdir(exist_ok=True)
    
    # Clean old files
    for html_file in STORES_DIR.glob("*.html"):
        html_file.unlink()
    for html_file in STATES_DIR.glob("*.html"):
        html_file.unlink()
    for html_file in CITIES_DIR.glob("*.html"):
        html_file.unlink()
    
    # Generate store pages
    print("\n📄 Generating store pages...")
    seen = set()
    for store in stores:
        slug = store_slug(store)
        if slug in seen:
            raise RuntimeError(f"Duplicate generated slug: {slug}")
        seen.add(slug)
        (STORES_DIR / f"{slug}.html").write_text(render_store_page(store), encoding="utf-8")
    print(f"  ✅ Generated {len(stores):,} store pages")
    
    # Generate state pages
    print("\n🗺️ Generating state pages...")
    by_state = defaultdict(list)
    for store in stores:
        state = store.get("state")
        if state:
            by_state[state].append(store)
    
    for state_name, state_stores in by_state.items():
        slug = state_slug(state_name)
        (STATES_DIR / f"{slug}.html").write_text(render_state_page(state_name, state_stores), encoding="utf-8")
    print(f"  ✅ Generated {len(by_state)} state pages")
    
    # Generate states index
    (STATES_DIR / "index.html").write_text(render_states_index_page(stores), encoding="utf-8")
    print(f"  ✅ Generated states/index.html")
    
    # Generate city pages (top 50)
    print("\n🏙️ Generating city pages...")
    city_count = generate_city_pages(stores, 50)
    print(f"  ✅ Generated {city_count} city pages")
    
    # Generate stores index
    (STORES_DIR / "index.html").write_text(render_stores_index_page(stores), encoding="utf-8")
    print(f"  ✅ Generated stores/index.html")
    
    # Generate All Locations hub page
    (ROOT / "all-locations.html").write_text(render_all_locations_hub(stores), encoding="utf-8")
    print(f"  ✅ Generated all-locations.html")
    
    # Generate sitemap
    sitemap_count = build_sitemap(stores)
    print(f"\n📊 Generated sitemap.xml with {sitemap_count:,} URLs")
    
    # Generate robots.txt
    generate_robots_txt()
    
    print(f"\n{'='*50}")
    print(f"🎉 GENERATION COMPLETE!")
    print(f"{'='*50}")
    print(f"📁 Store pages: {STORES_DIR}")
    print(f"📁 State pages: {STATES_DIR}")
    print(f"📁 City pages: {CITIES_DIR}")
    print(f"📄 All Locations page: all-locations.html")
    print(f"📄 Sitemap: sitemap.xml")
    print(f"📄 Robots.txt: robots.txt")
    print(f"\n✅ Total pages generated: {len(stores) + len(by_state) + city_count + 4:,}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()