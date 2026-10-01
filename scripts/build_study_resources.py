"""Build original bilingual cam exercise and an honest editorial revision log."""
import math
from build_portal import ROOT, BASE, head, footer

DATE = '2026-10-01'
SLUG = 'cames-subida-cicloidal-polinomial.html'

def plot(pt):
    def path(law):
        points = []
        for i in range(101):
            u = i / 100
            f = u - math.sin(2 * math.pi * u) / (2 * math.pi) if law == 'cycloidal' else 10*u**3 - 15*u**4 + 6*u**5
            points.append(f'{"M" if i == 0 else "L"}{55+480*u:.2f},{250-210*f:.2f}')
        return ' '.join(points)
    label = 'Deslocamento normalizado nas duas leis de subida' if pt else 'Normalized displacement for both rise laws'
    return f'''<figure class="study-chart"><svg viewBox="0 0 600 300" role="img" aria-labelledby="cam-plot-title cam-plot-desc"><title id="cam-plot-title">{label}</title><desc id="cam-plot-desc">{'Ambas partem de zero e chegam a um; cruzam em u igual a 0,5. A curva cicloidal tem maior inclinação no ponto médio.' if pt else 'Both start at zero and reach one; they cross at u equal to 0.5. The cycloidal curve has a steeper slope at the midpoint.'}</desc><path d="M55 40V250H535" fill="none" stroke="#172c3e"/><path d="M55 145H535M295 40V250" fill="none" stroke="#d4dbdc" stroke-dasharray="4 4"/><path d="{path('cycloidal')}" fill="none" stroke="#174d6b" stroke-width="3"/><path d="{path('polynomial')}" fill="none" stroke="#a34b1b" stroke-width="3" stroke-dasharray="8 5"/><g fill="#172c3e" font-size="14"><text x="30" y="255">0</text><text x="30" y="45">1</text><text x="49" y="276">0</text><text x="280" y="276">0.5</text><text x="529" y="276">1</text><text x="540" y="255">u</text><text x="12" y="25">s/h</text></g></svg><figcaption>{'Azul contínuo: cicloidal. Laranja tracejado: polinomial 3-4-5. Eixo horizontal: fração da subida u; vertical: fração do curso s/h.' if pt else 'Solid blue: cycloidal. Dashed orange: 3-4-5 polynomial. Horizontal axis: fraction of rise u; vertical: fraction of lift s/h.'}</figcaption></figure>'''

def form(pt):
    return f'''<form class="study-form" data-cam-study hidden><fieldset><legend>{'Experimente outro curso, ângulo ou rotação' if pt else 'Try a different lift, angle or speed'}</legend><div class="study-inputs"><label>{'Curso h (mm)' if pt else 'Lift h (mm)'}<input name="lift" type="number" min="0.1" max="1000" step="any" value="30" required></label><label>{'Ângulo de subida β (graus)' if pt else 'Rise angle β (degrees)'}<input name="angle" type="number" min="1" max="359" step="any" value="90" required></label><label>{'Rotação constante (rpm)' if pt else 'Constant speed (rpm)'}<input name="rpm" type="number" min="1" max="10000" step="any" value="600" required></label></div><button class="button" type="submit">{'Comparar resultados' if pt else 'Compare results'}</button></fieldset><p data-cam-result role="status" aria-live="polite">{'Para 30 mm, 90° e 600 rpm, os valores calculados estão na tabela abaixo.' if pt else 'For 30 mm, 90° and 600 rpm, the calculated values are in the table below.'}</p></form>'''

