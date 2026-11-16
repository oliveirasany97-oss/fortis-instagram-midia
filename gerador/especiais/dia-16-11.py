"""Conteúdo de 16/11/2026 (feed 1080x1440, stories 1080x1920) + story 06:00 de 17/11.

Layout em fluxo (flex em coluna) para que textos longos empurrem os blocos de baixo
em vez de invadir o rodapé. Ao renderizar, cada arte passa por uma checagem automática:
blocos marcados com a classe "k" não podem se sobrepor, precisam de 40px de folga
entre si e não podem sair da área segura.
"""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G
from PIL import Image
from playwright.async_api import async_playwright

A = G.A
W, H = 1080, 1440
SW, SH = 1080, 1920
G.ICONES["obra"] = '<path d="M8 54h48M14 54V26l18-14 18 14v28"/><path d="M26 54V38h12v16"/><path d="M4 30l28-22 28 22"/>'

CSS = """
.col{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center}
.col>*{position:static!important}
.meio{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;width:100%;gap:72px}
.zona .meio{gap:62px}
.zona .tab .lin{padding:13px 30px}
.meio>*{position:static!important}
.base>*{position:static!important}
.col .logo{transform:none}
.col .titulo,.col .kicker,.col .cta,.col .sub,.col .rodape,.col .handle,.meio .sub,.meio .cta{width:100%}
.base{display:flex;flex-direction:column;align-items:center;gap:40px;width:100%}
.fonte{max-width:900px;text-align:center;font-size:20px;line-height:1.4;color:#b3bfd1;background:rgba(5,12,25,.88);padding:12px 20px;border-radius:12px}
.selo{display:inline-block;font-weight:700;letter-spacing:4px;font-size:18px;color:#0E1F39;background:#D9B579;padding:6px 14px;border-radius:8px}
.tab{width:100%;text-align:left}
.tab .lin{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:18px 30px;border-bottom:1px solid rgba(217,181,121,.25)}
.tab .lin:last-child{border-bottom:none}
.tab .lin.d{background:rgba(217,181,121,.14)}
.tab .a{font-weight:700;color:#fff}
.tab .b{font-weight:700;color:#D9B579;text-align:right}
.tab .h{color:#D9B579;font-weight:600;letter-spacing:3px}
.check:last-child{margin-bottom:0!important}
"""


def tit(linhas):
    return "".join(f'<div class="{"metal" if i == len(linhas) - 1 else "branco"}">{G.e(t)}</div>' for i, t in enumerate(linhas))


def titulo(linhas, fs, mx=920, lh=1.04):
    return f'<div class="titulo k" data-max="{mx}" data-fs="{fs}" style="line-height:{lh}">{tit(linhas)}</div>'


def kicker(t, fs=24):
    return f'<div class="kicker k" style="font-size:{fs}px">{t}</div>'


def sub(t, fs=34, lr=100):
    return f'<p class="sub k" style="font-size:{fs}px;padding:0 {lr}px">{t}</p>'


def lista(itens, fs_b=32, fs_s=23, num=True, w=860):
    lis = "".join(f'<div class="check"><div class="box">{(k + 1) if num else "✓"}</div><div><b style="font-size:{fs_b}px">{G.e(a)}</b><span style="font-size:{fs_s}px">{G.e(b)}</span></div></div>' for k, (a, b) in enumerate(itens))
    return f'<div class="k" style="width:{w}px">{lis}</div>'


def rodape_feed():
    return '<div class="base"><div class="rodape k" style="font-size:21px">FORTÍS SOLUÇÕES MATCON</div></div>'


def feed(meio, logo_w=130, b=.75, fonte=None):
    """Feed 3:4. Coluna de 60px no topo a 56px na base."""
    f = f'<div class="fonte k">{fonte}</div>' if fonte else ''
    return f'''<div class="arte" style="width:{W}px;height:{H}px">{G.fundo(W, H, b)}
  <div class="col" style="top:64px;bottom:56px">
    <img class="logo k" src="{A}/logo.png" style="width:{logo_w}px;margin-bottom:44px">
    <div class="meio">{meio}</div>
    <div class="base" style="margin-top:40px">{f}<div class="rodape k" style="font-size:21px">FORTÍS SOLUÇÕES MATCON</div></div>
  </div></div>'''


