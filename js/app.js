/* ============================================================
   SA Bin Finder — Application Logic
   ============================================================ */

/* ---- UTILITIES ---- */

const SITE_URL = 'https://sabinfinder.com';

function getParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}

/**
 * Updates <title>, <meta description>, <link canonical>, and Open Graph tags.
 * Call this from every page init after data is known.
 */
function setPageMeta(title, description, canonicalPath) {
  document.title = title;

  let metaDesc = document.querySelector('meta[name="description"]');
  if (!metaDesc) {
    metaDesc = document.createElement('meta');
    metaDesc.name = 'description';
    document.head.appendChild(metaDesc);
  }
  metaDesc.content = description;

  let canonical = document.querySelector('link[rel="canonical"]');
  if (!canonical) {
    canonical = document.createElement('link');
    canonical.rel = 'canonical';
    document.head.appendChild(canonical);
  }
  canonical.href = SITE_URL + canonicalPath;

  // Open Graph
  const og = { 'og:title': title, 'og:description': description, 'og:url': SITE_URL + canonicalPath };
  Object.entries(og).forEach(([prop, val]) => {
    let tag = document.querySelector(`meta[property="${prop}"]`);
    if (!tag) {
      tag = document.createElement('meta');
      tag.setAttribute('property', prop);
      document.head.appendChild(tag);
    }
    tag.content = val;
  });
}

/**
 * Injects JSON-LD LocalBusiness schema for an enriched store.
 */
function injectStoreSchema(store) {
  const existing = document.getElementById('ld-store');
  if (existing) existing.remove();

  const rating   = parseFloat(store.rating)       || 0;
  const reviews  = parseInt(store.review_count)   || 0;
  const pid      = encodeURIComponent(store.place_id || '');

  const schema = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "Store"],
    "name": store.name,
    "address": {
      "@type": "PostalAddress",
      "streetAddress": store.address,
      "addressLocality": store.city,
      "addressRegion": store.state_abbr || store.state,
      "postalCode": store.zip,
      "addressCountry": "US"
    },
    "url": `${SITE_URL}/store.html?pid=${pid}`,
  };

  if (store.latitude && store.longitude) {
    schema.geo = {
      "@type": "GeoCoordinates",
      "latitude":  store.latitude,
      "longitude": store.longitude
    };
  }
  if (rating > 0 && reviews > 0) {
    schema.aggregateRating = {
      "@type": "AggregateRating",
      "ratingValue": rating.toFixed(1),
      "reviewCount": reviews
    };
  }
  if (store.top_reviews && store.top_reviews.length > 0) {
    schema.review = store.top_reviews.slice(0, 3).map(r => ({
      "@type": "Review",
      "author": { "@type": "Person", "name": r.author || "Reviewer" },
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": r.rating || 5
      },
      "reviewBody": (r.text || '').slice(0, 500)
    }));
  }

  const script = document.createElement('script');
  script.id   = 'ld-store';
  script.type = 'application/ld+json';
  script.textContent = JSON.stringify(schema, null, 0);
  document.head.appendChild(script);
}

function storesByState(slug) {
  return window.SAData.stores.filter(s => s.slug === slug);
}

function storeById(id) {
  return window.SAData.stores.find(s => s.id === id);
}

function stateBySlug(slug) {
  return window.SAData.states.find(s => s.slug === slug);
}

function storeCount(slug) {
  const stateData = stateBySlug(slug);
  if (!stateData) return 0;
  if (window.SAEnriched) {
    return window.SAEnriched.filter(s => s.state === stateData.name).length;
  }
  return window.SAData.stores.filter(s => s.slug === slug).length;
}

function todaysHours(hours) {
  const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const today = days[new Date().getDay()];
  return hours[today] || 'Call for hours';
}

function fmtDate(str) {
  if (!str) return '';
  const d = new Date(str);
  if (isNaN(d)) return '';
  return d.toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' });
}

function escHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ---- ENRICHED HELPERS ---- */

