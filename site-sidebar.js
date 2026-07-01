(function () {
  if (document.querySelector('.article-sidebar')) return;

  const script = document.currentScript;
  const rootUrl = script ? new URL('.', script.src) : new URL('/', window.location.href);
  const isPt = (document.documentElement.lang || '').toLowerCase().startsWith('pt');

  const page = (path) => new URL(path, rootUrl).href;
  const languageRoot = isPt ? 'pt-br/' : '';
  const articlesRoot = isPt ? 'pt-br/artigos/' : 'artigos/';

  const labels = isPt ? {
    aria: 'Navegação do portal',
    summary: 'Engenharia mecânica, elementos de máquinas, ferramentas didáticas e projetos do LASME.',
    portal: 'Portal',
    overview: ['Visão geral', 'Roteiro de estudo e proposta do portal'],
    recent: ['Publicações recentes', 'Novos artigos e atualizações'],
    technical: ['Conteúdo técnico', 'Principais trilhas de leitura'],
    contact: ['Contato', 'Autoria e vínculos institucionais'],
    projects: 'Projetos',
    engrenarium: ['Projetos', 'Página de portfólio de todos os projetos'],
    engrenariumSoftware: ['Engrenarium software', 'Página do software completo para planetárias'],
    engrenariumWeb: ['Engrenarium Web', 'Abrir o simulador no navegador'],
    powertrain: ['Powertrain Interativo', 'Motor, câmbio, diferencial e velocidades nas rodas'],
    lasmeGroup: 'LASME',
    lasme: ['LASME/UFSJ', 'Laboratório de Sistemas Mecânicos'],
    about: ['Sobre o portal', 'Contexto acadêmico e autoria'],
    articles: 'Artigos',
    recentArticles: ['Artigos recentes', 'Powertrain, cames e transmissões'],
    gears: ['Engrenagens e trens', 'Perfis, relações e análise de trens'],
    planetary: ['Engrenagens planetárias', 'Caso geral, aplicações e diferenciais'],
    cams: ['Cames e movimento', 'Seguidores, curvas e projeto analítico'],
    index: ['Índice completo', 'Todos os artigos técnicos por tema']
  } : {
    aria: 'Portal navigation',
    summary: 'Mechanical engineering, machine elements, teaching tools and LASME projects.',
    portal: 'Portal',
    overview: ['Overview', 'Study path and purpose of the portal'],
    recent: ['Recent publications', 'Newest articles and updates'],
    technical: ['Technical content', 'Main reading tracks'],
    contact: ['Contact', 'Authorship and institutional links'],
    projects: 'Projects',
    engrenarium: ['Projects', 'Portfolio page for all projects'],
    engrenariumSoftware: ['Engrenarium software', 'Full software page for planetary gears'],
    engrenariumWeb: ['Engrenarium Web', 'Open the browser simulator'],
    powertrain: ['Interactive Powertrain', 'Engine, gearbox, differential and wheel speeds'],
    lasmeGroup: 'LASME',
    lasme: ['LASME/UFSJ', 'Mechanical Systems Laboratory'],
    about: ['About the portal', 'Academic context and authorship'],
    articles: 'Articles',
    recentArticles: ['Recent articles', 'Powertrain, cams and transmissions'],
    gears: ['Gears and trains', 'Profiles, ratios and gear train analysis'],
    planetary: ['Planetary gears', 'General case, applications and differentials'],
    cams: ['Cams and motion', 'Followers, curves and analytical design'],
    index: ['Complete index', 'All technical articles by theme']
  };

  const item = (href, text, attrs = '') => `
    <li>
      <a href="${href}"${attrs}>
        <span class="sidebar-link-title">${text[0]}</span>
        <span class="sidebar-link-note">${text[1]}</span>
      </a>
    </li>`;

  const group = (title, items) => `
    <div class="article-group">
      <h3>${title}</h3>
      <ul class="article-sidebar-list">${items.join('')}</ul>
    </div>`;

  const home = page(`${languageRoot}index.html`);
  const articlesIndex = page(`${articlesRoot}index.html`);

  const sidebar = document.createElement('aside');
  sidebar.className = 'article-sidebar';
  sidebar.id = 'article-sidebar';
  sidebar.setAttribute('aria-label', labels.aria);
  sidebar.innerHTML = `
    <div class="article-sidebar-header">
      <h2>Barbudenge</h2>
      <p>${labels.summary}</p>
    </div>
    <div class="article-sidebar-content">
      ${group(labels.portal, [
        item(`${home}#portal`, labels.overview),
        item(`${home}#recentes`, labels.recent),
        item(`${home}#artigos`, labels.technical),
        item(`${home}#contato`, labels.contact)
      ])}
      ${group(labels.projects, [
        item(page(`${languageRoot}engrenarium.html`), labels.engrenarium),
        item(isPt ? 'https://barbudenge.github.io/lasmeufsj/pt-br/engrenarium/' : 'https://barbudenge.github.io/lasmeufsj/engrenarium/', labels.engrenariumSoftware, ' target="_blank" rel="noopener"'),
        item('https://barbudenge.github.io/engrenarium/', labels.engrenariumWeb, ' target="_blank" rel="noopener"'),
        item(page(`${articlesRoot}powertrain-interativo.html`), labels.powertrain, ' target="_blank" rel="noopener"')
      ])}
      ${group(labels.lasmeGroup, [
        item(isPt ? 'https://barbudenge.github.io/lasmeufsj/pt-br/' : 'https://barbudenge.github.io/lasmeufsj/', labels.lasme),
        item(page(`${languageRoot}sobre.html`), labels.about)
      ])}
      ${group(labels.articles, [
        item(`${articlesIndex}#artigos-recentes`, labels.recentArticles),
        item(`${articlesIndex}#fundamentos-engrenagens`, labels.gears),
        item(page(`${articlesRoot}engrenagens-planetarias.html`), labels.planetary),
        item(page(`${articlesRoot}cames.html`), labels.cams),
        item(`${articlesIndex}#indice-completo`, labels.index)
      ])}
    </div>`;

  const content = document.createElement('div');
  content.className = 'site-content';

  const layout = document.createElement('div');
  layout.className = 'site-layout';

  const bodyChildren = Array.from(document.body.children).filter((child) => child !== script);
  bodyChildren.forEach((child) => content.appendChild(child));
  layout.append(sidebar, content);
  document.body.insertBefore(layout, script || null);
})();
