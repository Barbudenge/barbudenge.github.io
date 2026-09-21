"""Check editorial HTML, local assets, fragments, metadata and sitemap coverage."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://barbudenge.github.io'
EXTERNAL_APPS = ('/lasmeufsj/', '/engrenarium/')

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.ids=[]; self.images=[]; self.h1=0; self.canonical=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='img':
            self.images.append(a)
            self.links.append(a.get('src',''))
        if tag in ('script','link'):
            if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a['href'])
            if a.get('src'): self.links.append(a['src'])
            if a.get('rel')=='stylesheet': self.links.append(a['href'])

files=[ROOT/'index.html',ROOT/'pt-br/index.html']+list((ROOT/'artigos').glob('*.html'))+list((ROOT/'pt-br/artigos').glob('*.html'))
pages={p:Page(p.read_text(encoding='utf-8')) for p in files}
errors=[]
for file,page in pages.items():
    name=file.relative_to(ROOT).as_posix()
    if page.h1!=1: errors.append(f'{name}: {page.h1} h1 headings')
    if len(page.canonical)!=1: errors.append(f'{name}: missing/duplicate canonical')
    if len(page.ids)!=len(set(page.ids)): errors.append(f'{name}: duplicate IDs')
    for image in page.images:
        if not image.get('alt'): errors.append(f'{name}: missing image alt')
    for link in page.links:
        parsed=urlsplit(link)
        if parsed.scheme and (parsed.scheme not in ('http','https') or parsed.netloc!='barbudenge.github.io'): continue
        if parsed.netloc and parsed.netloc!='barbudenge.github.io': continue
        target_path=unquote(parsed.path)
        if target_path.startswith(EXTERNAL_APPS): continue
        target=(ROOT/target_path.lstrip('/') if target_path.startswith('/') else file.parent/target_path) if target_path else file
        target=target.resolve()
        if target.is_dir(): target=target/'index.html'
        if not target.exists(): errors.append(f'{name}: missing {link}'); continue
        if parsed.fragment and target.suffix=='.html':
            target_page=pages.get(target) or Page(target.read_text(encoding='utf-8'))
            if unquote(parsed.fragment) not in target_page.ids: errors.append(f'{name}: missing fragment {link}')
    for block in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',file.read_text(encoding='utf-8'),re.S):
        try: json.loads(block)
        except ValueError as e: errors.append(f'{name}: invalid JSON-LD {e}')
urls={e.text for e in ET.parse(ROOT/'urls-sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
for file,page in pages.items():
    if page.canonical and page.canonical[0] not in urls: errors.append(f'{file.name}: not in sitemap')
for error in errors: print(error)
print(f'{len(files)} editorial pages checked; {len(urls)} sitemap URLs; {len(errors)} errors.')
raise SystemExit(bool(errors))