function enrichedByState(stateName) {
  if (!window.SAEnriched) return [];
  return window.SAEnriched.filter(s => s.state === stateName);
}

function storeByPlaceId(pid) {
  if (!window.SAEnriched) return null;
  return window.SAEnriched.find(s => s.place_id === pid);
}

function starsHtml(rating) {
  const r    = parseFloat(rating) || 0;
  const full = Math.floor(r);
  const half = (r - full) >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  let h = '<span class="stars-row">';
  for (let i = 0; i < full;  i++) h += '<span class="star-f">★</span>';
  if (half)                         h += '<span class="star-h">★</span>';
  for (let i = 0; i < empty; i++) h += '<span class="star-e">★</span>';
  return h + '</span>';
}

function scoreBar(label, score) {
  if (score == null) return '';
  const pct = Math.round((score / 10) * 100);
  const cls = pct >= 70 ? 'good' : pct >= 50 ? 'mid' : 'low';
  return `
    <div class="score-item">
      <div class="score-top">
        <span class="score-lbl">${label}</span>
        <span class="score-num ${cls}">${score}<span class="score-den">/10</span></span>
      </div>
      <div class="score-bar-wrap"><div class="score-fill ${cls}" style="width:${pct}%"></div></div>
    </div>`;
}

/* ---- ENRICHED STORE CARD ---- */

function storeCardEnriched(store) {
  const rating      = parseFloat(store.rating) || 0;
  const reviewCount = parseInt(store.review_count) || 0;

  const ratingHtml = rating > 0 ? `
    <div class="store-rating">
      ${starsHtml(rating)}
      <span class="rating-num">${rating.toFixed(1)}</span>
      <span class="rating-cnt">(${reviewCount.toLocaleString()})</span>
    </div>` : '';

  const chips = [
    store.friendly_staff_score != null ? `<span class="schip good">Staff ${store.friendly_staff_score}/10</span>` : '',
    store.donations_score      != null ? `<span class="schip mid">Donations ${store.donations_score}/10</span>`   : '',
    store.cleanliness_score    != null ? `<span class="schip">Clean ${store.cleanliness_score}/10</span>`         : '',
  ].filter(Boolean).join('');

  return `
    <div class="store-card">
      <div class="store-card-header">
        <div class="store-card-logo">SA</div>
        <div>
          <div class="store-card-title">${escHtml(store.name)}</div>
          <div class="store-card-city">${escHtml(store.city)}, ${store.state_abbr || store.state}</div>
        </div>
      </div>
      <div class="store-card-body">
        <div class="store-card-detail">
          <span class="store-card-detail-icon">&#128205;</span>
          <span>${escHtml(store.address)}, ${escHtml(store.city)}, ${store.state_abbr} ${store.zip}</span>
        </div>
        ${ratingHtml}
        ${chips ? `<div class="schips-row">${chips}</div>` : ''}
      </div>
      <div class="store-card-footer">
        <a href="store.html?pid=${encodeURIComponent(store.place_id)}" class="btn btn-primary btn-block">View Store Details</a>
      </div>
    </div>`;
}

/* ---- SHARED COMPONENTS ---- */

function renderNav() {
  document.getElementById('navContainer').innerHTML = `
    <nav class="nav">
      <div class="container">
        <div class="nav-inner">
          <a href="index.html" class="nav-logo">
            <div class="nav-logo-icon">SA</div>
            <span>SA Bin Finder</span>
          </a>
          <ul class="nav-links">
            <li><a href="index.html">Home</a></li>
            <li><a href="states.html">Browse States</a></li>
            <li><a href="submit.html" class="nav-cta">+ Add a Store</a></li>
          </ul>
          <div class="nav-toggle" id="navToggle">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </nav>
    <div class="mobile-menu" id="mobileMenu">
      <a href="index.html">Home</a>
      <a href="states.html">Browse States</a>
      <a href="submit.html">+ Add a Store</a>
    </div>
  `;
  document.getElementById('navToggle').addEventListener('click', () => {
    document.getElementById('mobileMenu').classList.toggle('open');
  });
}

