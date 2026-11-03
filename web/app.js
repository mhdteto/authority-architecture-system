(() => {
  'use strict';
  const block = document.getElementById('explorer-data');
  if (!block) return;
  const data = JSON.parse(block.textContent);
  const byId = (id) => document.getElementById(id);
  const el = (tag, text, cls) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = String(text);
    if (cls) node.className = cls;
    return node;
  };
  const contains = (row, query) => !query || Object.values(row).join(' ').toLocaleLowerCase().includes(query);
  const empty = (parent, message) => parent.append(el('p', message, 'empty'));
  const tabs = [...document.querySelectorAll('[data-tab]')];
  const panels = [...document.querySelectorAll('[data-panel]')];
  const selectTab = (name, focus = false, updateHash = true) => {
    tabs.forEach((tab) => {
      const selected = tab.dataset.tab === name;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focus) tab.focus();
    });
    panels.forEach((panel) => { panel.hidden = panel.dataset.panel !== name; });
    if (updateHash) history.replaceState(null, '', '#' + name);
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab.dataset.tab));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); selectTab(tabs[next].dataset.tab, true); }
    });
  });
  const applyHash = () => {
    const name = location.hash.slice(1);
    if (tabs.some((tab) => tab.dataset.tab === name)) {
      selectTab(name, false, false);
      document.querySelector('.workspace').scrollIntoView({ block: 'start' });
    }
  };
  selectTab('overview', false, false);
  window.addEventListener('hashchange', applyHash);

  function renderIdentity() {
    const status = byId('identity-status').value;
    const query = byId('identity-search').value.trim().toLocaleLowerCase();
    const rows = data.identity.results.filter((row) => (status === 'all' || row.status === status) && contains(row, query));
    const body = byId('identity-rows'); body.replaceChildren();
    rows.forEach((row) => {
      const tr = el('tr');
      [row.market + ' / ' + row.language, row.field, row.canonical || '—', row.observed || 'Missing'].forEach((value) => tr.append(el('td', value)));
      const statusCell = el('td'); statusCell.append(el('span', row.status.replaceAll('_', ' '), 'status ' + row.status));
      tr.append(statusCell); body.append(tr);
    });
    if (!rows.length) { const tr = el('tr'); const cell = el('td', 'No matching field observations.'); cell.colSpan = 5; tr.append(cell); body.append(tr); }
    byId('identity-count').textContent = rows.length + ' field observations across the supplied fictional profiles';
  }
  byId('identity-status').addEventListener('change', renderIdentity);
  byId('identity-search').addEventListener('input', renderIdentity);

  function renderEvidence() {
    const status = byId('evidence-status').value;
    const claims = data.evidence.claims.filter((claim) => status === 'all' || claim.statuses.includes(status));
    const parent = byId('evidence-cards'); parent.replaceChildren();
    claims.forEach((claim) => {
      const card = el('article', undefined, 'claim'); card.append(el('h4', claim.claim_text));
      card.append(el('p', claim.entity + ' · ' + claim.claim_id));
      const badges = el('div', undefined, 'badges');
      claim.statuses.forEach((status) => badges.append(el('span', status, 'status ' + (status === 'conflicting sources' ? 'conflict' : status === 'missing evidence' ? 'missing' : ''))));
      card.append(badges, el('p', claim.evidence.length + ' supplied reviews · ' + claim.independent_support_publishers + ' independent-support publisher(s) by input declaration'));
      if (claim.evidence.length) {
        const details = el('details'); details.append(el('summary', 'Inspect the supplied reviews'));
        const list = el('ul');
        claim.evidence.forEach((review) => {
          const li = el('li');
          li.append(el('strong', review.publisher + ' — ' + review.support_status), el('p', review.relationship + ' · access: ' + (review.accessed_on || 'not recorded')), el('p', review.review_note), el('code', review.source_url));
          list.append(li);
        });
        details.append(list); card.append(details);
      } else card.append(el('p', 'No evidence rows were supplied for this claim.'));
      parent.append(card);
    });
    if (!claims.length) empty(parent, 'No matching claims.');
    byId('evidence-count').textContent = claims.length + ' fictional claim(s) shown';
  }
  byId('evidence-status').addEventListener('change', renderEvidence);

  const matchesCitation = (row) => (byId('citation-language').value === 'all' || row.language === byId('citation-language').value) && (byId('citation-market').value === 'all' || row.market === byId('citation-market').value);
  function renderCitations() {
    const groups = data.citations.groups.filter(matchesCitation);
    const answers = data.citations.answers.filter(matchesCitation);
    const parent = byId('citation-groups'); parent.replaceChildren();
    groups.forEach((group) => {
      const card = el('article', undefined, 'group-card');
      card.append(el('h4', group.language + ' / ' + group.market), el('strong', Math.round(group.cited_answer_rate * 100) + '%'), el('p', group.cited_answer_count + ' cited answers ÷ ' + group.answer_count + ' all answers'), el('p', group.explicit_citation_count + ' normalized explicit citation(s) summed across answers'), el('p', group.engine + ' · ' + group.model + ' · ' + group.interface), el('p', group.collected_from + ' to ' + group.collected_to + ' · fabricated observations'));
      parent.append(card);
    });
    if (!groups.length) empty(parent, 'No observations for this language/market combination. This is missing data, not a zero citation rate.');
    const body = byId('citation-rows'); body.replaceChildren();
    answers.forEach((answer) => {
      const row = el('tr'); row.append(el('td', answer.answer_id), el('td', answer.market + ' / ' + answer.language), el('td', answer.answer_text));
      const urls = el('td');
      if (!answer.citation_urls.length) urls.textContent = 'No explicit citation';
      answer.citation_urls.forEach((url) => urls.append(el('code', url)));
      row.append(urls); body.append(row);
    });
    if (!answers.length) { const tr = el('tr'); const cell = el('td', 'No matching supplied answers.'); cell.colSpan = 4; tr.append(cell); body.append(tr); }
    byId('citation-count').textContent = answers.length + ' simulated answers · ' + groups.length + ' separate group(s) · no pooled rate';
    byId('citation-export').disabled = !answers.length;
  }
  byId('citation-language').addEventListener('change', renderCitations);
  byId('citation-market').addEventListener('change', renderCitations);
  byId('citation-export').addEventListener('click', () => {
    const answers = data.citations.answers.filter(matchesCitation);
    if (!answers.length) return;
    const fields = ['answer_id','engine','model','interface','language','market','collected_on','answer_text','citation_count','citation_urls'];
    const cell = (value) => {
      let text = Array.isArray(value) ? JSON.stringify(value) : String(value ?? '');
      if (/^[\s\uFEFF]*[=+@-]/u.test(text)) text = "'" + text;
      return '"' + text.replaceAll('"', '""') + '"';
    };
    const csv = [fields.map(cell).join(','), ...answers.map((row) => fields.map((field) => cell(row[field])).join(','))].join('\r\n') + '\r\n';
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    const link = el('a'); link.href = url; link.download = 'fictional-citation-observations.csv';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });

  const markets = [...new Set(data.sources.map((row) => row.market))].sort();
  markets.forEach((market) => { const option = el('option', market); option.value = market; byId('source-market').append(option); });
  function renderSources() {
    const market = byId('source-market').value;
    const query = byId('source-search').value.trim().toLocaleLowerCase();
    const sources = data.sources.filter((row) => (market === 'all' || row.market === market) && contains(row, query));
    const parent = byId('source-cards'); parent.replaceChildren();
    sources.forEach((source) => {
      const card = el('article', undefined, 'source-card'); card.append(el('span', source.market + ' / ' + source.category, 'label'));
      const title = el('h4'); const link = el('a', source.name); link.href = source.url; link.rel = 'noopener noreferrer'; title.append(link); card.append(title, el('p', source.publisher), el('p', source.supports));
      const detail = el('details'); detail.append(el('summary', 'Scope and verification notes'), el('p', source.limits), el('p', source.access_note), el('p', source.verification.replaceAll('_', ' ') + ' · ' + source.checked_on), el('p', source.verification_note));
      const reference = el('a', 'Primary verification reference ↗'); reference.href = source.verification_url; reference.rel = 'noopener noreferrer'; detail.append(reference); card.append(detail); parent.append(card);
    });
    if (!sources.length) empty(parent, 'No matching catalogue entries.');
    byId('source-count').textContent = sources.length + ' real public entry point(s) · verify the particular record separately';
  }
  byId('source-market').addEventListener('change', renderSources);
  byId('source-search').addEventListener('input', renderSources);

  renderIdentity(); renderEvidence(); renderCitations(); renderSources(); applyHash();
})();
