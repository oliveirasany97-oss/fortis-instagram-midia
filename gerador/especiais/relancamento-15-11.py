"""Relançamento @fortismatcon.oficial — 15/11/2026 (feed 1080x1440, stories 1080x1920)."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G

A = G.A
W, H = 1080, 1440
ROD = '<div class="rodape" style="bottom:70px;font-size:21px">FORTÍS SOLUÇÕES MATCON</div>'
HANDLE_ST = '<div class="handle" style="bottom:385px;font-size:24px">@fortismatcon.oficial</div>'

def tit(linhas):
    return "".join(f'<div class="{"metal" if i == len(linhas) - 1 else "branco"}">{G.e(t)}</div>' for i, t in enumerate(linhas))

def arte(w, h, corpo, b=.75):
    return f'<div class="arte" style="width:{w}px;height:{h}px">{G.fundo(w, h, b)}{corpo}</div>'

# ---------- FEED 15:30 — MANIFESTO ----------
def manifesto():
    pil = "".join(f'''<div class="card" style="padding:28px 16px">{G.icone(ic, 70)}
      <h3 style="margin-top:14px;font-size:27px">{t}</h3><p style="margin-top:8px;font-size:20px">{d}</p></div>'''
      for ic, t, d in [("carrinho", "Compras", "Comprar certo, na hora certa"),
                       ("equipe", "Equipe", "Cada um sabe o seu papel"),
                       ("grafico", "Números", "Decidir olhando a margem")])
    return arte(W, H, f'''
  <img class="logo" src="{A}/logo.png" style="top:70px;width:160px">
  <div class="kicker" style="top:330px;font-size:24px">QUEM SOMOS</div>
  <div class="titulo" data-max="920" data-fs="112" style="top:380px;line-height:1.03">{tit(["DONO DE LOJA", "NÃO DECIDE SOZINHO"])}</div>
  <p class="sub" style="top:640px;left:100px;right:100px;font-size:32px">A Fortís entra na sua loja, senta ao seu lado e olha os números junto com você. <b>Experiência de quem vive o varejo de material de construção desde 2013.</b></p>
  <div style="position:absolute;top:880px;left:90px;right:90px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px">{pil}</div>
  <p class="cta" style="top:1205px;font-size:28px;padding:0 70px">De loja em loja, <b>lado a lado com o dono.</b></p>
  {ROD}''')

# ---------- FEED 19:30 — ORIGEM (carrossel) ----------
def origem():
    s1 = arte(W, H, f'''
  <img class="logo" src="{A}/logo.png" style="top:70px;width:170px">
  <div class="kicker" style="top:350px;font-size:24px">A ORIGEM DA FORTÍS</div>
  <div class="titulo" data-max="920" data-fs="150" style="top:410px;line-height:1.0">{tit(["DE 300 MIL", "PARA 750 MIL"])}</div>
  <p class="sub" style="top:790px;left:110px;right:110px;font-size:36px">Faturamento mensal da <b>mesma loja</b> de material de construção.</p>
  <p class="cta" style="top:1160px;font-size:30px;color:var(--gold)">Deslize para o lado →</p>{ROD}''')
    s2 = arte(W, H, f'''
  <img class="logo" src="{A}/logo.png" style="top:70px;width:130px">
  <div class="kicker" style="top:330px;font-size:24px">ANTES DA FORTÍS</div>
  <div class="titulo" data-max="920" data-fs="100" style="top:380px;line-height:1.04">{tit(["EU ERA GERENTE", "DE UMA LOJA MATCON"])}</div>
  <p class="sub" style="top:650px;left:110px;right:110px;font-size:35px">Não cheguei como consultor. Cheguei como gerente, com a loja na mão e o resultado na conta. Ali apliquei um <b>modelo próprio de gestão.</b></p>
  <div class="assina" style="left:0;right:0;text-align:center;top:1010px;font-size:24px">SÂNY OLIVEIRA<small>CEO &amp; Fundador · FORTÍS SOLUÇÕES MATCON</small></div>{ROD}''')
    itens = [("Reposicionamento", "Rever o lugar da loja no mercado e no bairro."),
             ("Processos internos", "Compras, estoque e equipe com rotina e responsável."),
             ("Rentabilidade", "Decidir olhando a margem, não só o volume.")]
    lis = "".join(f'<div class="check"><div class="box">{k+1}</div><div><b>{G.e(a)}</b><span>{G.e(b)}</span></div></div>' for k, (a, b) in enumerate(itens))
    s3 = arte(W, H, f'''
  <img class="logo" src="{A}/logo.png" style="top:60px;width:110px">
  <div class="titulo" data-max="920" data-fs="76" style="top:300px;line-height:1.05"><div class="metal">OS 3 PILARES DO MÉTODO</div></div>
  <div style="position:absolute;top:480px;left:120px;right:110px">{lis}</div>{ROD}''')
    s4 = arte(W, H, f'''
  <img class="logo" src="{A}/logo.png" style="top:200px;width:220px">
  <div class="titulo" data-max="920" data-fs="104" style="top:600px;line-height:1.04">{tit(["ESSE RESULTADO", "VIROU A FORTÍS"])}</div>
  <p class="sub" style="top:870px;left:110px;right:110px;font-size:35px">A indicação que veio dessa loja deu origem à <b>Fortís Soluções MATCON</b>, em 2023. Hoje levamos o mesmo método de loja em loja.</p>{ROD}''', .9)
    return [("origem-1", s1), ("origem-2", s2), ("origem-3", s3), ("origem-4", s4)]

# ---------- FEED 22:30 — 7 SINAIS (carrossel) ----------
def sinais():
    capa = arte(W, H, f'''
  <img class="logo" src="{A}/logo.png" style="top:70px;width:170px">
  <div class="kicker" style="top:350px;font-size:24px">TESTE RÁPIDO</div>
  <div class="titulo" data-max="920" data-fs="120" style="top:410px;line-height:1.02">{tit(["7 SINAIS DE QUE", "A LOJA CRESCEU", "E A GESTÃO NÃO"])}</div>
  <p class="sub" style="top:860px;left:110px;right:110px;font-size:36px">Conte quantos você <b>reconhece na sua loja.</b></p>
  <p class="cta" style="top:1160px;font-size:30px;color:var(--gold)">Deslize para o lado →</p>{ROD}''')
    todos = [("Falta o que vende todo dia", "A ruptura só aparece quando o cliente pede."),
             ("Compra repetida", "O mesmo item comprado duas vezes porque ninguém sabia."),
             ("Tudo passa pelo dono", "Sem você na loja, as decisões param."),
             ("Estoque que não bate", "O sistema diz uma coisa, a prateleira diz outra."),
             ("Desconto sem critério", "Cada vendedor negocia de um jeito e a margem some."),
             ("Meta só no fim do mês", "A equipe descobre o resultado quando não dá mais tempo."),
             ("Controle no papel", "Pedidos, devoluções e entregas no caderno.")]
    def lista(ini, fim, titulo):
        lis = "".join(f'<div class="check"><div class="box">{k+1}</div><div><b>{G.e(a)}</b><span>{G.e(b)}</span></div></div>' for k, (a, b) in list(enumerate(todos))[ini:fim])
        return arte(W, H, f'''
  <img class="logo" src="{A}/logo.png" style="top:60px;width:110px">
  <div class="titulo" data-max="920" data-fs="72" style="top:290px;line-height:1.05"><div class="metal">{titulo}</div></div>
  <div style="position:absolute;top:440px;left:120px;right:110px">{lis}</div>{ROD}''')
    fim = arte(W, H, f'''
  <img class="logo" src="{A}/logo.png" style="top:200px;width:220px">
  <div class="titulo" data-max="920" data-fs="104" style="top:600px;line-height:1.04">{tit(["MARCOU 3 OU MAIS?", "VAMOS CONVERSAR"])}</div>
  <p class="sub" style="top:870px;left:110px;right:110px;font-size:35px">Responda no direct com o número de sinais da sua loja. <b>A gente te mostra por onde começar.</b></p>{ROD}''', .9)
    return [("sinais-1", capa), ("sinais-2", lista(0, 4, "SINAIS 1 A 4")), ("sinais-3", lista(4, 7, "SINAIS 5 A 7")), ("sinais-4", fim)]

# ---------- STORIES ----------
SW, SH = 1080, 1920
FONTE = 'position:absolute;right:60px;bottom:250px;max-width:620px;text-align:right;font-size:19px;line-height:1.4;color:#aab6c9;background:rgba(0,0,0,.38);padding:10px 16px;border-radius:10px'

def story_porcelanato():
    linhas = [("Porcelanato", "até 0,5%", True), ("Grés", "0,5% a 3%", False), ("Semi-grés", "3% a 6%", False),
              ("Semiporoso", "6% a 10%", False), ("Poroso", "acima de 10%", False)]
    tab = "".join(f'''<div style="display:flex;justify-content:space-between;padding:20px 34px;border-bottom:1px solid rgba(217,181,121,.25);{'background:rgba(217,181,121,.14)' if d else ''}">
      <span style="font-size:36px;font-weight:{700 if d else 600};color:{'#D9B579' if d else '#fff'}">{a}</span><span style="font-size:36px;font-weight:700;color:{'#D9B579' if d else '#e9edf5'}">{b}</span></div>''' for a, b, d in linhas)
    return arte(SW, SH, f'''
  <img class="logo" src="{A}/logo.png" style="top:230px;width:150px">
  <div class="kicker" style="top:500px;font-size:28px">ENTENDA A DIFERENÇA</div>
  <div class="titulo" data-max="900" data-fs="104" style="top:550px;line-height:1.04">{tit(["CERÂMICA OU", "PORCELANATO?"])}</div>
  <p class="sub" style="top:800px;left:90px;right:90px;font-size:34px">O que separa um do outro é a <b>absorção de água</b>:</p>
  <div class="card" style="position:absolute;top:900px;left:90px;right:90px;padding:6px 0;text-align:left">{tab}</div>
  <p class="sub" style="top:1380px;left:90px;right:90px;font-size:31px">Quanto menor a absorção, maior a resistência. O porcelanato técnico chega a <b>até 0,1%</b>.</p>
  <div class="rodape" style="bottom:470px;font-size:22px">FORTÍS SOLUÇÕES MATCON</div>
  <div style="{FONTE};bottom:360px">Fonte: ABNT NBR ISO 13006 e ABNT NBR 15463 (porcelanato), citadas em manual técnico Decortiles e na revista Cerâmica Industrial</div>''', .93)

def story_flow():
    itens = [("Falta avisada na hora", "O vendedor registra a ruptura no celular."),
             ("Fila por marca", "Cada item vai para a fila certa de compra."),
             ("Ao lado do seu ERP", "Sem trocar de sistema.")]
    lis = "".join(f'<div class="check" style="margin-bottom:26px"><div class="box">{k+1}</div><div><b style="font-size:30px">{G.e(a)}</b><span style="font-size:22px">{G.e(b)}</span></div></div>' for k, (a, b) in enumerate(itens))
    return arte(SW, SH, f'''
  <img class="logo" src="{A}/logo.png" style="top:230px;width:130px;left:150px;transform:none">
  <div class="kicker esq" style="top:470px;left:70px;width:auto;font-size:24px;letter-spacing:7px">FORTÍS FLOW</div>
  <div class="titulo esq" data-max="500" data-fs="86" style="top:520px;left:70px;right:auto;line-height:1.04">{tit(["NENHUMA", "COMPRA", "FICA PARA", "TRÁS"])}</div>
  <div style="position:absolute;top:1000px;left:70px;width:500px">{lis}</div>
  <div class="halo" style="width:560px;height:1000px;left:540px;top:380px"></div>
  <div style="position:absolute;left:600px;top:420px;width:410px;height:888px;border-radius:50px;border:10px solid #0b1424;outline:3px solid rgba(217,181,121,.85);box-shadow:0 0 50px rgba(217,181,121,.25),0 40px 80px rgba(0,0,0,.6);overflow:hidden;background:#0E1F39">
    <img src="{A}/telas/fila.png" style="width:100%;display:block"></div>
  <div style="position:absolute;left:600px;width:410px;top:1330px;text-align:center;font-weight:600;letter-spacing:5px;color:var(--gold);font-size:16px">TELA REAL · DADOS FICTÍCIOS</div>
  <div class="rodape" style="bottom:430px;font-size:22px">FORTÍS SOLUÇÕES MATCON</div>{HANDLE_ST}''', .93)

def story_bomdia():
    return arte(SW, SH, f'''
  <img class="logo" src="{A}/logo.png" style="top:280px;width:170px">
  <div style="position:absolute;top:620px;left:0;right:0;bottom:520px;display:flex;flex-direction:column;justify-content:center">
    <div class="kicker" style="position:static;font-size:28px">BOM DIA, LOJISTA</div>
    <div class="titulo" data-max="900" data-fs="104" style="position:static;margin-top:34px;line-height:1.05">{tit(["SEGUNDA É DIA", "DE ALINHAR"])}</div>
    <p class="sub" style="position:static;margin:44px 100px 0;font-size:42px">15 minutos com a equipe antes de abrir: <b>meta da semana, o que falta comprar e quem cuida de cada setor.</b></p>
    <p class="cta" style="position:static;margin-top:60px;font-size:36px;padding:0 80px">Loja alinhada começa a semana na frente.</p>
  </div>
  <div class="rodape" style="bottom:430px;font-size:22px">FORTÍS SOLUÇÕES MATCON</div>{HANDLE_ST}''', .93)

itens = [("feed-manifesto", manifesto(), (W, H))]
itens += [(n, c, (W, H)) for n, c in origem()]
itens += [(n, c, (W, H)) for n, c in sinais()]
itens += [("story-porcelanato", story_porcelanato(), (SW, SH)), ("story-flow-fila", story_flow(), (SW, SH)),
          ("story-bomdia-16-11", story_bomdia(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'relancamento-15-11')
asyncio.run(G.renderizar(itens, saida))
