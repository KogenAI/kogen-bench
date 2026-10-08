(() => {
  const form = document.querySelector('[data-round-filters]');
  const rows = [...document.querySelectorAll('[data-round-row]')];
  if (!form || !rows.length) return;
  const query = form.querySelector('[data-round-query]');
  const status = form.querySelector('[data-round-status]');
  const family = form.querySelector('[data-round-family]');
  const count = form.querySelector('[data-round-count]');
  const params = new URLSearchParams(location.search);
  query.value = params.get('q') || '';
  status.value = params.get('status') || '';
  family.value = params.get('family') || '';

  const apply = (writeUrl = true) => {
    const q = query.value.trim().toLowerCase();
    const s = status.value;
    const f = family.value;
    let visible = 0;
    for (const row of rows) {
      const match = (!q || row.dataset.search.toLowerCase().includes(q))
        && (!s || row.dataset.status === s)
        && (!f || row.dataset.families.split(' ').includes(f));
      row.hidden = !match;
      if (match) visible += 1;
    }
    count.textContent = visible === rows.length ? 'All registered entries' : 'Matching registered entries';
    if (writeUrl) {
      const next = new URLSearchParams();
      if (q) next.set('q', query.value.trim());
      if (s) next.set('status', s);
      if (f) next.set('family', f);
      history.replaceState(null, '', `${location.pathname}${next.size ? `?${next}` : ''}`);
    }
  };
  form.addEventListener('submit', (event) => event.preventDefault());
  query.addEventListener('input', () => apply());
  status.addEventListener('change', () => apply());
  family.addEventListener('change', () => apply());
  apply(false);
})();