def cam_article(pt):
    root = '/pt-br/' if pt else '/'
    title = 'Uma subida de came, duas leis: cálculo cicloidal e polinomial 3-4-5' if pt else 'One cam rise, two laws: cycloidal and 3-4-5 polynomial calculations'
    desc = 'Compare deslocamento, velocidade, aceleração e jerk em uma subida de 30 mm. Altere os dados, confira as equações e resolva exercícios.' if pt else 'Compare displacement, velocity, acceleration and jerk for a 30 mm rise. Change the inputs, check the equations and solve exercises.'
    schema = {'@context':'https://schema.org','@type':'Article','headline':title,'description':desc,'datePublished':DATE,'dateModified':DATE,'author':{'@type':'Organization','name':'Barbudenge','url':BASE+root+'sobre.html'},'inLanguage':'pt-BR' if pt else 'en','mainEntityOfPage':BASE+root+'artigos/'+SLUG}
    out = head(title, desc, root+'artigos/'+SLUG, ('/' if pt else '/pt-br/')+'artigos/'+SLUG, pt, schema)
    out = out.replace('</head>', r'''<script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},svg:{fontCache:'global'}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script><script defer src="/study-tools.js"></script></head>''')
    out += f'<main id="main" class="wrap"><article class="reading"><p><a href="{root}artigos/">← {"Todos os artigos" if pt else "All articles"}</a></p><span class="eyebrow">{"Caderno de cálculo · Cames" if pt else "Calculation notebook · Cams"}</span><h1>{title}</h1><p class="meta">Barbudenge · <time datetime="{DATE}">{DATE}</time> · {"Exemplo didático calculado" if pt else "Calculated teaching example"}</p>'
    if pt:
        body = r'''
<p class="lead">Duas curvas podem produzir o mesmo curso e parecer quase iguais no desenho, mas exigir velocidades, acelerações e transições diferentes. Aqui vamos construir uma comparação que pode ser repetida no papel e usada como referência para interpretar o CrucibleCam. Os números são cálculos didáticos, não medições de um equipamento.</p>
<nav class="toc" aria-label="Neste artigo"><strong>Neste artigo</strong><a href="#dados">Dados e hipóteses</a><a href="#leis">Leis e derivadas</a><a href="#comparacao">Comparação calculada</a><a href="#interpretacao">Como interpretar e conferir</a><a href="#exercicios">Exercícios com resposta</a></nav>
<h2 id="dados">1. Defina o movimento antes de escolher a curva</h2>
<p>Considere a subida de um seguidor ao longo de 30 mm durante 90° de rotação da came, a 600 rpm constantes. A subida começa e termina junto a trechos de parada. O restante da volta precisa conter a parada e o retorno; não estamos definindo um ciclo completo nem um perfil pronto para fabricação.</p>
<p>Adotamos curso \(h=30\,\mathrm{mm}\), ângulo da subida \(\beta=\pi/2\,\mathrm{rad}\) e velocidade angular \(\omega=2\pi n/60=20\pi\,\mathrm{rad/s}\). O tempo de subida é \(T=\beta/\omega=0{,}025\,\mathrm{s}\). A variável \(u=\theta/\beta\), de zero a um, mede quanto da subida foi percorrido. O ângulo θ é contado a partir do início desse trecho.</p>
<p>Esta análise prescreve o deslocamento do seguidor. Não considera massa, forças, atrito, elasticidade, raio de base ou raio de rolete. Por isso, ela permite comparar leis cinemáticas, mas não decidir sozinha qual came suporta uma aplicação.</p>
<h2 id="leis">2. Escreva a lei e derive com a unidade correta</h2>
<p>Escrevendo \(s=h f(u)\), as duas leis são:</p>
<div class="formula">\[\begin{aligned}f_{\rm cicloidal}(u)&=u-\frac{\sin(2\pi u)}{2\pi}\\f_{3-4-5}(u)&=10u^3-15u^4+6u^5\end{aligned}\]</div>
<p>Para a cicloidal, as derivadas em relação a u são \(f'=1-\cos(2\pi u)\), \(f''=2\pi\sin(2\pi u)\) e \(f^{(3)}=4\pi^2\cos(2\pi u)\). Para a polinomial, são \(f'=30u^2-60u^3+30u^4\), \(f''=60u-180u^2+120u^3\) e \(f^{(3)}=60-360u+360u^2\).</p>
<p>A velocidade do seguidor não é simplesmente a derivada por ângulo. Como a rotação é constante, a regra da cadeia dá:</p>
<div class="formula">\[v=\frac{h\omega}{\beta}f'(u),\qquad a=\frac{h\omega^2}{\beta^2}f''(u),\qquad j=\frac{h\omega^3}{\beta^3}f^{(3)}(u)\]</div>
<p>Com h em mm e β em radianos, os resultados são mm/s, mm/s² e mm/s³. Usar 90 na fórmula em lugar de π/2 altera o resultado por um fator grande. Se a rotação variar, aparecem termos adicionais com aceleração angular; esta ferramenta não os calcula.</p>
<h2 id="comparacao">3. Compare curvas e resultados</h2>
__PLOT__
<p>As curvas têm deslocamento zero no início, curso completo no fim e meio curso em u=0,5. Nesse ponto, a velocidade normalizada vale 2 na cicloidal e 1,875 na polinomial. Essa pequena diferença no desenho corresponde a uma diferença de 150 mm/s no exemplo.</p>
__FORM__
<noscript><p>A comparação abaixo funciona sem JavaScript. Para outros dados, use as fórmulas da seção anterior.</p></noscript>
<div class="table-scroll" tabindex="0" role="region" aria-label="Comparação das leis"><table><caption>Subida de 30 mm em 90°, a 600 rpm constantes</caption><thead><tr><th scope="col">Grandeza</th><th scope="col">Cicloidal</th><th scope="col">Polinomial 3-4-5</th></tr></thead><tbody><tr><th scope="row">Tempo de subida</th><td>0,025 s</td><td>0,025 s</td></tr><tr><th scope="row">Velocidade máxima</th><td>2 400 mm/s</td><td>2 250 mm/s</td></tr><tr><th scope="row">Máxima aceleração em módulo</th><td>301 592,895 mm/s²</td><td>277 128,129 mm/s²</td></tr><tr><th scope="row">Jerk nas extremidades da subida</th><td>75 798 561,800 mm/s³</td><td>115 200 000 mm/s³</td></tr></tbody></table></div>
<p>Os máximos usados na tabela são analíticos: \(\max f'\) vale 2 e 15/8; \(\max|f''|\) vale 2π e \(10\sqrt{3}/3\), respectivamente. Não são máximos estimados por amostragem do gráfico. O calculador mantém essas mesmas expressões quando os dados mudam.</p>
<h2 id="interpretacao">4. A menor aceleração não resolve toda a escolha</h2>
<p>A polinomial reduz a velocidade de pico em 6,25% e a aceleração de pico em aproximadamente 8,11% em relação à cicloidal neste problema. Entretanto, seu jerk nas extremidades é maior. Na parada, deslocamento constante implica velocidade, aceleração e jerk iguais a zero.</p>
<p>As duas leis se conectam à parada sem saltos de deslocamento, velocidade ou aceleração, mas têm um salto de jerk. Portanto, não é correto dizer que qualquer uma delas elimina todas as descontinuidades do diagrama SVAJ. A escolha depende do que se exige das junções e da dinâmica do sistema.</p>
<p>Ao usar o <a href="https://barbudenge.github.io/cruciblecam/pt-br/">CrucibleCam</a>, configure uma subida equivalente, confira o curso e o ângulo e identifique se a escala representa derivadas por ângulo ou por tempo. Examine as junções com as paradas e com o retorno. Não compare apenas os números máximos: observe também sinais, unidades e continuidade.</p>
<p>Depois, o projeto geométrico precisa verificar ângulo de pressão, curvatura, possibilidade de recorte do perfil e dimensão do rolete quando ele existir. Mesmo um diagrama cinemático suave pode levar a um perfil inviável. Este caderno não calcula essas verificações e não afirma validar uma versão do simulador.</p>
<h2 id="exercicios">5. Faça uma previsão antes de calcular</h2>
<p><strong>Exercício 1:</strong> mantenha curso e ângulo, mas passe de 600 para 1 200 rpm. Como mudam tempo, velocidade, aceleração e jerk?</p>
<details><summary>Ver resposta e justificativa</summary><p>O tempo cai à metade, para 0,0125 s. A velocidade dobra, a aceleração quadruplica e o jerk multiplica por oito, porque dependem de ω, ω² e ω³. Na cicloidal, os picos passam a 4 800 mm/s e 1 206 371,579 mm/s². Aumentar a rotação não altera a curva normalizada de deslocamento.</p></details>
<p><strong>Exercício 2:</strong> mantenha 30 mm e 600 rpm, mas aumente a subida de 90° para 180°. É equivalente a reduzir a rotação pela metade para este trecho?</p>
<details><summary>Ver resposta e limites</summary><p>Para a cinemática desta subida, sim: a razão ω/β cai à metade. O tempo dobra, v cai à metade, a a um quarto e j a um oitavo. Mas o restante do ciclo fica com menos ângulo disponível. Não é a mesma alteração do ciclo completo e não garante que parada e retorno caibam na nova especificação.</p></details>
<h2>Base do exemplo e próximas leituras</h2>
<p>As expressões foram diferenciadas e os valores calculados para este caderno. A base conceitual está em <a href="cames-curvas-deslocamento.html">Curvas de deslocamento e diagramas SVAJ</a>. Para entender a geometria, leia <a href="cames-projeto-analitico.html">Projeto analítico de cames</a>; para trabalhar as junções, prossiga para <a href="camforge-correcao-descontinuidades-curva-svaj.html">Correção de descontinuidades no SVAJ</a>.</p>
'''
    else:
        body = r'''
<p class="lead">Two curves can deliver the same lift and look almost identical, yet demand different velocities, accelerations and transitions. This notebook builds a comparison you can repeat on paper and use when interpreting CrucibleCam. These are calculated teaching examples, not equipment measurements.</p>
<nav class="toc" aria-label="In this article"><strong>In this article</strong><a href="#dados">Inputs and assumptions</a><a href="#leis">Laws and derivatives</a><a href="#comparacao">Calculated comparison</a><a href="#interpretacao">Interpretation and checking</a><a href="#exercicios">Exercises with answers</a></nav>
<h2 id="dados">1. Specify the motion before choosing a curve</h2>
<p>A follower rises 30 mm over 90° of cam rotation at a constant 600 rpm. The rise starts and ends next to dwell segments. The remainder of the revolution must contain dwell and return: this is not a complete cycle or a manufacturing profile.</p>
<p>We use lift \(h=30\,\mathrm{mm}\), rise angle \(\beta=\pi/2\,\mathrm{rad}\) and angular speed \(\omega=2\pi n/60=20\pi\,\mathrm{rad/s}\). Rise time is \(T=\beta/\omega=0.025\,\mathrm{s}\). The variable \(u=\theta/\beta\), from zero to one, measures progress through the rise. Angle θ is measured from the start of this segment.</p>
<p>This analysis prescribes follower displacement. It does not include mass, forces, friction, compliance, base radius or roller radius. It compares kinematic laws, but cannot by itself determine which cam can withstand an application.</p>
<h2 id="leis">2. Write the law and differentiate with consistent units</h2>
<p>With \(s=h f(u)\), the laws are:</p>
<div class="formula">\[\begin{aligned}f_{\rm cycloidal}(u)&=u-\frac{\sin(2\pi u)}{2\pi}\\f_{3-4-5}(u)&=10u^3-15u^4+6u^5\end{aligned}\]</div>
<p>For the cycloidal law, derivatives with respect to u are \(f'=1-\cos(2\pi u)\), \(f''=2\pi\sin(2\pi u)\), and \(f^{(3)}=4\pi^2\cos(2\pi u)\). For the polynomial, they are \(f'=30u^2-60u^3+30u^4\), \(f''=60u-180u^2+120u^3\), and \(f^{(3)}=60-360u+360u^2\).</p>
<p>Follower velocity is not simply the derivative with respect to angle. For constant cam speed, the chain rule gives:</p>
<div class="formula">\[v=\frac{h\omega}{\beta}f'(u),\qquad a=\frac{h\omega^2}{\beta^2}f''(u),\qquad j=\frac{h\omega^3}{\beta^3}f^{(3)}(u)\]</div>
<p>With h in mm and β in radians, the units are mm/s, mm/s² and mm/s³. Entering 90 instead of π/2 in this formula changes the result by a large factor. Variable cam speed introduces additional angular acceleration terms; this calculator does not include them.</p>
<h2 id="comparacao">3. Compare curves and numerical results</h2>
__PLOT__
<p>Both curves start at zero displacement, end at full lift and reach half lift at u=0.5. At that point normalized velocity is 2 for the cycloidal law and 1.875 for the polynomial. The small visual difference corresponds to 150 mm/s in this example.</p>
__FORM__
<noscript><p>The comparison below works without JavaScript. For different inputs, use the equations above.</p></noscript>
<div class="table-scroll" tabindex="0" role="region" aria-label="Law comparison"><table><caption>30 mm rise over 90°, at a constant 600 rpm</caption><thead><tr><th scope="col">Quantity</th><th scope="col">Cycloidal</th><th scope="col">3-4-5 polynomial</th></tr></thead><tbody><tr><th scope="row">Rise time</th><td>0.025 s</td><td>0.025 s</td></tr><tr><th scope="row">Peak velocity</th><td>2,400 mm/s</td><td>2,250 mm/s</td></tr><tr><th scope="row">Peak absolute acceleration</th><td>301,592.895 mm/s²</td><td>277,128.129 mm/s²</td></tr><tr><th scope="row">Jerk at rise endpoints</th><td>75,798,561.800 mm/s³</td><td>115,200,000 mm/s³</td></tr></tbody></table></div>
<p>The maxima are analytical: \(\max f'\) is 2 and 15/8; \(\max|f''|\) is 2π and \(10\sqrt{3}/3\), respectively. They are not estimates from graph sampling. The calculator uses these same expressions when inputs change.</p>
<h2 id="interpretacao">4. Lower acceleration does not settle every design choice</h2>
<p>The polynomial reduces peak velocity by 6.25% and peak acceleration by approximately 8.11% relative to the cycloidal law in this problem. However, its endpoint jerk is larger. During dwell, constant displacement means zero velocity, acceleration and jerk.</p>
<p>Both laws join a dwell without jumps in displacement, velocity or acceleration, but have a jerk jump. Neither eliminates every discontinuity in the SVAJ diagram. Selection depends on the required boundary conditions and system dynamics.</p>
<p>In <a href="https://barbudenge.github.io/cruciblecam/">CrucibleCam</a>, configure an equivalent rise, check lift and angle, and identify whether the scale represents derivatives with respect to angle or time. Inspect joins with dwell and return. Compare signs, units and continuity as well as peak values.</p>
<p>Geometric design must then check pressure angle, curvature, undercutting and roller dimensions where applicable. Even smooth kinematic diagrams can produce an infeasible profile. This notebook does not perform those checks or claim to validate a simulator release.</p>
<h2 id="exercicios">5. Predict the change before calculating</h2>
<p><strong>Exercise 1:</strong> keep lift and angle fixed, but increase speed from 600 to 1,200 rpm. What happens to time, velocity, acceleration and jerk?</p>
<details><summary>Show answer and reasoning</summary><p>Time halves to 0.0125 s. Velocity doubles, acceleration quadruples, and jerk increases eightfold, because they depend on ω, ω² and ω³. Cycloidal peaks become 4,800 mm/s and 1,206,371.579 mm/s². Speed does not change the normalized displacement curve.</p></details>
<p><strong>Exercise 2:</strong> keep 30 mm and 600 rpm, but increase the rise angle from 90° to 180°. Is this equivalent to halving speed for this segment?</p>
<details><summary>Show answer and limits</summary><p>For this rise's kinematics, yes: ω/β halves. Time doubles, v halves, a becomes one quarter and j one eighth. However, less angle remains for the rest of the cycle. This is not the same change to the complete cycle and does not ensure that dwell and return fit the new specification.</p></details>
<h2>Basis of this example and further reading</h2>
<p>The expressions were differentiated and the values calculated for this notebook. For background, read <a href="cames-curvas-deslocamento.html">Displacement curves and SVAJ diagrams</a>. For geometry, read <a href="cames-projeto-analitico.html">Analytical cam design</a>; for joins, continue with <a href="camforge-correcao-descontinuidades-curva-svaj.html">Correcting SVAJ discontinuities</a>.</p>
'''
    body = body.replace('__PLOT__',plot(pt)).replace('__FORM__',form(pt))
    body += f'<p class="article-correction">{"Encontrou um erro? Envie os dados e o endereço desta página para" if pt else "Found an error? Send the inputs and this page address to"} <a href="mailto:arturavelar@ufsj.edu.br">arturavelar@ufsj.edu.br</a>.</p>'
    (ROOT/root.strip('/')/'artigos'/SLUG).write_text(out+body+'</article></main>'+footer(pt),encoding='utf-8')