def story(meio, fonte=None, logo_w=150):
    """Story 9:16. Tudo dentro de 250px (topo) e 400px (base). Ordem: conteúdo, rodapé, @, fonte."""
    f = f'<div class="fonte k" style="font-size:19px;max-width:880px">{fonte}</div>' if fonte else ''
    return f'''<div class="arte" style="width:{SW}px;height:{SH}px">{G.fundo(SW, SH, .93)}
  <div class="col zona" style="top:262px;bottom:410px">
    <img class="logo k" src="{A}/logo.png" style="width:{logo_w}px;margin-bottom:44px">
    <div class="meio">{meio}</div>
    <div class="base" style="margin-top:50px">
      <div class="rodape k" style="font-size:22px">FORTÍS SOLUÇÕES MATCON</div>
      <div class="handle k" style="font-size:24px">@fortismatcon.oficial</div>
      {f}
    </div>
  </div></div>'''


def card(html, pad="6px 0", w=900):
    return f'<div class="card k" style="width:{w}px;padding:{pad}">{html}</div>'


def tabela(linhas, fs=32, destaque=()):
    return '<div class="tab">' + "".join(f'<div class="lin{" d" if i in destaque else ""}"><span class="a" style="font-size:{fs}px">{a}</span><span class="b" style="font-size:{fs}px">{b}</span></div>' for i, (a, b) in enumerate(linhas)) + '</div>'


# ================= FEED 10:30 — ESCALA 5x2 NA LOJA · PARTE 1 =================
FONTE_EC = 'Fonte: Emenda Constitucional 141/2026, promulgada em 16/10/2026 · conforme Portal Contábeis e GreenLegis'

