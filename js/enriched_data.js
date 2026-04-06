/* ============================================================
   SA Directory — Enriched Store Data Loader
   Loads enriched_stores_clean.json (all categories combined)
   and exposes window.SAEnriched + window._enrichedReady
   ============================================================ */

window.SAEnriched = null;

window._enrichedReady = new Promise(function (resolve) {
  fetch('js/enriched_stores_clean.json?v=6')
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (data) {
      window.SAEnriched = data;
      resolve(data);
    })
    .catch(function (err) {
      console.warn('[SA Directory] enriched_stores_clean.json load failed:', err);
      window.SAEnriched = [];
      resolve([]);
    });
});