def revision_page(pt):
    root = '/pt-br/' if pt else '/'
    title = 'Revisões do portal' if pt else 'Portal revisions'
    desc = 'Registro das mudanças editoriais e canal para informar erros em artigos e cálculos.' if pt else 'An editorial change log and a way to report errors in articles and calculations.'
    out = head(title,desc,root+'atualizacoes.html',('/' if pt else '/pt-br/')+'atualizacoes.html',pt)
    if pt:
        body = '''<p>Este registro identifica mudanças concretas do portal editorial. As datas de publicação dos artigos são preservadas; revisões de conteúdo são indicadas separadamente. Os aplicativos e o LASME têm ciclos de manutenção próprios.</p><h2>1 de outubro de 2026</h2><ul><li>Novo caderno de cames com dedução das leis cicloidal e polinomial 3-4-5, gráfico comparativo, cálculo de picos e exercícios comentados.</li><li>O guia de planetárias recebeu um conferidor de velocidades com verificação da condição geométrica dos dentes.</li><li>A página inicial passou a destacar atividades de cálculo e teve a disposição em telas pequenas corrigida.</li></ul><h2>Como pedir uma correção</h2><p>Envie o endereço da página, a seção, os dados de entrada e o resultado esperado para <a href="mailto:arturavelar@ufsj.edu.br">arturavelar@ufsj.edu.br</a>. Quando houver revisão técnica, a página deve indicar a data e o que foi alterado. Este registro não representa uma promessa de frequência de publicação.</p>'''
    else:
        body = '''<p>This log identifies concrete changes to the editorial portal. Article publication dates are preserved; content revisions are indicated separately. The applications and LASME have their own maintenance cycles.</p><h2>1 October 2026</h2><ul><li>A new cam notebook derives cycloidal and 3-4-5 polynomial laws, with a comparative graph, peak calculations and explained exercises.</li><li>The planetary guide now includes a speed checker with a tooth geometry condition check.</li><li>The home page highlights calculation activities and its layout on small screens was corrected.</li></ul><h2>How to request a correction</h2><p>Send the page address, section, inputs and expected result to <a href="mailto:arturavelar@ufsj.edu.br">arturavelar@ufsj.edu.br</a>. Technical revisions should state their date and describe the change. This log does not promise a publication schedule.</p>'''
    body += f'<p><a href="{root}artigos/{SLUG}">{"Abrir o caderno de cames" if pt else "Open the cam notebook"}</a> · <a href="{root}artigos/conferir-resultados-planetaria.html">{"Abrir o guia de planetárias" if pt else "Open the planetary guide"}</a></p><p><a href="{root}sobre.html">{"Autoria e critérios editoriais" if pt else "Authorship and editorial approach"}</a></p>'
    (ROOT/root.strip('/')/'atualizacoes.html').write_text(out+f'<main id="main" class="wrap"><article class="reading"><h1>{title}</h1>'+body+'</article></main>'+footer(pt),encoding='utf-8')