def escala():
    s1 = feed(f'''{kicker("ESCALA 5x2 NA LOJA · PARTE 1")}
  {titulo(["A ESCALA NOVA", "COMEÇA NO MAPA"], 128)}
  {sub("Antes de distribuir folgas, descubra <b>em que horas a sua loja realmente vende.</b>", 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)
    s2 = feed(f'''{kicker("O QUE MUDA NA PRÁTICA")}
  {titulo(["A REGRA NOVA"], 96)}
  {lista([("42 horas por semana", "Limite a partir de meados de dezembro de 2026. Em dezembro de 2027, cai para 40 horas."),
          ("Dois dias de descanso", "Por semana, com um deles preferencialmente no domingo."),
          ("Sem redução de salário", "A emenda proíbe reduzir salários, inclusive os pisos.")], 34, 24)}''', 110, .9, fonte=FONTE_EC)
    s3 = feed(f'''{kicker("PASSO 1")}
  {titulo(["MAPEIE O MOVIMENTO"], 96)}
  {lista([("Puxe as vendas por hora", "Das últimas 8 semanas, no sistema ou no caixa."),
          ("Marque os picos", "Abertura, almoço e sábado costumam pesar. Confirme com os números da sua loja."),
          ("Separe por setor", "Balcão, caixa, depósito e entrega têm picos diferentes.")], 34, 24)}''', 110, .9)
    tab = tabela([("<span class='h'>FAIXA</span>", "<span class='h'>BALCÃO · CAIXA · DEPÓSITO</span>"),
                  ("Seg a sex · 7h às 9h", "3 · 1 · 2"), ("Seg a sex · 9h às 12h", "2 · 1 · 2"),
                  ("Seg a sex · 12h às 14h", "2 · 1 · 1"), ("Seg a sex · 14h às 18h", "2 · 1 · 2"),
                  ("Sábado · 7h às 12h", "4 · 2 · 2")], 28, destaque=(5,))
    s4 = feed(f'''{kicker("PASSO 2")}
  {titulo(["DEFINA O MÍNIMO", "DE CADA SETOR"], 84)}
  {sub("Quantas pessoas cada setor precisa, faixa por faixa.<br><b>A escala nunca fica abaixo disso.</b>", 30, 90)}
  {card(tab, "4px 0", 880)}
  <div class="k"><span class="selo">EXEMPLO ILUSTRATIVO</span></div>''', 110, .9)
    s5 = feed(f'''{kicker("NA PARTE 2")}
  {titulo(["FOLGAS SEM", "SETOR DESCOBERTO"], 104)}
  {sub("Com o mapa e o mínimo de cada setor, a escala de revezamento fica fácil de montar.", 32, 110)}
  {sub("Cada loja deve validar a escala com o seu <b>contador ou advogado trabalhista.</b>", 28, 120)}
  <p class="cta k" style="font-size:30px;padding:0 90px">Quer montar o mapa da sua loja? <b>Chame no direct.</b></p>''', 150, 1.3)
    return [("1030-escala-5x2-parte1-1", s1), ("1030-escala-5x2-parte1-2", s2), ("1030-escala-5x2-parte1-3", s3),
            ("1030-escala-5x2-parte1-4", s4), ("1030-escala-5x2-parte1-5", s5)]


# ================= FEED 15:30 — A CONTA DA LOJA: DESCONTO =================
def conta_desconto():
    cards = "".join(f'''<div class="card" style="padding:26px 12px"><div style="font-size:22px;color:#c4ccda;font-weight:600">{a}</div>
      <div style="font-family:Osw;font-size:64px;color:#D9B579;margin-top:6px">{b}</div><div style="font-size:20px;color:#c4ccda">de venda a mais</div></div>'''
      for a, b in [("3% de desconto", "+11%"), ("5% de desconto", "+20%"), ("10% de desconto", "+50%")])
    return feed(f'''{kicker("A CONTA DA LOJA")}
  {titulo(["5% DE DESCONTO", "= 20% A MAIS DE VENDA"], 100)}
  {sub("Exemplo com <b>margem bruta de 30%</b>: quanto vender a mais para manter o mesmo lucro?", 31, 100)}
  <div class="k" style="width:900px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px">{cards}</div>
  {sub("Venda de R$ 100 com custo de R$ 70 deixa R$ 30.<br>Com 5% de desconto, sobram R$ 25.<br>Para voltar aos R$ 30, é preciso vender 20% a mais.", 25, 110)}
  <p class="cta k" style="font-size:29px;padding:0 80px">Desconto sem critério é <b>margem indo embora no balcão.</b></p>''', 130, 1.3)


# ================= FEED 19:30 — ESPELHO DO DONO =================
def espelho():
    return feed(f'''{kicker("ESPELHO DO DONO")}
  {titulo(["SÁBADO DE LOJA CHEIA", "E O DONO NO CAIXA"], 100)}
  {lista([("Você cobre o almoço do caixa", "Porque ninguém mais pode fechar o dinheiro."),
          ("Resolve a entrega que atrasou", "O cliente liga e pede para falar com o dono."),
          ("Autoriza cada desconto", "O vendedor não sabe até onde pode ir."),
          ("Fecha a porta sem saber a margem", "Vendeu bem, mas não sabe quanto sobrou.")], 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 80px">A loja vendeu. Mas quem fez a gestão? <b>Se você se viu aqui, chame no direct.</b></p>''', 120, 1.3)


# ================= FEED 22:30 — TODA LOJA PRECISA TER: CHECKLIST DE FECHAMENTO =================
def fechamento():
    capa = feed(f'''{kicker("TODA LOJA PRECISA TER")}
  {titulo(["CHECKLIST", "DE FECHAMENTO"], 140)}
  {sub("O dia só termina quando a loja está <b>pronta para abrir amanhã.</b>", 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)
    itens = [("Caixa conferido", "Valores batidos e diferença registrada, se houver."),
             ("Orçamentos do dia", "Cada um com data de retorno ao cliente."),
             ("Faltas anotadas", "O comprador recebe a lista antes de ir embora."),
             ("Retiradas separadas", "Pedidos pagos identificados com nome e data."),
             ("Balcão pronto", "Limpo, com preços e etiquetas no lugar."),
             ("Loja fechada com segurança", "Depósito, portas e alarme conferidos.")]
    l1 = feed(f'''{titulo(["ITENS 1 A 3"], 76)}{lista(itens[:3], 36, 25)}''', 110, .9)
    l2 = feed(f'''{titulo(["ITENS 4 A 6"], 76)}{lista([(a, b) for a, b in itens[3:]], 36, 25).replace('class="box">1<', 'class="box">4<').replace('class="box">2<', 'class="box">5<').replace('class="box">3<', 'class="box">6<')}''', 110, .9)
    fim = feed(f'''{titulo(["MANDE PARA", "SUA EQUIPE"], 120)}
  {sub("Imprima e cole perto do caixa. Quem fecha a loja confere item por item, <b>todo dia.</b>", 34, 110)}
  <p class="cta k" style="font-size:30px;padding:0 90px">Quer a rotina completa da sua loja? <b>Chame no direct.</b></p>''', 210, .9)
    return [("2230-checklist-fechamento-1", capa), ("2230-checklist-fechamento-2", l1),
            ("2230-checklist-fechamento-3", l2), ("2230-checklist-fechamento-4", fim)]


# ================= STORY 12:00 — MERCADO: INCC-M OUTUBRO =================
def story_incc():
    tab = tabela([("INCC-M geral", "0,35%"), ("Materiais e equipamentos", "0,41%"), ("Materiais em setembro", "0,17%"),
                  ("Serviços", "0,31%"), ("Mão de obra", "0,27%")], 30, destaque=(1,))
    return story(f'''{kicker("MERCADO MATCON · INCC-M/FGV", 26)}
  {titulo(["MATERIAIS SOBEM", "0,41% EM OUTUBRO"], 92, 900)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">No ano, o índice acumula <b>6,23%</b>. A sua tabela de preço acompanhou?</p>''',
      'Fonte: FGV IBRE, INCC-M de out/2026 (27/10) · via Diário do Grande ABC e Brasil em Folhas', 100)


# ================= STORY 18:00 — PRODUTO: ARGAMASSA AC I x AC II x AC III =================
def story_argamassa():
    tab = tabela([("AC I", "Áreas internas"), ("AC II", "Internas e externas"),
                  ("AC III", "Mais aderência: variação<br>de temperatura e vibração")], 30, destaque=(2,))
    return story(f'''{kicker("ARGAMASSA COLANTE", 28)}
  {titulo(["AC I, AC II", "OU AC III?"], 92, 900)}
  {card(tab)}
  {sub("Letra <b>E</b>: tempo em aberto estendido.<br>Letra <b>D</b>: deslizamento reduzido.<br>Fachada, piscina e peça grande: <b>siga o boletim técnico do fabricante.</b>", 29, 80)}''',
      'Fonte: ABNT NBR 14081-1 · boletins técnicos Quartzolit e Votorantim · Brasil Engenharia', 100)


# ================= STORY 21:00 — FORTÍS OBRAS =================
def story_obras():
    return story(f'''{kicker("FORTÍS OBRAS", 28)}
  {titulo(["A OBRA DO BAIRRO", "VIRA CLIENTE"], 96, 900)}
  {sub("Um app para a loja <b>acompanhar as obras da região</b> e não deixar nenhuma esfriar.", 31, 90)}
  {lista([("Radar de obras", "Mostra as obras quentes e as que estão esfriando sem contato."),
          ("Profissionais parceiros", "Pedreiros e mestres com pontos por indicação e ranking."),
          ("Calendário de eventos", "Treinamentos da loja com alertas antes de cada data.")], 30, 23, w=880)}
  <p class="cta k" style="font-size:34px;padding:0 80px">Quer ver como funciona? <b>Chame no direct.</b></p>''', None, 120)


# ================= STORY 06:00 (17/11) — BOM DIA, LOJISTA =================
def story_bomdia():
    return story(f'''{kicker("BOM DIA, LOJISTA", 28)}
  {titulo(["ELOGIE EM PÚBLICO", "CORRIJA EM PARTICULAR"], 100, 900)}
  {sub("Hoje, escolha <b>uma atitude certa de alguém da equipe</b> e reconheça na frente de todos. Ajuste de rota é conversa a dois.", 40, 90)}
  <p class="cta k" style="font-size:36px;padding:0 80px">Equipe reconhecida veste a camisa.</p>''', None, 170)


CHECA_JS = """
() => {
  const r = [];
  const arte = document.querySelector('.arte').getBoundingClientRect();
  const story = arte.height > 1500;
  const top = story ? 250 : 40, bot = story ? arte.height - 400 : arte.height - 40;
  const caixa = e => { if (e.tagName === 'IMG' || e.classList.contains('card') || e.classList.contains('fonte')) return e.getBoundingClientRect();
    const g = document.createRange(); g.selectNodeContents(e); const b = g.getBoundingClientRect(); return b.width ? b : e.getBoundingClientRect(); };
  const els = [...document.querySelectorAll('.k')].map(e => ({e, b: caixa(e), n: (e.className + ' ' + (e.innerText || 'img')).slice(0, 50)}));
  for (const x of els) {
    if (x.b.top < top || x.b.bottom > bot) r.push('FORA DA AREA SEGURA: ' + x.n + ' ' + Math.round(x.b.top) + '-' + Math.round(x.b.bottom));
    if (x.b.left < 50 || x.b.right > arte.width - 50) r.push('BORDA LATERAL: ' + x.n);
    if (x.e.scrollWidth > x.e.clientWidth + 2 && !x.e.classList.contains('titulo')) r.push('TEXTO TRANSBORDA: ' + x.n);
  }
  for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
    const a = els[i].b, b = els[j].b;
    if (els[i].e.contains(els[j].e) || els[j].e.contains(els[i].e)) continue;
    const hOver = a.left < b.right && b.left < a.right;
    if (!hOver) continue;
    const gap = Math.max(b.top - a.bottom, a.top - b.bottom);
    const sameBase = els[i].e.parentElement === els[j].e.parentElement && els[i].e.parentElement.classList.contains('base');
    const minimo = 40;
    if (gap < minimo) r.push('FOLGA ' + Math.round(gap) + 'px entre [' + els[i].n + '] e [' + els[j].n + ']');
  }
  const t = [...document.querySelectorAll('.titulo')].map(t => +t.style.fontSize.replace('px',''));
  return {r, t};
}
"""


async def renderizar(itens, saida):
    os.makedirs(saida, exist_ok=True)
    tmp = os.path.join(G.AQUI, ".tmp"); os.makedirs(tmp, exist_ok=True)
    falhas = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for nome, corpo, (w, h) in itens:
            caminho = os.path.join(tmp, nome + ".html")
            pag = G.pagina(corpo).replace("</style>", CSS + "</style>", 1)
            open(caminho, "w").write(pag)
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.goto("file://" + caminho); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.evaluate(G.AJUSTE_JS)
            res = await pg.evaluate(CHECA_JS)
            png = os.path.join(tmp, nome + ".png")
            await pg.screenshot(path=png); await pg.close()
            Image.open(png).convert("RGB").save(os.path.join(saida, nome + ".jpg"), quality=92)
            falhas += len(res["r"])
            print("ok" if not res["r"] else "ATENÇÃO", nome, "títulos(px):", res["t"])
            for x in res["r"]:
                print("   -", x)
        await b.close()
    print("TOTAL DE PROBLEMAS:", falhas)


itens = [(n, c, (W, H)) for n, c in escala()]
itens += [("1530-conta-desconto", conta_desconto(), (W, H)), ("1930-espelho-sabado-no-caixa", espelho(), (W, H))]
itens += [(n, c, (W, H)) for n, c in fechamento()]
itens += [("story-1200-incc-outubro", story_incc(), (SW, SH)), ("story-1800-argamassa-ac", story_argamassa(), (SW, SH)),
          ("story-2100-obras", story_obras(), (SW, SH)), ("story-0600-17-11-bom-dia", story_bomdia(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-16-11')
asyncio.run(renderizar(itens, saida))
