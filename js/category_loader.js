/* ============================================================
   Category Data Loader
   Fetches the right JSON file based on window.SA_CATEGORY
   and sets window.SACategoryData + resolves window._categoryReady
   ============================================================ */

(function () {
  const MAP = {
    thrift : 'js/thrift_stores.json',
    food   : 'js/food_pantries.json',
    rehab  : 'js/rehab_centers.json',
    all    : 'js/enriched_stores_clean.json'
  };

  const cat  = window.SA_CATEGORY || 'all';
  const file = MAP[cat] || MAP['all'];

  window._categoryReady = fetch(file + '?v=6')
    .then(r => r.json())
    .then(data => {
      window.SACategoryData = data;
      // Also expose as SAEnriched so existing helpers (starsHtml, scoreBar, etc.) work
      window.SAEnriched = data;
      return data;
    })
    .catch(err => {
      console.error('Category loader error:', err);
      window.SACategoryData = [];
      window.SAEnriched = [];
      return [];
    });
})();
