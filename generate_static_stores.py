#!/usr/bin/env python3
"""
Generate static HTML store detail pages for Donation Center Finder.

Why this exists:
- store.html is a JavaScript-rendered shell.
- Crawlers that do not execute JavaScript see weak/empty store pages.
- This script pre-generates one crawlable HTML page per store from
  js/enriched_stores_clean.json, plus a crawlable /stores directory page.

Run:
    python3 generate_static_stores.py
"""

import json
import re
import html
from pathlib import Path
from datetime import date
from urllib.parse import quote

BASE_URL = "https://donationcenterfinder.com"
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "js" / "enriched_stores_clean.json"
STORES_DIR = ROOT / "stores"
SITEMAP_PATH = ROOT / "sitemap.xml"

STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/thrift-stores", "0.9", "weekly"),
    ("/food-pantries", "0.9", "weekly"),
    ("/rehab-centers", "0.9", "weekly"),
    ("/states", "0.8", "weekly"),
    ("/stores", "0.8", "weekly"),
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

def schema_image(store):
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
        str(part)
        for part in [
            store.get("name"),
            store.get("city"),
            store.get("state_abbr") or store.get("state"),
            store.get("zip"),
        ]
        if part
    )
    suffix = short_id(store)
    return f"{slugify(base)}-{suffix}" if suffix else slugify(base)


def store_path(store):
    return f"/stores/{store_slug(store)}.html"


def state_slug(state_name):
    return STATE_SLUGS.get(state_name, slugify(state_name))


def category_label(category):
    return {
        "thrift": "Thrift Store & Donation Center",
        "food": "Food Pantry",
        "rehab": "Rehabilitation Center",
    }.get(str(category or "").lower(), "Donation Center")
def placeholder_image(store):
    category = str(store.get("category") or "").lower()
    if category == "food":
        return "../images/placeholder-food.jpg"
    if category == "rehab":
        return "../images/placeholder-rehab.jpg"
    return "../images/placeholder-thrift.jpg"


def display_image(store):
    photo = str(store.get("photo") or "")
    if photo.startswith("images/"):
        return "../" + photo
    if photo.startswith("/images/"):
        return ".." + photo
    return placeholder_image(store)


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


def json_ld(store):
    path = store_path(store)
    schema = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "Store"],
        "name": store.get("name"),
        "url": BASE_URL + path,
        "image": schema_image(store), "telephone": store.get("phone"),
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

    # Drop empty values, including inside address.
    schema = {k: v for k, v in schema.items() if v}
    if "address" in schema:
        schema["address"] = {k: v for k, v in schema["address"].items() if v}
    return json.dumps(schema, ensure_ascii=False, separators=(",", ":"))


def page_shell(title, description, canonical_path, body, extra_head=""):
    canonical = BASE_URL + canonical_path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Donation Center Finder">
  <meta property="og:title" content="{esc(title)}">
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
          <li><a href="{BASE_URL}/states">States</a></li>
          <li><a href="{BASE_URL}/stores">All Locations</a></li>
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
            <li><a href="{BASE_URL}/states">Browse All States</a></li>
            <li><a href="{BASE_URL}/submit">Submit a Location</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h3>Popular States</h3>
          <ul>
            <li><a href="{BASE_URL}/state?state=california">California</a></li>
            <li><a href="{BASE_URL}/state?state=texas">Texas</a></li>
            <li><a href="{BASE_URL}/state?state=florida">Florida</a></li>
            <li><a href="{BASE_URL}/state?state=new-york">New York</a></li>
            <li><a href="{BASE_URL}/state?state=illinois">Illinois</a></li>
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


