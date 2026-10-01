# Revisão editorial — 21 de setembro de 2026

## Diagnóstico e limites

O aviso “Conteúdo de baixo valor” não revela quais páginas motivaram a decisão.
Esta revisão não teve acesso à conta AdSense nem ao Search Console. Portanto,
os pontos abaixo são problemas observados e oportunidades de melhoria, não uma
identificação definitiva da causa da recusa. Nenhuma mudança garante aprovação.

O acervo já possuía 23 artigos por idioma, com cálculos, figuras e exemplos
associados às ferramentas do autor. Aumentar a quantidade indiscriminadamente
não era a prioridade. A entrada do portal repetia muitos destinos no menu
lateral, na navegação superior, nas seções e no rodapé. Os simuladores ficavam
longe do início, e o acesso a Powertrain levava primeiro a um artigo.

As orientações oficiais consultadas priorizam conteúdo próprio, utilidade e
navegação clara; não estabelecem uma quantidade mágica de artigos ou visitas:

- [Preparar páginas para o AdSense](https://support.google.com/adsense/answer/7299563?hl=pt-BR).
- [Site ainda não está pronto para exibir anúncios](https://support.google.com/adsense/answer/12176698?hl=pt-BR).
- [Problemas de aprovação da conta](https://support.google.com/adsense/answer/81904?hl=pt-BR).

## Implementação

- Página inicial refeita em português e inglês, com hierarquia mais curta,
  três simuladores diretamente acessíveis, trilhas em ordem de leitura,
  exemplo resolvido em destaque, autoria e contato.
- FAQ, glossário e livros preservados em seções recolhíveis.
- Catálogos reconstruídos com os 24 artigos de cada língua, busca sem distinção
  de acentos, filtro por assunto, estado sem resultados e botão de limpeza.
- Todo o acervo é acessível por links em HTML, mesmo sem executar JavaScript.
- Novo guia de planetária simples: geometria, hipóteses, três configurações,
  substituição dos resultados, limitações e exercício resolvido. Não apresenta
  cálculos didáticos como medições ou testes realizados no software.
- Aula de trens simples e compostos ampliada com reduções de dois estágios,
  contraste entre topologias e conferência de distância entre eixos.
- Artigos existentes receberam sumário, ligação para autoria/privacidade,
  contato para correções e mais espaço de leitura. A navegação lateral injetada
  foi retirada apenas desses documentos editoriais.
- Tabelas largas ganharam rolagem própria; fórmulas permanecem dentro da
  largura de leitura. Não foi necessário editar CSS das aplicações.
- Catálogos, metadados bilíngues e sitemap atualizados. O código de identificação
  AdSense foi mantido; a propriedade Analytics da página inicial também.

## Preservação

Nenhum arquivo de `camforge/`, LASME, Engrenarium ou Powertrain foi modificado.
As aplicações hospedadas em outros repositórios também não foram alteradas.
Os recursos compartilhados `site-sidebar.css`, `site-sidebar.js` e
`language-switch.css` permanecem intactos. As imagens preexistentes não foram
editadas, incluindo os arquivos não versionados `curv1.jpg` e `curv2.jpg`.

Os textos em `artigos/` que explicam as aplicações pertencem ao portal editorial;
receberam navegação e ajustes de leitura, sem alterar o funcionamento dos aplicativos.

## Verificação

- 52 páginas editoriais verificadas automaticamente: links locais, imagens,
  âncoras, H1 único, IDs únicos, JSON-LD válido e presença no sitemap.
- 62 URLs no sitemap, incluindo as entradas já existentes para aplicações.
- Sintaxe do JavaScript e espaços do diff verificados.
- Prévia no navegador em desktop e largura de 390 px: início PT/EN,
  catálogo PT, novo guia e artigos com fórmulas/tabelas.
- Busca “planetaria”: 11 resultados; combinada com cames: zero; limpeza:
  retorno aos 24 artigos. A busca é um recurso adicional, sem esconder o
  acervo inicial de visitantes sem JavaScript.
- Correção de extravasamento horizontal encontrada na tabela do artigo de
  correção SVAJ; largura final da página igual à largura visível no celular.
- Destino público do CrucibleCam em português aberto com sucesso no navegador.
  Engrenarium e Powertrain também foram consultados pela pesquisa web.

## Antes da próxima solicitação

A publicação no GitHub Pages foi autorizada pelo responsável pelo portal após
a revisão da versão local. A solicitação de revisão na conta AdSense é uma
etapa separada e não foi realizada nesta tarefa.

Depois de publicar, confira se o domínio mostra a nova versão, se o Google
consegue acessar as páginas e se o sitemap publicado está atualizado. Use a
inspeção de URL do Search Console para confirmar a versão rastreada. Só então
solicite nova revisão. Não existe prazo de espera fixo que garanta aprovação.

## Sugestões para as áreas protegidas (não implementadas)

Se houver uma revisão futura dessas áreas, eu avaliaria incluir junto a cada
simulador um exemplo completo com entradas, resultado esperado, convenções de
sinal/unidade, limitações e ligação ao artigo correspondente. O CrucibleCam já tem
uma explicação pública abaixo da interface; um caso reproduzível agregaria mais
valor do que repetir a descrição da ferramenta.

Também verificaria na configuração do AdSense onde os anúncios automáticos
podem aparecer, especialmente telas apenas de controles ou sem conteúdo
editorial. Essa avaliação exige acesso à conta e inspeção das páginas afetadas;
não implica que ferramentas ou aplicações sejam, por si só, proibidas.
# Revisão de 1 de outubro de 2026

Após a nova recusa, foram acrescentados recursos utilizáveis no portal editorial:

- Caderno bilíngue original de comparação de subida cicloidal e polinomial
  3-4-5: hipóteses, derivadas, gráfico estático, máximos analíticos, cálculo com
  dados variáveis e dois exercícios comentados.
- Conferidor no guia de planetárias: rotação do braço a partir de sol e coroa,
  velocidades relativas e rejeição de números de dentes incompatíveis com a
  geometria de referência adotada.
- Seção de atividades na página inicial e registro público de revisões com
  canal de correção. As datas antigas de publicação foram preservadas.
- Correção da cascata de estilos que mantinha duas colunas no hero móvel.
- Classificação do artigo CrucibleCam desktop no assunto de cames.

Verificação: 58 páginas editoriais e 68 URLs no sitemap, sem erros de links,
fragmentos, imagens ou JSON-LD detectados pelo verificador. O navegador
confirmou 17 expressões matemáticas renderizadas sem erro no novo caderno,
valores de referência, mudança de rotação e condições inválidas de dentes.
Prévia em 390 px sem transbordamento lateral na home e no novo artigo.
Nenhum arquivo dos aplicativos ou do LASME foi alterado.

Estas mudanças aumentam a utilidade do conteúdo; não demonstram, por si só,
interesse sustentado do público e não garantem aprovação. Não foram inventados
visitantes, medições, depoimentos, revisões antigas ou resultados de ensaios.
Continua sendo necessário observar o uso real, atender dúvidas concretas e
manter os materiais conforme novas necessidades aparecerem.

Referências oficiais consultadas nesta revisão:
- https://support.google.com/adsense/answer/7299563
- https://support.google.com/adsense/answer/12176698
- https://support.google.com/adsense/answer/9724
