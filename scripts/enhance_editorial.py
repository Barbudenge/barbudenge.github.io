"""Add static article navigation, without modifying shared application assets."""
from pathlib import Path
import re
import html

ROOT = Path(__file__).resolve().parents[1]
for folder in [ROOT/'artigos', ROOT/'pt-br/artigos']:
    pt = folder.parent.name == 'pt-br'
    for path in folder.glob('*.html'):
        if path.name in ['index.html','conferir-resultados-planetaria.html']:
            continue
        text = path.read_text(encoding='utf-8')
        def responsive_table(match):
            preceding = text[:match.start()]
            if re.search(r'<div class="table-scroll"[^>]*>\s*$', preceding):
                return match[0]
            return '<div class="table-scroll" tabindex="0" role="region" aria-label="'+('Tabela com rolagem horizontal' if pt else 'Horizontally scrollable table')+'">'+match[0]+'</div>'
        text = re.sub(r'<table\b.*?</table>', responsive_table, text, flags=re.S)
        if 'class="article-toc"' in text:
            path.write_text(text,encoding='utf-8')
            continue
        text = re.sub(r'\s*<link rel="stylesheet" href="[^"]*site-sidebar.css"\s*/?>','',text)
        text = re.sub(r'\s*<script src="[^"]*site-sidebar.js"></script>','',text)
        text = text.replace('</head>','<link rel="stylesheet" href="/editorial.css">\n</head>')
        text = text.replace('<body>', '<body>\n<a class="editorial-skip" href="#article-content">'+('Pular para o artigo' if pt else 'Skip to article')+'</a>')
        match = re.search(r'(<article\b[^>]*>)(.*?)(</article>)',text,re.S)
        if not match:
            raise ValueError(f'No article in {path}')
        opening, body, closing = match.groups()
        opening = opening.replace('<article', '<article id="article-content"',1)
        entries = []
        used = set(re.findall(r'\bid="([^"]+)"',text))
        def heading(m):
            attrs, title = m.groups()
            existing = re.search(r'\bid="([^"]+)"',attrs)
            anchor = existing[1] if existing else f'leitura-{len(entries)+1}'
            if not existing:
                while anchor in used:
                    anchor += '-section'
                used.add(anchor)
            entries.append((anchor, html.unescape(re.sub('<[^>]+>','',title))))
            return '<h2'+attrs+(f' id="{anchor}"' if not existing else '')+'>'+title+'</h2>'
        body = re.sub(r'<h2([^>]*)>(.*?)</h2>',heading,body,flags=re.S)
        toc = '<details class="article-toc"><summary>'+('Neste artigo' if pt else 'In this article')+'</summary><nav aria-label="'+('Seções do artigo' if pt else 'Article sections')+'"><ol>'+''.join(f'<li><a href="#{anchor}">{html.escape(title)}</a></li>' for anchor,title in entries)+'</ol></nav></details>'
        correction = '<div class="article-correction"><p>'+('Dúvidas sobre uma equação ou resultado? Envie o endereço desta página e os dados do seu cálculo para ' if pt else 'Questions about an equation or result? Send this page address and your calculation inputs to ')+'<a href="mailto:arturavelar@ufsj.edu.br">arturavelar@ufsj.edu.br</a>. · <a href="../sobre.html">'+('Sobre o autor' if pt else 'About the author')+'</a> · <a href="../privacy.html">'+('Privacidade' if pt else 'Privacy')+'</a></p></div>'
        text = text[:match.start()]+opening+toc+body+correction+closing+text[match.end():]
        path.write_text(text,encoding='utf-8')
print('Article navigation updated; applications untouched.')