def planet_checker(pt):
    path = ROOT/('pt-br/artigos' if pt else 'artigos')/'conferir-resultados-planetaria.html'
    text = path.read_text(encoding='utf-8')
    general = r'<div class="formula">\[n_C=\frac{N_S n_S+N_R n_R}{N_S+N_R},\qquad N_P=\frac{N_R-N_S}{2}\]</div>'
    if 'data-planet-study' in text:
        if 'N_S n_S+N_R n_R' not in text:
            text = text.replace('<form class="study-form" data-planet-study',general+'<form class="study-form" data-planet-study',1)
            path.write_text(text,encoding='utf-8')
        return
    labels = ['Dentes do sol', 'Dentes da coroa', 'Rotação do sol (rpm)', 'Rotação da coroa (rpm)'] if pt else ['Sun teeth', 'Ring teeth', 'Sun speed (rpm)', 'Ring speed (rpm)']
    fields = ''
    for label, name, value in zip(labels,['sun','ring','sunSpeed','ringSpeed'],[24,72,1200,0]):
        limits = 'min="1" max="1000" step="1"' if name in ('sun','ring') else 'min="-100000" max="100000" step="any"'
        fields += f'<label>{label}<input name="{name}" type="number" {limits} value="{value}" required></label>'
    heading = 'Conferidor: duas velocidades conhecidas' if pt else 'Checker: two known speeds'
    intro = 'Use a mesma convenção de sinal para sol e coroa. O conferidor resolve a equação de uma planetária simples e verifica se o satélite teria um número inteiro positivo de dentes. O cálculo não analisa carga, interferência ou fases de montagem.' if pt else 'Use the same sign convention for sun and ring. This checker solves the equation for a simple planetary assembly and checks whether the planet would have a positive integer tooth count. It does not analyse load, interference or assembly phasing.'
    block = f'''<h2 id="conferidor">{heading}</h2><p>{intro}</p><form class="study-form" data-planet-study hidden><fieldset><legend>{'Dados para a equação do braço' if pt else 'Inputs for the carrier equation'}</legend><div class="study-inputs">{fields}</div><button type="submit" class="button">{'Calcular e interpretar' if pt else 'Calculate and interpret'}</button></fieldset><p data-planet-result role="status" aria-live="polite">{'Os dados iniciais reproduzem o caso de coroa fixa: braço a 300 rpm.' if pt else 'The initial inputs reproduce the fixed-ring case: carrier at 300 rpm.'}</p></form><noscript><p>{'Use a equação e os exemplos resolvidos acima para fazer a conferência sem JavaScript.' if pt else 'Use the equation and worked examples above to check the result without JavaScript.'}</p></noscript>'''
    block = block.replace('<form class="study-form" data-planet-study',general+'<form class="study-form" data-planet-study',1)
    text = text.replace('<h2 id="conferencia">',block+'<h2 id="conferencia">',1)
    text = text.replace('</head>','<script defer src="/study-tools.js"></script></head>',1)
    text = text.replace('"dateModified": "2026-09-21"',f'"dateModified": "{DATE}"')
    visible = ('Revisado em 2026-10-01: adicionado conferidor de velocidades e condição de dentes.' if pt else 'Revised on 2026-10-01: added speed checker and tooth condition check.')
    text = text.replace('<p class="lead">',f'<p class="meta">{visible}</p><p class="lead">',1)
    text = text.replace('<a href="#conferencia">',f'<a href="#conferidor">{heading}</a><a href="#conferencia">',1)
    path.write_text(text,encoding='utf-8')

if __name__ == '__main__':
    for pt in (False,True):
        cam_article(pt)
        revision_page(pt)
        planet_checker(pt)
    print('Bilingual cam notebook and revision log built.')
