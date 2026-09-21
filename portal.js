// Progressive enhancement: every article and link remains available without JavaScript.
(() => {
  const form = document.querySelector('[data-catalog-filter]');
  if (!form) return;
  const search = form.querySelector('input');
  const topic = form.querySelector('select');
  const cards = [...document.querySelectorAll('[data-topic]')];
  const status = document.querySelector('[data-result-count]');
  const empty = document.querySelector('[data-empty]');
  const pt = document.documentElement.lang.startsWith('pt');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const update = () => {
    const words = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      const matches = (!topic.value || card.dataset.topic === topic.value) && words.every(word => normalize(card.textContent).includes(word));
      card.hidden = !matches;
      if (matches) count++;
    });
    status.textContent = pt ? `${count} de ${cards.length} artigos` : `${count} of ${cards.length} articles`;
    empty.hidden = count !== 0;
  };
  form.hidden = false;
  form.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', update);
  topic.addEventListener('change', update);
  form.addEventListener('reset', () => { search.value = ''; topic.value = ''; update(); });
  update();
})();
