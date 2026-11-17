"""Conteúdo de 17/11/2026 (feed 1080x1440, stories 1080x1920) + story 06:00 de 18/11.

Mesmo layout em fluxo e checagem automática de sobreposição/áreas seguras de dia-16-11.py.
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



def row(left, right, gap=40):
    return f'<div style="display:flex;align-items:center;justify-content:center;gap:{gap}px;width:100%">{left}{right}</div>'


# ================= FEED 10:30 — ESCALA 5x2 NA LOJA · PARTE 2 =================
FONTE_EC = 'Fonte: Emenda Constitucional 141/2026 (DOU de 16/10/2026) · conforme Senior Exigências Legais e Movimento Econômico'

def escala():
    s1 = feed(f'''{kicker("ESCALA 5x2 NA LOJA · PARTE 2")}
  {titulo(["FOLGAS SEM", "SETOR DESCOBERTO"], 118)}
  {sub("Como distribuir as duas folgas da semana e <b>manter o sábado coberto.</b>", 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)
    s2 = feed(f'''{kicker("PASSO 3")}
  {titulo(["DOMINGO + 1"], 110)}
  {lista([("Duas folgas por semana", "A regra nova pede dois dias de descanso, um deles preferencialmente no domingo."),
          ("Loja fechada no domingo?", "Então o domingo já é a primeira folga de todo mundo."),
          ("A segunda folga gira", "Ela cai de segunda a sexta. O sábado, dia de pico, fica com a equipe inteira.")], 34, 24)}''', 110, .9, fonte=FONTE_EC)
    tab = tabela([("<span class='h'>EQUIPE</span>", "<span class='h'>2ª FOLGA</span>"),
                  ("Vendedor 1", "Segunda"), ("Vendedor 2", "Terça"), ("Vendedor 3", "Quarta"),
                  ("Vendedor 4", "Quinta"), ("Vendedor 5", "Sexta"), ("Sábado", "Todos trabalham")], 27, destaque=(6,))
    s3 = feed(f'''{kicker("PASSO 4")}
  {titulo(["ESPALHE A", "SEGUNDA FOLGA"], 86)}
  {card(tab, "4px 0", 820)}
  <div class="k"><span class="selo">EXEMPLO ILUSTRATIVO</span></div>''', 110, .9)
    s4 = feed(f'''{kicker("PASSO 5")}
  {titulo(["CONFIRA O MÍNIMO"], 96)}
  {lista([("Cruze com o mapa da Parte 1", "Em cada dia, quem fica cobre o mínimo de cada setor?"),
          ("Mesmo setor, dias diferentes", "Se o balcão tem duas pessoas, as folgas delas nunca caem no mesmo dia."),
          ("Gire a cada mês", "Quem folgou na segunda passa para outro dia. Ninguém fica sempre com o mesmo.")], 34, 24)}''', 110, .9)
    s5 = feed(f'''{kicker("NA PARTE 3")}
  {titulo(["PRODUTIVIDADE", "POR VENDEDOR"], 110)}
  {sub("Com menos horas na semana, cada hora de balcão precisa render mais.", 32, 110)}
  {sub("Cada loja deve validar a escala com o seu <b>contador ou advogado trabalhista.</b>", 28, 120)}
  <p class="cta k" style="font-size:30px;padding:0 90px">Quer ajuda para montar a escala da sua loja? <b>Chame no direct.</b></p>''', 150, 1.3)
    return [("1030-escala-5x2-parte2-1", s1), ("1030-escala-5x2-parte2-2", s2), ("1030-escala-5x2-parte2-3", s3),
            ("1030-escala-5x2-parte2-4", s4), ("1030-escala-5x2-parte2-5", s5)]


# ================= FEED 15:30 — A CONTA DA LOJA: 13º SALÁRIO =================
def conta_13():
    cards = "".join(f'''<div class="card" style="padding:18px 16px"><div style="font-size:22px;color:#c4ccda;font-weight:600;letter-spacing:2px">{a}</div>
      <div style="font-family:Osw;font-size:50px;color:#D9B579;margin-top:6px">{b}</div><div style="font-size:21px;color:#c4ccda">{c}</div></div>'''
      for a, b, c in [("1ª PARCELA", "ATÉ 30/11", "metade do salário"), ("2ª PARCELA", "ATÉ 18/12", "o restante, com descontos")])
    return feed(f'''{kicker("A CONTA DA LOJA")}
  {titulo(["O 13º JÁ ESTÁ", "NO SEU CAIXA?"], 92)}
  {sub("Folha de <b>R$ 30 mil</b> = <b>R$ 30 mil a mais</b> até 18/12, além dos salários.", 29, 100)}
  <div class="k" style="width:860px;display:grid;grid-template-columns:1fr 1fr;gap:24px">{cards}</div>
  {sub("Para não apertar: separe <b>1/12 da folha todo mês (8,33%)</b>. Encargos à parte: confirme com o contador.", 25, 110)}
  <p class="cta k" style="font-size:29px;padding:0 80px">Dezembro sem susto começa em janeiro. <b>Chame no direct.</b></p>''', 110, 1.3,
      fonte='Fonte: Lei 4.749/1965 · datas de 2026 conforme Gazeta SP e Metrópoles')


# ================= FEED 19:30 — ESPELHO DO DONO =================
def espelho():
    return feed(f'''{kicker("ESPELHO DO DONO")}
  {titulo(["SEU WHATSAPP", "VIROU O SAC DA LOJA"], 104)}
  {lista([("Cliente manda áudio às 22h", "E espera a resposta antes de a loja abrir."),
          ("Vendedor pede preço só para você", "Porque a tabela está na sua cabeça."),
          ("Fornecedor negocia direto com você", "E ninguém mais sabe o que foi combinado."),
          ("Férias com o celular na mão", "A loja não anda sem você responder.")], 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 80px">Loja que depende do celular do dono não cresce. <b>Se você se viu aqui, chame no direct.</b></p>''', 120, 1.3)


# ================= FEED 22:30 — TODA LOJA PRECISA TER: ALÇADA DE DESCONTO =================
def alcada():
    capa = feed(f'''{kicker("TODA LOJA PRECISA TER")}
  {titulo(["ALÇADA", "DE DESCONTO"], 140, 920, 1.18)}
  {sub("Quem pode dar quanto de desconto, <b>sem ligar para o dono.</b>", 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)
    tab = tabela([("<span class='h'>QUEM</span>", "<span class='h'>PODE DAR</span>"),
                  ("Vendedor", "até 3%"), ("Gerente", "até 6%"), ("Dono", "acima de 6%")], 36, destaque=(3,))
    s2 = feed(f'''{titulo(["A TABELA"], 96)}
  {sub("Defina os seus percentuais pela margem: <b>básico tem margem menor que acabamento.</b>", 30, 110)}
  {card(tab, "4px 0", 820)}
  <div class="k"><span class="selo">EXEMPLO ILUSTRATIVO</span></div>''', 110, .9)
    s3 = feed(f'''{titulo(["AS REGRAS"], 96)}
  {lista([("Desconto tem motivo", "À vista, volume ou cliente de obra. Sem motivo, sem desconto."),
          ("Fica registrado no pedido", "Quem deu, quanto e por quê."),
          ("Margem baixa fica de fora", "Na dúvida, o vendedor chama o gerente."),
          ("Revisão todo mês", "O dono confere quanto saiu em desconto e ajusta a tabela.")], 34, 24)}''', 110, .9)
    fim = feed(f'''{titulo(["MANDE PARA", "SUA EQUIPE"], 120)}
  {sub("Imprima a tabela e deixe no balcão. Desconto vira <b>decisão da loja, não pressão do cliente.</b>", 34, 110)}
  <p class="cta k" style="font-size:30px;padding:0 90px">Quer definir a alçada da sua loja? <b>Chame no direct.</b></p>''', 210, .9)
    return [("2230-alcada-desconto-1", capa), ("2230-alcada-desconto-2", s2),
            ("2230-alcada-desconto-3", s3), ("2230-alcada-desconto-4", fim)]


# ================= STORY 12:00 — MERCADO: ABRAMAT REVISA 2026 =================
def story_abramat():
    tab = tabela([("Outubro x out/2025", "+1,0%"), ("Janeiro a outubro", "−2,8%"),
                  ("Básicos (jan a out)", "−2,6%"), ("Acabamento (jan a out)", "−3,2%")], 30, destaque=(1,))
    return story(f'''{kicker("MERCADO MATCON · ABRAMAT", 26)}
  {titulo(["INDÚSTRIA PREVÊ", "QUEDA DE 1,3% EM 2026"], 88, 900)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Mercado lento: <b>quem tem gestão toma a venda de quem não tem.</b></p>''',
      'Fonte: ABRAMAT, revisão de 12/11/2026 · via CNN Brasil (Estadão Conteúdo) e Diário do Grande ABC', 100)


# ================= STORY 18:00 — PRODUTO: SIGLAS DO CIMENTO =================
def story_cimento():
    tab = tabela([("CP II-E", "com escória de alto-forno"), ("CP II-F", "com fíler calcário"), ("CP II-Z", "com pozolana"),
                  ("CP III", "de alto-forno"), ("CP IV", "pozolânico"), ("CP V-ARI", "alta resistência inicial")], 25)
    return story(f'''{kicker("ENTENDA A SIGLA", 26)}
  {titulo(["O QUE DIZ O", "SACO DE CIMENTO"], 88, 900)}
  {card(tab)}
  {sub("O número no fim (<b>25, 32 ou 40</b>) é a resistência mínima à compressão aos 28 dias, em MPa. <b>RS</b>: resistente a sulfatos.", 25, 80)}''',
      'Fonte: ABNT NBR 16697:2018 (Cimento Portland – Requisitos) · conforme Sienge e Engenharia 360', 90)


# ================= STORY 21:00 — FORTÍS FLOW: ENCOMENDAS =================
def story_flow():
    esq = lista([("Registrada na venda", "Cliente, produto, valor e prazo."),
                 ("Status à vista", "Aberta, em andamento, na fila."),
                 ("Busca na hora", "Por produto e por marca.")], 30, 22, w=470)
    cel = f'''<div style="display:flex;flex-direction:column;align-items:center;gap:44px">
      <div class="k" style="width:280px;height:440px;border-radius:40px;border:8px solid #0b1424;outline:3px solid rgba(217,181,121,.85);box-shadow:0 0 40px rgba(217,181,121,.25);overflow:hidden;background:#0E1F39">
        <img src="{A}/telas/encomendas.png" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block"></div>
      <div class="k" style="font-weight:600;letter-spacing:4px;color:#D9B579;font-size:16px">TELA REAL · DADOS FICTÍCIOS</div></div>'''
    return story(f'''{kicker("FORTÍS FLOW", 28)}
  {titulo(["ENCOMENDA", "NÃO SE PERDE"], 84, 900)}
  {row(esq, cel)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Quer ver na sua loja? <b>Chame no direct.</b></p>''', None, 90)


# ================= STORY 06:00 (18/11) — BOM DIA, LOJISTA =================
def story_bomdia():
    return story(f'''{kicker("BOM DIA, LOJISTA", 28)}
  {titulo(["QUARTA É DIA DE", "CONFERIR O RUMO"], 100, 900)}
  {sub("Metade da semana já foi. Compare <b>o que a loja vendeu com a meta</b> e combine com a equipe o ajuste de hoje.", 40, 90)}
  <p class="cta k" style="font-size:36px;padding:0 80px">Ainda dá tempo de fechar a semana bem.</p>''', None, 170)

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
itens += [("1530-conta-13-salario", conta_13(), (W, H)), ("1930-espelho-whatsapp-do-dono", espelho(), (W, H))]
itens += [(n, c, (W, H)) for n, c in alcada()]
itens += [("story-1200-abramat-revisao-2026", story_abramat(), (SW, SH)), ("story-1800-siglas-cimento", story_cimento(), (SW, SH)),
          ("story-2100-flow-encomendas", story_flow(), (SW, SH)), ("story-0600-18-11-bom-dia", story_bomdia(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-17-11')
asyncio.run(renderizar(itens, saida))
