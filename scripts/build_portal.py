"""Build the bilingual editorial home/catalog from the existing article HTML.

Python standard library only. Never writes to applications or LASME.
Run from any directory: python scripts/build_portal.py
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://barbudenge.github.io'
esc = html.escape

def plain(value):
    return html.unescape(re.sub('<[^>]+>', '', value)).strip()

def article_data(folder):
    result = []
    for path in folder.glob('*.html'):
        if path.name == 'index.html':
            continue
        text = path.read_text(encoding='utf-8')
        title = plain(re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)[1])
        description = html.unescape(re.search(r'<meta name="description" content="([^"]+)"', text)[1])
        date = re.search(r'"datePublished"\s*:\s*"([^"]+)"', text)[1]
        body = re.search(r'<article\b[^>]*>(.*?)</article>', text, re.S)
        words = len(plain(body[1] if body else text).split())
        image = re.search(r'<img[^>]+src="([^"]+)"[^>]+alt="([^"]*)"', text)
        image_path = '/' + (path.parent / html.unescape(image[1])).resolve().relative_to(ROOT).as_posix() if image and not image[1].startswith('http') else '/figs/planet1.png'
        topic = 'cams' if ('came' in path.stem or 'camforge' in path.stem) else 'planetary' if any(s in path.stem for s in ['planet', 'ferguson', 'ravigneaux', 'allison', 'modelo-t', 'cvt']) else 'gears'
        result.append(dict(slug=path.name, title=title, description=description, date=date, minutes=max(1, round(words/200)), image=image_path, alt=html.unescape(image[2]) if image else title, topic=topic))
    return sorted(result, key=lambda a: (a['date'], a['slug']), reverse=True)

def head(title, description, path, counterpart, pt, schema=None):
    en, br = (counterpart, path) if pt else (path, counterpart)
    structured = json.dumps(schema or {'@context':'https://schema.org','@type':'WebPage','name':title,'url':BASE+path,'inLanguage':'pt-BR' if pt else 'en'}, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="{'pt-BR' if pt else 'en'}"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Barbudenge</title><meta name="description" content="{esc(description)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="google-site-verification" content="JUtHYIOjO9B2FTwzMsDgDWdLjIoQFGVocn-YMQuUfvs">
<meta name="google-adsense-account" content="ca-pub-5777194849710689">
<link rel="canonical" href="{BASE+path}">
<link rel="alternate" hreflang="en" href="{BASE+en}"><link rel="alternate" hreflang="pt-BR" href="{BASE+br}"><link rel="alternate" hreflang="x-default" href="{BASE+en}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{BASE+path}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/figs/engr-web.png">
<link rel="stylesheet" href="/portal.css"><script defer src="/portal.js"></script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5777194849710689" crossorigin="anonymous"></script>
<script type="application/ld+json">{structured}</script>
</head><body><a class="skip" href="#main">{'Pular para o conteúdo' if pt else 'Skip to content'}</a>
<header class="masthead"><div class="wrap top"><a class="brand" href="{'/pt-br/' if pt else '/'}">Barbu<span>denge</span></a>
<nav class="nav" aria-label="{'Navegação principal' if pt else 'Main navigation'}">
<a href="{'/pt-br/' if pt else '/'}artigos/">{'Artigos' if pt else 'Articles'}</a><a href="{'/pt-br/' if pt else '/'}#artigos">{'Trilhas de estudo' if pt else 'Learning paths'}</a><a href="{'/pt-br/' if pt else '/'}#projetos">{'Simuladores' if pt else 'Simulators'}</a><a href="{'/pt-br/' if pt else '/'}sobre.html">{'Sobre e contato' if pt else 'About & contact'}</a>
</nav><div class="languages" aria-label="{'Idioma' if pt else 'Language'}"><a href="{br}" lang="pt-BR" hreflang="pt-BR" {'aria-current="page"' if pt else ''}>PT</a><a href="{en}" lang="en" hreflang="en" {'' if pt else 'aria-current="page"'}>EN</a></div></div></header>'''

def footer(pt):
    home = '/pt-br/' if pt else '/'
    return f'''<footer class="footer"><div class="wrap"><span>© 2026 Barbudenge · {'Engenharia mecânica para estudar e experimentar' if pt else 'Mechanical engineering to study and explore'}</span><span><a href="{home}sobre.html">{'Autoria e contato' if pt else 'Author & contact'}</a> · <a href="{home}privacy.html">{'Privacidade' if pt else 'Privacy'}</a></span></div></footer></body></html>'''

def card(a, pt, image=True):
    prefix = '/pt-br/artigos/' if pt else '/artigos/'
    labels = {'cams':'Cames e movimento' if pt else 'Cams & motion','planetary':'Planetárias e transmissões' if pt else 'Planetary gears & transmissions','gears':'Engrenagens e fundamentos' if pt else 'Gears & fundamentals'}
    return f'''<article class="card" data-topic="{a['topic']}">{f'<img class="card-image" loading="lazy" src="{esc(a["image"])}" alt="{esc(a["alt"])}">' if image else ''}<div class="card-body"><span class="eyebrow">{labels[a['topic']]}</span><h3><a href="{prefix+a['slug']}">{esc(a['title'])}</a></h3><p>{esc(a['description'])}</p><p class="meta"><time datetime="{a['date']}">{a['date']}</time> · {a['minutes']} min {'de leitura' if pt else 'read'}</p><div class="links"><a href="{prefix+a['slug']}">{'Ler artigo' if pt else 'Read article'} →</a></div></div></article>'''

def home(pt, articles):
    root = '/pt-br/' if pt else '/'
    path = ROOT / ('pt-br/index.html' if pt else 'index.html')
    old = path.read_text(encoding='utf-8')
    # Keep the existing reference material and its incoming fragment links.
    archived = []
    for name, label in [('faq','Perguntas frequentes' if pt else 'Frequently asked questions'),('glossario','Glossário de mecanismos' if pt else 'Mechanisms glossary'),('livros','Livros e traduções' if pt else 'Books and translations')]:
        match = re.search(fr'<section id="{name}"[^>]*>.*?</section>', old, re.S)
        if match:
            content = match[0]
            # Old homepage assets were relative; generated pages use root-relative paths.
            content = re.sub(r'src="(?:\.\./)?figs/', 'src="/figs/', content)
            archived.append(f'<details class="archive-details"><summary>{label}</summary>{content}</details>')
    title = 'Engrenagens, cames e mecanismos na prática' if pt else 'Gears, cams and mechanisms in practice'
    description = 'Aprenda mecanismos com exemplos resolvidos, trilhas de artigos e os simuladores Engrenarium, CamForge e Powertrain Interativo.' if pt else 'Study mechanisms with worked examples, guided reading and the Engrenarium, CamForge and Interactive Powertrain simulators.'
    out = head(title, description, root, '/' if pt else '/pt-br/', pt)
    # Preserve the existing home-page analytics property.
    out = out.replace('</head>', '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-FJPKSBEZR2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-FJPKSBEZR2');</script></head>''')
    out += f'''<main id="main"><div class="wrap intro"><div><span class="eyebrow">{'Caderno de engenharia mecânica' if pt else 'Mechanical engineering notebook'}</span><h1>{'Entenda o movimento. Confira o cálculo.' if pt else 'Understand motion. Check the numbers.'}</h1><p>{'Engrenagens, transmissões e cames explicados com equações, figuras e exemplos resolvidos. Um percurso entre o mecanismo no papel e a simulação no navegador.' if pt else 'Gears, transmissions and cams explained through equations, diagrams and worked examples. A path from the mechanism on paper to a simulation in your browser.'}</p><div class="actions"><a class="button" href="#artigos">{'Escolher uma trilha' if pt else 'Choose a learning path'}</a><a href="#projetos">{'Abrir os simuladores' if pt else 'Open the simulators'} ↓</a></div></div><figure><img src="/figs/engre-web.png" width="1389" height="781" fetchpriority="high" alt="{'Interface do Engrenarium Web para estudo de engrenagens planetárias' if pt else 'Engrenarium Web interface for studying planetary gears'}"><figcaption>{'Do desenho ao resultado: explore entrada, saída e braço no Engrenarium.' if pt else 'From diagram to result: explore input, output and carrier motion in Engrenarium.'}</figcaption></figure></div>
<section class="section tools" id="projetos"><div class="wrap"><div class="section-head"><div><span class="eyebrow">{'Laboratório no navegador' if pt else 'Browser laboratory'}</span><h2>{'Três maneiras de experimentar' if pt else 'Three ways to experiment'}</h2></div><a href="{'/projects/pt-br/' if pt else '/projects/'}">{'Todos os projetos' if pt else 'All projects'} →</a></div><div class="grid">'''
    tools = [
      ('Engrenarium Web','/figs/engr-web.png','https://barbudenge.github.io/engrenarium/'+('pt-br/' if pt else ''),'engrenagens-planetarias.html','Investigue velocidades em planetárias. Compare o que acontece ao fixar a coroa, o sol ou o porta-satélites.' if pt else 'Investigate planetary gear speeds. Compare what happens when the ring, sun or carrier is fixed.'),
      ('CamForge','/figs/aulas/projcam1.jpg','https://barbudenge.github.io/camforge/'+('pt-br/' if pt else ''),'camforge-exemplo-correcao-descontinuidades.html','Explore leis de movimento e perfis de cames. Use os diagramas SVAJ para investigar a continuidade entre os trechos.' if pt else 'Explore motion laws and cam profiles. Use SVAJ diagrams to investigate continuity between segments.'),
      ('Powertrain Interativo' if pt else 'Interactive Powertrain','/figs/aulas/power1.png','https://barbudenge.github.io/lasmeufsj/powertrain/'+('pt-br/' if pt else ''),'powertrain-interativo.html','Acompanhe a rotação do motor até as rodas. Relacione marcha, diferencial e velocidade do veículo em reta e em curva.' if pt else 'Follow engine rotation all the way to the wheels. Connect gear selection, differential action and vehicle speed on straights and turns.')]
    for name,image,url,guide,desc in tools:
        out += f'<article class="card"><img class="card-image" src="{image}" alt="{name}" loading="lazy"><div class="card-body"><h3>{name}</h3><p>{desc}</p><div class="links"><a href="{url}">{"Abrir simulador" if pt else "Open simulator"} ↗</a><a href="{root}artigos/{guide}">{"Estudar um exemplo" if pt else "Study an example"} →</a></div></div></article>'
    out += f'</div></div></section><section class="section" id="artigos"><div class="wrap"><div class="section-head"><div><span class="eyebrow">{"Comece pelo que você quer aprender" if pt else "Start with what you want to learn"}</span><h2>{"Escolha seu percurso" if pt else "Choose your path"}</h2></div><a href="{root}artigos/">{len(articles)} {"artigos no acervo" if pt else "articles in the library"} →</a></div><div class="grid">'
    tracks = [
      ('01','Engrenagens e trens' if pt else 'Gears & gear trains','Como os dentes, os eixos comuns e o tipo de contato determinam velocidade e sentido de rotação.' if pt else 'How teeth, shared shafts and mesh types determine speed and direction.', [('engrenagens-funcoes-perfil-nomenclatura','Perfil, módulo e nomenclatura' if pt else 'Profile, module and terminology'),('trens-engrenagens-simples-compostos','Trens simples e compostos' if pt else 'Simple and compound trains'),('cambio-manual-trens-engrenagens','Aplicação: câmbio manual' if pt else 'Application: manual gearbox')]),
      ('02','Planetárias e transmissões' if pt else 'Planetary gears & transmissions','Aprenda a usar velocidades relativas ao braço antes de analisar conjuntos com vários estágios.' if pt else 'Learn to use speeds relative to the carrier before analysing multistage assemblies.', [('engrenagens-planetarias','Equação geral das planetárias' if pt else 'The general planetary equation'),('conferir-resultados-planetaria','Exemplo: conferir três configurações' if pt else 'Example: check three configurations'),('transmissao-allison-1000','Aplicação: Allison 1000' if pt else 'Application: Allison 1000')]),
      ('03','Cames e leis de movimento' if pt else 'Cams & motion laws','Ligue a especificação de deslocamento à velocidade, à aceleração e à geometria do perfil.' if pt else 'Connect the displacement specification to velocity, acceleration and profile geometry.', [('cames-nomenclatura-seguidores','Cames e seguidores' if pt else 'Cams and followers'),('cames-curvas-deslocamento','Curvas de deslocamento e SVAJ' if pt else 'Displacement curves and SVAJ'),('camforge-correcao-descontinuidades-curva-svaj','Aplicação: corrigir descontinuidades' if pt else 'Application: correcting discontinuities')])]
    for num,name,desc,links in tracks:
        out += f'<article class="track"><span class="number">{num} / {"TRILHA DE ESTUDO" if pt else "LEARNING PATH"}</span><h3>{name}</h3><p>{desc}</p><ol>'+''.join(f'<li><a href="{root}artigos/{slug}.html">{label}</a></li>' for slug,label in links)+'</ol></article>'
    out += f'''</div></div></section><section class="section"><div class="wrap feature"><div><span class="eyebrow">{'Exemplo resolvido' if pt else 'Worked example'}</span><h2>{'Mesmos dentes.<br>Três comportamentos.' if pt else 'Same teeth.<br>Three behaviours.'}</h2><p>{'Sol com 24 dentes, coroa com 72. Fixar um elemento diferente muda o resultado — e o sentido de rotação.' if pt else 'A 24-tooth sun and a 72-tooth ring. Fixing a different member changes the result — and the direction of rotation.'}</p><a href="{root}artigos/conferir-resultados-planetaria.html">{'Acompanhar o cálculo e conferir os resultados' if pt else 'Follow the calculation and check the results'} →</a></div><div><p class="result">1 200 → 300 rpm</p><p>{'Coroa fixa, entrada no sol e saída no braço: redução de 4:1. O guia compara esse resultado com sol fixo e braço fixo, e mostra como detectar erros de sinal.' if pt else 'Fixed ring, sun input and carrier output: a 4:1 reduction. The guide compares this result with a fixed sun and a fixed carrier, and shows how to detect sign errors.'}</p></div></div></section>
<section class="section" id="recentes"><div class="wrap"><div class="section-head"><div><span class="eyebrow">{'Para continuar estudando' if pt else 'Keep learning'}</span><h2>{'Publicações recentes' if pt else 'Recent articles'}</h2></div><a href="{root}artigos/">{'Explorar o acervo' if pt else 'Explore the library'} →</a></div><div class="grid">{''.join(card(a,pt) for a in articles[:3])}</div></div></section>
<section class="section" id="portal"><div class="wrap author"><div><span class="eyebrow">{'Quem escreve' if pt else 'Who writes'}</span><h2>Artur Henrique<br>de Freitas Avelar</h2><p>{'Professor da Universidade Federal de São João del-Rei. O portal reúne notas de aula adaptadas, análise de mecanismos e guias dos projetos ligados ao seu trabalho em ensino e desenvolvimento de ferramentas.' if pt else 'Professor at the Federal University of São João del-Rei. This portal brings together adapted teaching notes, mechanism analysis and guides to projects connected with his teaching and tool development.'}</p><a href="{root}sobre.html">{'Conhecer o autor e os critérios editoriais' if pt else 'About the author and editorial approach'} →</a></div><div id="contato"><span class="eyebrow">{'Dúvidas e correções' if pt else 'Questions & corrections'}</span><h3>{'Encontrou uma conta que não fecha?' if pt else 'Found a calculation that does not add up?'}</h3><p>{'Envie o endereço do artigo, os dados usados e o resultado que você encontrou. Isso ajuda a localizar erros de unidade, convenção de sinal ou hipótese de cálculo.' if pt else 'Send the article address, the inputs you used and the result you obtained. This helps identify unit errors, sign conventions or calculation assumptions.'}</p><a href="mailto:arturavelar@ufsj.edu.br">arturavelar@ufsj.edu.br</a><p style="margin-top:20px"><a href="https://barbudenge.github.io/lasmeufsj/{'pt-br/' if pt else ''}">LASME / UFSJ ↗</a> · <a href="https://github.com/Barbudenge">GitHub ↗</a></p></div></div></section>
<section class="section"><div class="wrap"><h2>{'Material de consulta' if pt else 'Reference shelf'}</h2>{''.join(archived)}</div></section></main>'''
    path.write_text(out+footer(pt), encoding='utf-8')

def catalog(pt, articles):
    root = '/pt-br/' if pt else '/'
    title = 'Artigos de engenharia mecânica' if pt else 'Mechanical engineering articles'
    description = 'Exemplos, fundamentos e guias de engrenagens, planetárias, transmissões e cames. Busque no acervo por tema ou palavra.' if pt else 'Worked examples, fundamentals and guides to gears, planetary systems, transmissions and cams. Search the library by topic or keyword.'
    schema = {'@context':'https://schema.org','@type':'CollectionPage','name':title,'url':BASE+root+'artigos/','inLanguage':'pt-BR' if pt else 'en','mainEntity':{'@type':'ItemList','numberOfItems':len(articles),'itemListElement':[{'@type':'ListItem','position':i+1,'name':a['title'],'url':BASE+root+'artigos/'+a['slug']} for i,a in enumerate(articles)]}}
    out = head(title,description,root+'artigos/',('/' if pt else '/pt-br/')+'artigos/',pt,schema)
    out += f'''<main id="main" class="wrap"><div class="catalog-head"><span class="eyebrow">{'Biblioteca técnica' if pt else 'Technical library'}</span><h1>{title}</h1><p>{description}</p><p><a href="{root}#artigos">{'Está começando? Siga uma trilha de estudo.' if pt else 'Getting started? Follow a learning path.'}</a></p></div>
<form class="filters" data-catalog-filter hidden role="search"><div><label for="search">{'Buscar nos títulos e resumos' if pt else 'Search titles and summaries'}</label><input id="search" type="search" placeholder="{'Ex.: velocidade, planetária, SVAJ' if pt else 'E.g. speed, planetary, SVAJ'}"></div><div><label for="topic">{'Assunto' if pt else 'Topic'}</label><select id="topic"><option value="">{'Todos os assuntos' if pt else 'All topics'}</option><option value="gears">{'Engrenagens e fundamentos' if pt else 'Gears & fundamentals'}</option><option value="planetary">{'Planetárias e transmissões' if pt else 'Planetary gears & transmissions'}</option><option value="cams">{'Cames e movimento' if pt else 'Cams & motion'}</option></select></div><button type="reset">{'Limpar' if pt else 'Clear'}</button></form>
<p data-result-count role="status" aria-live="polite">{len(articles)} {'artigos' if pt else 'articles'}</p><p class="empty" data-empty hidden>{'Nenhum artigo encontrado. Tente outro termo ou limpe os filtros.' if pt else 'No articles found. Try another term or clear the filters.'}</p><div id="indice-completo"><span id="artigos-recentes"></span><div class="grid catalog-grid">'''
    for a in articles:
        rendered = card(a,pt,False).replace('<h3>', '<h2>').replace('</h3>', '</h2>')
        if a['slug'] == 'engrenagens-funcoes-perfil-nomenclatura.html':
            rendered = rendered.replace('class="card"', 'id="fundamentos-engrenagens" class="card"', 1)
        out += rendered
    out += '</div></div></main>'+footer(pt)
    (ROOT / root.strip('/') / 'artigos/index.html').write_text(out, encoding='utf-8')

if __name__ == '__main__':
    for pt in [False,True]:
        articles = article_data(ROOT / ('pt-br/artigos' if pt else 'artigos'))
        home(pt,articles)
        catalog(pt,articles)
        print(f'{"PT" if pt else "EN"}: {len(articles)} articles')