function renderFooter() {
  document.getElementById('footerContainer').innerHTML = `
    <footer>
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <div class="footer-logo">
              <div class="footer-logo-icon">SA</div>
              <span>SA Bin Finder</span>
            </div>
            <p>The #1 community directory for Salvation Army bin stores and by-the-pound outlets across all 50 states. Find your nearest store today — free, always.</p>
          </div>
          <div>
            <div class="footer-heading">Quick Links</div>
            <ul class="footer-links">
              <li><a href="index.html">Home</a></li>
              <li><a href="states.html">Browse All States</a></li>
              <li><a href="submit.html">Submit a Store</a></li>
            </ul>
          </div>
          <div>
            <div class="footer-heading">Popular States</div>
            <ul class="footer-links">
              <li><a href="state.html?state=california">California</a></li>
              <li><a href="state.html?state=texas">Texas</a></li>
              <li><a href="state.html?state=florida">Florida</a></li>
              <li><a href="state.html?state=new-york">New York</a></li>
              <li><a href="state.html?state=michigan">Michigan</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2025 SA Bin Finder &mdash; Community-powered directory. Not affiliated with The Salvation Army.</p>
        </div>
      </div>
    </footer>
  `;
}

/* ---- STORE CARD (legacy data.js stores) ---- */

function storeCard(store) {
  const hours = todaysHours(store.hours);
  const tags  = store.features.slice(0, 4).map(f => `<span class="tag">${f}</span>`).join('');
  const badge = store.verified ? '<span class="badge-verified">&#10003; Verified</span>' : '';
  return `
    <div class="store-card">
      <div class="store-card-header">
        <div class="store-card-logo">SA</div>
        <div>
          <div class="store-card-title">${store.name}</div>
          <div class="store-card-city">${store.city}, ${store.state}</div>
        </div>
      </div>
      <div class="store-card-body">
        <div class="store-card-detail">
          <span class="store-card-detail-icon">&#128205;</span>
          <span>${store.address}, ${store.city}, ${store.state} ${store.zip}</span>
        </div>
        <div class="store-card-detail">
          <span class="store-card-detail-icon">&#128222;</span>
          <span>${store.phone}</span>
        </div>
        <div class="store-card-detail">
          <span class="store-card-detail-icon">&#9878;</span>
          <span><strong>${store.pricing}</strong> &middot; Restocks: ${store.restock_days.join(', ')}</span>
        </div>
        <div class="store-card-detail">
          <span class="store-card-detail-icon">&#128336;</span>
          <span>Today: ${hours}</span>
        </div>
        <div class="store-card-tags">${tags}${badge}</div>
      </div>
      <div class="store-card-footer">
        <a href="store.html?id=${store.id}" class="btn btn-primary btn-block">View Store Details</a>
      </div>
    </div>
  `;
}

/* ---- STATES GRID ---- */

function statesGrid(states) {
  return states.map(state => {
    const count = storeCount(state.slug);
    const label = count > 0 ? `${count.toLocaleString()} store${count > 1 ? 's' : ''}` : 'Be first to add';
    return `
      <a href="state.html?state=${state.slug}" class="state-card">
        <div class="state-card-name">${state.name}</div>
        <div class="state-card-count ${count > 0 ? 'has-stores' : ''}">${label}</div>
      </a>
    `;
  }).join('');
}

/* ============================================================
   PAGE: HOMEPAGE
   ============================================================ */