def render_store_page(store):
    path = store_path(store)
    state = store.get("state") or ""
    state_link = f"/state?state={state_slug(state)}"
    city = store.get("city") or ""
    category = category_label(store.get("category"))
    rating_snippet = ""
    try:
        rating = float(store.get("rating") or 0)
        reviews = int(store.get("review_count") or 0)
        if rating > 0:
            rating_snippet = f" Rated {rating:.1f}/5 by {reviews:,} reviewers."
    except (TypeError, ValueError):
        pass

    title = f"{store.get('name')} — {city}, {state} | Donation Center Finder"
    description = (
        f"Visit {store.get('name')} in {city}, {state}."
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
        <span class="sep">&#8250;</span>
        <a href="{BASE_URL}/states">States</a>
        <span class="sep">&#8250;</span>
        <a href="{BASE_URL}/{esc(state_link)}">{esc(state)}</a>
        <span class="sep">&#8250;</span>
        <span>{esc(store.get("name"))}</span>
      </div>
    </div>
  </div>

  <main class="store-detail">
    <div class="container">
      <div class="store-detail-card">
        <div class="store-detail-photo"><img src="{esc(img)}" alt="{esc(store.get("name"))}" loading="eager"></div>
        <div class="store-detail-header">
          <div class="store-detail-logo">SA</div>
          <div class="store-detail-title">
            <h1>{esc(store.get("name"))}</h1>
            <div class="city-state">{esc(city)}, {esc(state)} {esc(store.get("zip"))}</div>
            {rating_html(store)}
          </div>
        </div>
        <div class="store-detail-body">
          <div class="detail-section">
            <div class="detail-section-title">Contact &amp; Location</div>
            <div class="info-row"><span class="icon">&#128205;</span><span>{esc(address_line)}</span></div>
            {f'<div class="info-row"><span class="icon">&#128222;</span><a href="tel:{esc(phone)}">{esc(phone)}</a></div>' if phone else ''}
            {f'<div class="info-row"><span class="icon">&#127760;</span><a href="{esc(website)}" target="_blank" rel="noopener">{esc(re.sub(r"^https?://", "", website).rstrip("/"))}</a></div>' if website else ''}
            {f'<div style="margin-top:12px;"><a href="{esc(maps)}" target="_blank" rel="noopener" class="btn btn-outline">&#128205; View on Google Maps</a></div>' if maps else ''}
          </div>

{hours_html(store)}

          <div class="detail-section">
            <div class="detail-section-title">Service Type</div>
            <span class="tag" style="font-size:0.95rem;">{esc(category)}</span>
          </div>

          <div class="detail-section">
            <div class="detail-section-title">About This Location</div>
            <p style="color:var(--muted); font-size:0.95rem;">
              {esc(store.get("name"))} is listed in our directory as a {esc(category.lower())}
              serving {esc(city)}, {esc(state)}. Use the contact details above to confirm current hours,
              donation guidelines, services, and availability before visiting.
            </p>
          </div>

          <div style="text-align:center; padding-top:8px; font-size:0.83rem; color:var(--muted);">
            <a href="{BASE_URL}/submit" style="color:var(--muted);">&#9999; Suggest a correction</a>
          </div>
        </div>
      </div>
      <p style="margin-top:20px;"><a href="{BASE_URL}/{esc(state_link)}" class="btn btn-outline">&#8592; All {esc(state)} stores</a> <a href="{BASE_URL}/stores" class="btn btn-outline">All locations</a></p>
    </div>
  </main>
"""
    extra_head = f'  <script type="application/ld+json">{json_ld(store)}</script>\n'
    return page_shell(title, description, path, body, extra_head)


def render_index_page(stores):
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
      <section class="detail-section">
        <div class="detail-section-title">{esc(state)} Donation Centers</div>
        <ul style="columns:2; line-height:1.8; padding-left:20px;">
{links}
        </ul>
      </section>""")

    body = f"""  <main class="section">
    
  </main>
"""
    return page_shell(
        "All Donation Center Locations | Donation Center Finder",
        f"Browse all {len(stores):,} donation center location pages by state, including thrift stores, food pantries, and rehabilitation centers.",
        "/stores",
        body
    )


def build_sitemap(stores):
    today = date.today().isoformat()
    states = sorted({state_slug(s.get("state")) for s in stores if s.get("state")})

    entries = []
    for path, priority, changefreq in STATIC_PAGES:
        entries.append((BASE_URL + path, priority, changefreq))
    for slug in states:
        entries.append((f"{BASE_URL}/state?state={quote(slug)}", "0.8", "weekly"))
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


def main():
    stores = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    STORES_DIR.mkdir(exist_ok=True)

    # Remove previously generated store HTML files so deleted stores do not linger.
    for html_file in STORES_DIR.glob("*.html"):
        html_file.unlink()

    seen = set()
    for store in stores:
        slug = store_slug(store)
        if slug in seen:
            raise RuntimeError(f"Duplicate generated slug: {slug}")
        seen.add(slug)
        (STORES_DIR / f"{slug}.html").write_text(render_store_page(store), encoding="utf-8")

    (STORES_DIR / "index.html").write_text(render_index_page(stores), encoding="utf-8")
    sitemap_count = build_sitemap(stores)

    print(f"Generated {len(stores):,} static store pages in {STORES_DIR}")
    print(f"Generated /stores index page")
    print(f"Generated sitemap.xml with {sitemap_count:,} URLs")


if __name__ == "__main__":
    main()
