"""Conteúdo de 18/11/2026 (feed 1080x1440, stories 1080x1920) + story 06:00 de 19/11.

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


# ================= FEED 10:30 — CARROSSEL SALVÁVEL: CONFERÊNCIA NO RECEBIMENTO =================
def recebimento():
    capa = feed(f'''{kicker("MANDE PARA SUA EQUIPE")}
  {titulo(["ANTES DE", "ASSINAR O CANHOTO"], 118)}
  {sub("O que conferir quando <b>o caminhão do fornecedor</b> encosta na loja.", 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)
    s2 = feed(f'''{kicker("COM A NOTA NA MÃO")}
  {titulo(["CONFIRA O PAPEL"], 100)}
  {lista([("Nota x pedido de compra", "Produto, quantidade e preço são os que você negociou?"),
          ("Prazo e condição", "Vencimento e forma de pagamento iguais ao combinado."),
          ("Dados da loja", "Razão social e CNPJ certos, para não travar o fiscal.")], 34, 24)}''', 110, .9)
    s3 = feed(f'''{kicker("COM A MERCADORIA NO CHÃO")}
  {titulo(["CONTE E OLHE"], 100)}
  {lista([("Conte volume por volume", "Saco, caixa e peça. Não aceite “está tudo aí”."),
          ("Abra o que dá para abrir", "Saco furado, caixa amassada, peça trincada."),
          ("Lote e tonalidade", "Piso e revestimento do mesmo lote, para não faltar na obra do cliente."),
          ("Validade", "Cimento, argamassa e rejunte com data longe de vencer.")], 32, 23)}''', 110, .9)
    fim = feed(f'''{titulo(["DEU DIFERENÇA?"], 104)}
  {lista([("Anote no canhoto", "Antes de assinar, escreva o que faltou ou chegou avariado."),
          ("Foto na hora", "Com o motorista ainda na loja."),
          ("Avise o fornecedor no mesmo dia", "Depois, vira prejuízo da loja.")], 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 90px">Quer uma rotina de recebimento para a sua loja? <b>Chame no direct.</b></p>''', 110, .9)
    return [("1030-recebimento-1", capa), ("1030-recebimento-2", s2), ("1030-recebimento-3", s3), ("1030-recebimento-4", fim)]


# ================= FEED 15:30 — A CONTA DA LOJA: O ITEM QUE FALTOU =================
def conta_ruptura():
    tab = tabela([("Lista do cliente", "R$ 1.200"), ("Item que faltou", "R$ 30"),
                  ("Lucro bruto perdido (margem 25%)", "R$ 300"), ("3 vezes por semana, no mês", "R$ 3.600")], 28, destaque=(3,))
    return feed(f'''{kicker("A CONTA DA LOJA")}
  {titulo(["FALTOU O REJUNTE.", "FOI A LISTA INTEIRA."], 84)}
  {sub("Cliente de obra quer <b>levar tudo num lugar só.</b> Se falta um item, ele leva a lista para o concorrente.", 29, 100)}
  {card(tab, "4px 0", 860)}
  <div class="k"><span class="selo">EXEMPLO ILUSTRATIVO</span></div>
  <p class="cta k" style="font-size:29px;padding:0 80px">Estoque mínimo por item evita essa conta. <b>Chame no direct.</b></p>''', 110, 1.3)


# ================= FEED 19:30 — ESPELHO DO DONO =================
def espelho():
    return feed(f'''{kicker("ESPELHO DO DONO")}
  {titulo(["O FUNCIONÁRIO QUE", "MAIS TRABALHA É VOCÊ"], 96)}
  {lista([("Abre e fecha a loja", "Porque ninguém mais tem a chave nem a confiança."),
          ("Cobre o caixa no almoço", "E ainda confere o caminhão que chegou."),
          ("Faz entrega quando o motorista falta", "O dono vira a peça de reposição de todo mundo."),
          ("À noite, faz o pedido de compra", "A gestão fica para a hora em que sobra energia.")], 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 80px">Dono que faz tudo não tem tempo de fazer a loja crescer. <b>Se você se viu aqui, chame no direct.</b></p>''', 120, 1.3)


# ================= FEED 22:30 — DE LOJA EM LOJA =================
def de_loja():
    cards = "".join(f'''<div class="card" style="width:860px;padding:18px 32px;text-align:left">
      <div style="font-family:Osw;font-size:38px;color:#D9B579">{a}</div>
      <div style="font-size:23px;color:#dfe5ee;margin-top:4px">{b}</div></div>'''
      for a, b in [("META NA PAREDE", "Todo mundo sabe quanto a loja precisa vender hoje, não só o dono."),
                   ("10 MINUTOS ANTES DE ABRIR", "Uma conversa curta: o que entra, o que sai, quem cobre o quê."),
                   ("NÚMERO TODA SEMANA", "O dono olha margem e estoque sem esperar o contador.")])
    return feed(f'''{kicker("DE LOJA EM LOJA")}
  {titulo(["O QUE AS LOJAS", "QUE CRESCEM FAZEM"], 96)}
  {sub("Tamanho e cidade mudam. <b>Estes três hábitos se repetem.</b>", 28, 100)}
  <div class="k" style="display:flex;flex-direction:column;gap:20px;align-items:center">{cards}</div>
  <p class="cta k" style="font-size:29px;padding:0 80px">Quais faltam na sua loja? <b>Diagnóstico sem custo no direct.</b></p>''', 96, 1.3)


# ================= STORY 12:00 — MERCADO: SINAPI OUTUBRO =================
def story_sinapi():
    tab = tabela([("Custo do m² (out/26)", "R$ 2.005,57"), ("Variação no mês", "+0,29%"),
                  ("Materiais no mês", "+0,46%"), ("Mão de obra no mês", "+0,08%"),
                  ("Acumulado em 12 meses", "+6,84%")], 30, destaque=(0,))
    return story(f'''{kicker("MERCADO MATCON · IBGE", 26)}
  {titulo(["CUSTO DO M² PASSA", "DOS R$ 2 MIL"], 92, 900)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Custo subindo: <b>a sua tabela de preço acompanhou?</b></p>''',
      'Fonte: IBGE, SINAPI out/2026 (divulgado em 12/11/2026) · via IBGE e Diário do Grande ABC', 100)


# ================= STORY 18:00 — PRODUTO: TUBO MARROM x BRANCO x CPVC =================
def story_tubos():
    tab = tabela([("<span class='h'>TUBO</span>", "<span class='h'>USO</span>"),
                  ("PVC marrom soldável", "água fria"), ("PVC branco", "esgoto, pluvial e ventilação"),
                  ("CPVC", "água quente")], 28)
    return story(f'''{kicker("ENTENDA A DIFERENÇA", 26)}
  {titulo(["MARROM, BRANCO", "OU CPVC?"], 96, 900)}
  {card(tab)}
  {sub("Cada linha tem a sua norma: <b>NBR 5648</b> (água fria), <b>NBR 5688</b> (esgoto) e <b>NBR 15884</b> (CPVC). Vendedor que explica isso <b>vende a conexão certa.</b>", 25, 80)}''',
      'Fonte: ABNT NBR 5648, NBR 5688 e NBR 15884 · fichas técnicas Amanco e Tigre (via AECweb)', 90)


# ================= STORY 21:00 — FORTÍS OBRAS: PROFISSIONAIS PARCEIROS =================
def story_obras():
    return story(f'''{kicker("FORTÍS OBRAS", 28)}
  {titulo(["O PEDREIRO QUE", "INDICA VOLTA"], 96, 900)}
  {sub("Quem decide a compra da obra muitas vezes é o <b>profissional</b>. O Fortís Obras ajuda a loja a cuidar dele.", 31, 90)}
  {lista([("Pontos por indicação", "Cada cliente indicado soma pontos para o profissional."),
          ("Ranking de parceiros", "A loja vê quem mais traz obra e reconhece."),
          ("Radar de obras", "Mostra as obras quentes e as que estão esfriando sem contato.")], 30, 23, w=880)}
  <p class="cta k" style="font-size:34px;padding:0 80px">Quer ver como funciona? <b>Chame no direct.</b></p>''', None, 120)


# ================= STORY 06:00 (19/11) — BOM DIA, LOJISTA =================
def story_bomdia():
    return story(f'''<div class="kicker k" style="font-size:28px;margin-bottom:12px">BOM DIA, LOJISTA</div>
  {titulo(["CADA UM COM", "UMA MISSÃO"], 104, 900)}
  {sub("Antes de abrir a porta, diga a cada pessoa <b>uma tarefa que precisa estar pronta até o fim do dia.</b>", 40, 90)}
  <p class="cta k" style="font-size:36px;padding:0 80px">Equipe que sabe o que fazer não espera o dono mandar.</p>''', None, 170)

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



itens = [(n, c, (W, H)) for n, c in recebimento()]
itens += [("1530-conta-item-que-faltou", conta_ruptura(), (W, H)), ("1930-espelho-dono-faz-tudo", espelho(), (W, H)),
          ("2230-de-loja-em-loja-habitos", de_loja(), (W, H))]
itens += [("story-1200-sinapi-outubro", story_sinapi(), (SW, SH)), ("story-1800-tubos-pvc", story_tubos(), (SW, SH)),
          ("story-2100-obras-parceiros", story_obras(), (SW, SH)), ("story-0600-19-11-bom-dia", story_bomdia(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-18-11')
asyncio.run(renderizar(itens, saida))