async function initHomepage() {
  const ready = window._enrichedReady || Promise.resolve([]);
  await ready;

  /* Store count */
  const totalEl = document.getElementById('totalStores');
  if (totalEl) {
    const total = window.SAEnriched ? window.SAEnriched.length : window.SAData.stores.length;
    totalEl.textContent = total.toLocaleString();
  }

  /* States grid */
  const statesEl = document.getElementById('statesGrid');
  if (statesEl) statesEl.innerHTML = statesGrid(window.SAData.states);

  /* Featured stores */
  const recentEl = document.getElementById('recentStores');
  if (recentEl) {
    if (window.SAEnriched && window.SAEnriched.length > 0) {
      const titleEl = document.getElementById('recentStoresTitle');
      const subEl   = document.getElementById('recentStoresSub');
      if (titleEl) titleEl.textContent = 'Top-Rated Stores';
      if (subEl)   subEl.textContent   = 'Highest-rated Salvation Army stores from across the country';

      const featured = [...window.SAEnriched]
        .filter(s => parseFloat(s.rating) >= 4.3 && parseInt(s.review_count) >= 20)
        .sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating))
        .slice(0, 6);
      const toShow = featured.length >= 3 ? featured : window.SAEnriched.slice(0, 6);
      recentEl.innerHTML = toShow.map(storeCardEnriched).join('');
    } else {
      const recent = [...window.SAData.stores]
        .sort((a, b) => new Date(b.added) - new Date(a.added))
        .slice(0, 6);
      recentEl.innerHTML = recent.map(storeCard).join('');
    }
  }

  /* Search */
  const searchBtn   = document.getElementById('searchBtn');
  const searchInput = document.getElementById('searchInput');
  if (searchBtn && searchInput) {
    searchBtn.addEventListener('click', doSearch);
    searchInput.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });
  }
}

/* Map state abbreviations → full names for search normalisation */
const STATE_ABBR_MAP = {
  al:'alabama',ak:'alaska',az:'arizona',ar:'arkansas',ca:'california',
  co:'colorado',ct:'connecticut',de:'delaware',fl:'florida',ga:'georgia',
  hi:'hawaii',id:'idaho',il:'illinois',in:'indiana',ia:'iowa',
  ks:'kansas',ky:'kentucky',la:'louisiana',me:'maine',md:'maryland',
  ma:'massachusetts',mi:'michigan',mn:'minnesota',ms:'mississippi',mo:'missouri',
  mt:'montana',ne:'nebraska',nv:'nevada',nh:'new hampshire',nj:'new jersey',
  nm:'new mexico',ny:'new york',nc:'north carolina',nd:'north dakota',oh:'ohio',
  ok:'oklahoma',or:'oregon',pa:'pennsylvania',ri:'rhode island',sc:'south carolina',
  sd:'south dakota',tn:'tennessee',tx:'texas',ut:'utah',vt:'vermont',
  va:'virginia',wa:'washington',wv:'west virginia',wi:'wisconsin',wy:'wyoming',dc:'district of columbia'
};

function buildSearchText(s) {
  return [s.city, s.state, s.state_abbr, s.zip, s.county, s.address, s.name]
    .map(v => (v || '').toLowerCase()).join(' ');
}

function normaliseQuery(raw) {
  // Strip commas/periods, collapse spaces
  let q = raw.toLowerCase().replace(/[,\.]/g, ' ').replace(/\s+/g, ' ').trim();
  // Expand any state abbreviation tokens so "tx" becomes "texas"
  const tokens = q.split(' ').map(t => STATE_ABBR_MAP[t] || t);
  return tokens;
}

