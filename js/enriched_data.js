/* ============================================================
   SA Bin Finder — Enriched Store Data Loader
   Asynchronously fetches enriched_stores.json (2,931 stores)
   and exposes window.SAEnriched + window._enrichedReady
   ============================================================ */

window.SAEnriched = null;

window._enrichedReady = new Promise(function (resolve) {
  fetch('js/enriched_stores.json')
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (data) {
      window.SAEnriched = data;
      resolve(data);
    })
    .catch(function (err) {
      console.warn('[SA Bin Finder] enriched_stores.json load failed:', err);
      window.SAEnriched = [];
      resolve([]);
    });
});
