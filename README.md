# Barbudenge

Portal estático bilíngue de engenharia mecânica, publicado no GitHub Pages.
O conteúdo em português fica em `pt-br/`; a versão inglesa fica na raiz.

## Atualizar o portal

Os artigos completos são arquivos HTML em `artigos/` e `pt-br/artigos/`.
Cada artigo precisa de título H1, descrição, URL canônica e `datePublished` nos
dados estruturados. Preserve a data de publicação ao atualizar um artigo e
registre a data da alteração em `dateModified` e na informação visível ao leitor.

Depois de editar ou adicionar um artigo nas duas línguas:

```powershell
python scripts/enhance_editorial.py
python scripts/build_portal.py
./scripts/generate-sitemap.ps1
python scripts/check_site.py
node --check portal.js
```

`enhance_editorial.py` insere sumários estáticos, contato para correções e
contêineres de tabelas nos artigos existentes. `build_portal.py` reconstrói as
duas páginas iniciais e os catálogos a partir dos artigos. O conteúdo principal
e todos os links são HTML estático; JavaScript só acrescenta os filtros.

`scripts/add-worked-examples.py` foi usado para criar o guia de conferência e
expandir a aula de trens. Não é necessário executá-lo no fluxo normal: ele
sobrescreve o guia de conferência com o texto inicial, descartando edições manuais
posteriores nesse guia.

## Prévia local

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Abra `http://127.0.0.1:8765/pt-br/`. Teste também `/`, os filtros dos catálogos e
artigos com tabelas e fórmulas em tela pequena. Não abra apenas o HTML pelo
explorador: os recursos usam caminhos relativos à raiz do site.

Os arquivos de CrucibleCam, LASME, Engrenarium e Powertrain e os recursos
`site-sidebar.*` não são editados pelos geradores editoriais.

Consulte `RELATORIO-REVISAO-ADSENSE.md` para escopo, evidências e pendências.