async function doSearch() {
  const ready = window._enrichedReady || Promise.resolve([]);
  await ready;

  const rawQuery = document.getElementById('searchInput').value.trim();
  if (!rawQuery) return;

  const tokens = normaliseQuery(rawQuery);

  let results, isEnriched;
  if (window.SAEnriched) {
    isEnriched = true;
    results = window.SAEnriched.filter(s => {
      const text = buildSearchText(s);
      return tokens.every(tok => text.includes(tok));
    });
  } else {
    isEnriched = false;
    results = window.SAData.stores.filter(s => {
      const text = [s.city, s.state, s.zip, s.address, s.name]
        .map(v => (v || '').toLowerCase()).join(' ');
      return tokens.every(tok => text.includes(tok));
    });
  }

  const section  = document.getElementById('searchResults');
  const grid     = document.getElementById('searchResultsGrid');
  const titleEl  = document.getElementById('searchResultsTitle');
  if (!section) return;

  titleEl.textContent = `${results.length.toLocaleString()} result${results.length !== 1 ? 's' : ''} for "${rawQuery}"`;
  section.style.display = 'block';

  if (results.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">&#128269;</div>
        <h3>No stores found</h3>
        <p>Try a different city, state, or zip code — or <a href="submit.html">add this store</a> to the directory!</p>
      </div>`;
  } else {
    const capped = results.slice(0, 30);
    grid.innerHTML = capped.map(isEnriched ? storeCardEnriched : storeCard).join('');
    if (results.length > 30) {
      grid.innerHTML += `<p style="grid-column:1/-1; text-align:center; color:var(--muted); padding:16px 0; font-size:0.9rem;">Showing 30 of ${results.length.toLocaleString()} results — try a more specific search.</p>`;
    }
  }
  section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ============================================================
   PAGE: ALL STATES
   ============================================================ */

async function initStatesPage() {
  const ready = window._enrichedReady || Promise.resolve([]);
  await ready;

  const el = document.getElementById('allStatesGrid');
  if (!el) return;
  el.innerHTML = statesGrid(window.SAData.states);

  const searchEl = document.getElementById('stateSearch');
  if (searchEl) {
    searchEl.addEventListener('input', () => {
      const q = searchEl.value.toLowerCase();
      const filtered = q
        ? window.SAData.states.filter(s => s.name.toLowerCase().includes(q))
        : window.SAData.states;
      el.innerHTML = statesGrid(filtered);
      if (filtered.length === 0) {
        el.innerHTML = `<div class="empty-state" style="grid-column:1/-1"><div class="empty-state-icon">&#128269;</div><h3>No states matched</h3><p>Try a different search term.</p></div>`;
      }
    });
  }
}

/* ============================================================
   PAGE: STATE STORES
   ============================================================ */

async function initStatePage() {
  const slug = getParam('state');
  if (!slug) { window.location.href = 'states.html'; return; }

  const stateData = stateBySlug(slug);
  if (!stateData) { window.location.href = 'states.html'; return; }

  const ready = window._enrichedReady || Promise.resolve([]);
  await ready;

  const stores     = window.SAEnriched ? enrichedByState(stateData.name) : storesByState(slug);

  setPageMeta(
    `Salvation Army Stores in ${stateData.name} — ${stores.length} Locations | SA Bin Finder`,
    `Find all ${stores.length} Salvation Army thrift and bin stores in ${stateData.name}. Browse by city, view Google ratings, hours, and donation pickup options.`,
    `/state.html?state=${slug}`
  );

  const bcEl = document.getElementById('breadcrumbState');
  if (bcEl) bcEl.textContent = stateData.name;

  const hEl = document.getElementById('pageTitle');
  const sEl = document.getElementById('pageSubtitle');
  if (hEl) hEl.textContent = `${stateData.name} Bin Stores`;
  if (sEl) sEl.textContent = `${stores.length.toLocaleString()} Salvation Army bin store${stores.length !== 1 ? 's' : ''} found in ${stateData.name}`;

  const cityFilter = document.getElementById('cityFilter');
  const cities = [...new Set(stores.map(s => s.city))].sort();
  if (cityFilter && cities.length > 1) {
    cityFilter.innerHTML = `<option value="">All Cities</option>` +
      cities.map(c => `<option value="${escHtml(c)}">${escHtml(c)}</option>`).join('');
    cityFilter.addEventListener('change', () => {
      const city = cityFilter.value;
      const filtered = city ? stores.filter(s => s.city === city) : stores;
      const countEl = document.getElementById('resultCount');
      if (countEl) countEl.textContent = `${filtered.length.toLocaleString()} store${filtered.length !== 1 ? 's' : ''} shown`;
      renderStoreGrid(filtered);
    });
  }

  const countEl = document.getElementById('resultCount');
  if (countEl) countEl.textContent = `${stores.length.toLocaleString()} store${stores.length !== 1 ? 's' : ''} shown`;

  renderStoreGrid(stores);
}

function renderStoreGrid(stores) {
  const el = document.getElementById('storesContainer');
  if (!el) return;
  if (stores.length === 0) {
    el.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">&#127978;</div>
        <h3>No stores listed yet</h3>
        <p>Be the first to add a Salvation Army bin store in this state!</p>
        <a href="submit.html" class="btn btn-primary">Add a Store</a>
      </div>`;
  } else {
    const isEnriched = stores[0] && stores[0].place_id;
    el.innerHTML = stores.map(isEnriched ? storeCardEnriched : storeCard).join('');
  }
}

/* ============================================================
   PAGE: STORE DETAIL
   ============================================================ */

async function initStorePage() {
  const pid = getParam('pid');
  const id  = getParam('id');

  if (pid) {
    const ready = window._enrichedReady || Promise.resolve([]);
    await ready;
    const store = storeByPlaceId(decodeURIComponent(pid));
    if (store) {
      renderEnrichedStoreDetail(store);
      return;
    }
  }

  if (id) {
    const store = storeById(id);
    if (store) {
      renderLegacyStoreDetail(store);
      return;
    }
  }

  document.getElementById('storeDetailContainer').innerHTML = `
    <div class="empty-state">
      <div class="empty-state-icon">&#128269;</div>
      <h3>Store not found</h3>
      <p><a href="index.html">Back to home</a></p>
    </div>`;
}

function renderEnrichedStoreDetail(store) {
  const rating  = parseFloat(store.rating) || 0;
  const reviews = parseInt(store.review_count) || 0;
  const ratingSnippet = rating > 0 ? ` Rated ${rating.toFixed(1)}/5 by ${reviews} reviewers.` : '';
  setPageMeta(
    `${store.name} — ${store.city}, ${store.state} | SA Bin Finder`,
    `Visit ${store.name} in ${store.city}, ${store.state}.${ratingSnippet} Get directions, accepted donations, pickup scheduling & AI-scored reviews.`,
    `/store.html?pid=${encodeURIComponent(store.place_id || '')}`
  );
  injectStoreSchema(store);

  const stateSlug   = store.state.toLowerCase().replace(/\s+/g, '-');
  const bcStateLink = document.getElementById('breadcrumbStateLink');
  const bcStateName = document.getElementById('breadcrumbStateName');
  const bcStore     = document.getElementById('breadcrumbStore');
  if (bcStateLink) bcStateLink.href = `state.html?state=${stateSlug}`;
  if (bcStateName) bcStateName.textContent = store.state;
  if (bcStore)     bcStore.textContent     = store.name;

  const reviewCount = parseInt(store.review_count) || 0;

  const ratingHtml = rating > 0 ? `
    <div class="detail-rating">
      ${starsHtml(rating)}
      <span class="detail-rating-num">${rating.toFixed(1)}</span>
      <span class="detail-rating-cnt">&nbsp;(${reviewCount.toLocaleString()} Google reviews)</span>
    </div>` : '';

  const scoreBars = [
    scoreBar('Donation Experience', store.donations_score),
    scoreBar('Friendly Staff',      store.friendly_staff_score),
    scoreBar('Cleanliness',         store.cleanliness_score),
  ].filter(Boolean).join('');

  const scoresSection = scoreBars ? `
    <div class="detail-section">
      <div class="detail-section-title">AI-Powered Insights</div>
      <div class="score-bars">${scoreBars}</div>
      <p class="score-note">&#129302; Scores from AI analysis of Google reviews</p>
    </div>` : '';

  const itemTags = (store.accepted_items || [])
    .map(i => `<span class="tag">${escHtml(i)}</span>`).join('');

  const reviewCards = (store.top_reviews || []).slice(0, 3).map(r => {
    const rStars = parseFloat(r.rating) || 0;
    const rDate  = r.date ? fmtDate(r.date) : '';
    const text   = escHtml(r.text || '');
    const excerpt = text.length > 400 ? text.slice(0, 400) + '&hellip;' : text;
    return `
      <div class="review-card">
        <div class="review-header">
          <span class="review-author">${escHtml(r.author || 'Reviewer')}</span>
          <span class="review-stars">${starsHtml(rStars)}</span>
          ${rDate ? `<span class="review-date">${rDate}</span>` : ''}
        </div>
        <p class="review-text">${excerpt}</p>
      </div>`;
  }).join('');

  const reviewsSection = reviewCards ? `
    <div class="detail-section">
      <div class="detail-section-title">Customer Reviews</div>
      <div class="reviews-list">${reviewCards}</div>
      ${store.reviews_link ? `<a href="${store.reviews_link}" target="_blank" rel="noopener" class="btn btn-outline" style="margin-top:14px; display:inline-block;">Read All Reviews on Google &#8599;</a>` : ''}
    </div>` : '';

  document.getElementById('storeDetailContainer').innerHTML = `
    <div class="store-detail-card">
      <div class="store-detail-header">
        <div class="store-detail-logo">SA</div>
        <div class="store-detail-title">
          <h1>${escHtml(store.name)}</h1>
          <div class="city-state">${escHtml(store.city)}, ${escHtml(store.state)} ${escHtml(store.zip)}${store.county ? ` &middot; ${escHtml(store.county)} County` : ''}</div>
          ${ratingHtml}
        </div>
      </div>
      <div class="store-detail-body">

        <div class="detail-section">
          <div class="detail-section-title">Location</div>
          <div class="info-row"><span class="icon">&#128205;</span><span>${escHtml(store.address)}, ${escHtml(store.city)}, ${escHtml(store.state)} ${escHtml(store.zip)}</span></div>
          ${store.location_link ? `<div style="margin-top:12px;"><a href="${store.location_link}" target="_blank" rel="noopener" class="btn btn-outline">&#128205; View on Google Maps</a></div>` : ''}
        </div>

        ${scoresSection}

        <div class="detail-section">
          <div class="detail-section-title">Donate Goods</div>
          <p style="color:var(--muted); font-size:0.9rem; margin-bottom:14px;">Schedule a free donation pickup right from your home — Salvation Army picks it up at no charge.</p>
          <a href="${store.donation_pickup_url}" target="_blank" rel="noopener" class="btn btn-primary">&#128666; Schedule Free Pickup</a>
        </div>

        <div class="detail-section">
          <div class="detail-section-title">Accepted Donations</div>
          <div class="store-card-tags" style="margin:0;">${itemTags}</div>
        </div>

        ${reviewsSection}

        <div style="text-align:center; padding-top:8px; font-size:0.83rem; color:var(--muted);">
          <a href="submit.html" style="color:var(--muted);">&#9999; Suggest a correction</a>
        </div>

      </div>
    </div>
    <a href="state.html?state=${stateSlug}" class="btn btn-outline">&#8592; All ${escHtml(store.state)} stores</a>
  `;
}

function renderLegacyStoreDetail(store) {
  setPageMeta(
    `${store.name} — ${store.city}, ${store.state} | SA Bin Finder`,
    `Visit ${store.name} in ${store.city}, ${store.state}. View hours, accepted donations, and get directions to this Salvation Army thrift store.`,
    `/store.html?id=${store.id}`
  );

  const bcStateLink = document.getElementById('breadcrumbStateLink');
  const bcStateName = document.getElementById('breadcrumbStateName');
  const bcStore     = document.getElementById('breadcrumbStore');
  if (bcStateLink) bcStateLink.href = `state.html?state=${store.slug}`;
  if (bcStateName) bcStateName.textContent = store.state;
  if (bcStore)     bcStore.textContent     = store.name;

  const hoursRows = Object.entries(store.hours).map(([day, time]) =>
    `<div class="hours-day">${day}</div><div class="hours-time">${time}</div>`
  ).join('');

  const features = store.features.map(f => `<span class="tag">${f}</span>`).join('');

  const verifiedBadge = store.verified
    ? `<span class="badge-verified" style="margin-top:8px; display:inline-block;">&#10003; Verified Listing</span>`
    : `<span style="color:rgba(255,255,255,0.45); font-size:0.8rem; margin-top:6px; display:block;">Community Submitted</span>`;

  document.getElementById('storeDetailContainer').innerHTML = `
    <div class="store-detail-card">
      <div class="store-detail-header">
        <div class="store-detail-logo">SA</div>
        <div class="store-detail-title">
          <h1>${store.name}</h1>
          <div class="city-state">${store.city}, ${store.state} ${store.zip}</div>
          ${verifiedBadge}
        </div>
      </div>
      <div class="store-detail-body">

        <div class="detail-section">
          <div class="detail-section-title">Contact &amp; Location</div>
          <div class="info-row"><span class="icon">&#128205;</span><span>${store.address}, ${store.city}, ${store.state} ${store.zip}</span></div>
          <div class="info-row"><span class="icon">&#128222;</span><a href="tel:${store.phone.replace(/\D/g,'')}" style="color:var(--red)">${store.phone}</a></div>
        </div>

        <div class="detail-section">
          <div class="detail-section-title">Pricing &amp; Restocks</div>
          <div class="info-row"><span class="icon">&#9878;</span><span>Priced at <strong>${store.pricing}</strong></span></div>
          <div class="info-row"><span class="icon">&#128260;</span><span>Restocks: <strong>${store.restock_days.join(', ')}</strong></span></div>
        </div>

        <div class="detail-section">
          <div class="detail-section-title">Store Hours</div>
          <div class="hours-grid">${hoursRows}</div>
        </div>

        <div class="detail-section">
          <div class="detail-section-title">About This Store</div>
          <p style="color:var(--text);line-height:1.75;">${store.description}</p>
        </div>

        <div class="detail-section">
          <div class="detail-section-title">What You'll Find</div>
          <div class="store-card-tags">${features}</div>
        </div>

        <div style="text-align:center; padding-top:8px; font-size:0.83rem; color:var(--muted);">
          <a href="submit.html?correction=${store.id}" style="color:var(--muted);">&#9999; Suggest a correction</a>
          &nbsp;&bull;&nbsp;
          <span>Added ${fmtDate(store.added)}</span>
        </div>

      </div>
    </div>

    <a href="state.html?state=${store.slug}" class="btn btn-outline">
      &#8592; All ${store.state} stores
    </a>
  `;
}

/* ============================================================
   PAGE: SUBMIT A STORE
   ============================================================ */

function initSubmitPage() {
  const stateSelect = document.getElementById('storeState');
  if (stateSelect) {
    stateSelect.innerHTML = `<option value="">Select a state...</option>` +
      window.SAData.states.map(s => `<option value="${s.name}">${s.name}</option>`).join('');
  }

  const hoursEl = document.getElementById('hoursSection');
  if (hoursEl) {
    const days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
    let html = '';
    for (let i = 0; i < days.length; i += 2) {
      html += `<div class="form-row">`;
      for (let j = i; j < Math.min(i + 2, days.length); j++) {
        html += `
          <div class="form-group">
            <label class="form-label" for="h_${days[j]}">${days[j]}</label>
            <input type="text" class="form-input" id="h_${days[j]}" name="h_${days[j]}"
              placeholder="e.g. 9:00 AM – 6:00 PM or Closed">
          </div>
        `;
      }
      html += `</div>`;
    }
    hoursEl.innerHTML = html;
  }

  const form = document.getElementById('storeSubmitForm');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      let valid = true;
      form.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
          field.style.borderColor = 'var(--red)';
          valid = false;
        } else {
          field.style.borderColor = '';
        }
      });
      if (!valid) {
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
      }
      document.getElementById('formWrapper').style.display = 'none';
      const success = document.getElementById('successBox');
      success.classList.add('show');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}
