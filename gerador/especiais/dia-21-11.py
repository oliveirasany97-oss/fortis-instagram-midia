"""Conteúdo de 21/11/2026 (feed 1080x1440, stories 1080x1920) + story 06:00 de 22/11.

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


def lista(itens, fs_b=32, fs_s=23, num=True, w=860, ini=1):
    lis = "".join(f'<div class="check"><div class="box">{(k + ini) if num else "✓"}</div><div><b style="font-size:{fs_b}px">{G.e(a)}</b><span style="font-size:{fs_s}px">{G.e(b)}</span></div></div>' for k, (a, b) in enumerate(itens))
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


# ================= FEED 10:30 — CARROSSEL SALVÁVEL: A VENDA QUE FICA NO BALCÃO =================
def balcao():
    capa = feed(f'''{kicker("MANDE PARA SUA EQUIPE")}
  {titulo(["A VENDA QUE", "FICA NO BALCÃO"], 118)}
  {sub("Perguntas que o vendedor faz <b>antes de fechar o pedido</b> e que o cliente agradece depois.", 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)
    s2 = feed(f'''{kicker("ANTES DE FECHAR")}
  {titulo(["PERGUNTE"], 100)}
  {lista([("“Para qual etapa da obra é?”", "Quem sabe a etapa sabe o que vem junto."),
          ("“Já tem o que vai assentar?”", "Piso pede argamassa, rejunte e espaçador."),
          ("“Quem vai fazer o serviço?”", "O profissional costuma pedir o que falta.")], 34, 24)}''', 110, .9)
    s3 = feed(f'''{kicker("E COMPLETE")}
  {titulo(["MAIS DUAS"], 100)}
  {lista([("“Tem ferramenta para isso?”", "Desempenadeira, nível, broca, disco, fita."),
          ("“Quer levar uma sobra?”", "Uma pequena reserva evita a volta à loja e a falta de lote igual.")], 34, 24, ini=4)}
  {sub("Não é empurrar produto: é <b>evitar a segunda viagem.</b>", 30, 110)}''', 110, .9)
    fim = feed(f'''{titulo(["COMBINE COM", "A EQUIPE"], 104)}
  {lista([("Uma pergunta por venda", "Comece com a da etapa da obra."),
          ("Lista no balcão", "As perguntas à vista de todo vendedor."),
          ("Converse no fim da semana", "Qual pergunta mais gerou venda?")], 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 90px">Quer montar o roteiro de atendimento da sua loja? <b>Chame no direct.</b></p>''', 110, 1.3)
    return [("1030-venda-no-balcao-1", capa), ("1030-venda-no-balcao-2", s2), ("1030-venda-no-balcao-3", s3), ("1030-venda-no-balcao-4", fim)]


# ================= FEED 15:30 — A CONTA DA LOJA: GIRO =================
def conta_giro():
    tab = tabela([("<span class='h'>MESMOS R$ 6.000</span>", "<span class='h'>GANHO BRUTO NO ANO</span>"),
                  ("Gira 1 vez no ano", "R$ 1.500"), ("Gira 6 vezes no ano", "R$ 9.000")], 30, destaque=(2,))
    return feed(f'''{kicker("A CONTA DA LOJA")}
  {titulo(["MESMO DINHEIRO,", "6 VEZES O GANHO"], 88)}
  {sub("Ganho bruto de 25% sobre o custo = <b>R$ 1.500 a cada vez</b> que o estoque gira.", 29, 100)}
  {card(tab, "4px 0", 860)}
  <div class="k"><span class="selo">EXEMPLO ILUSTRATIVO</span></div>
  <p class="cta k" style="font-size:29px;padding:0 80px">Produto parado na prateleira não paga conta. <b>Quer olhar o giro da sua loja? Chame no direct.</b></p>''', 110, 1.3)


# ================= FEED 19:30 — ESPELHO DO DONO =================
def espelho():
    return feed(f'''{kicker("ESPELHO DO DONO")}
  {titulo(["ORÇAMENTO ENVIADO,", "CLIENTE SUMIDO"], 92)}
  {lista([("O orçamento sai pelo WhatsApp", "E ninguém liga de volta para saber o que achou."),
          ("Ninguém sabe quantos estão abertos", "Nem quanto dinheiro está parado neles."),
          ("O vendedor que fez saiu de folga", "E o cliente não tem com quem falar."),
          ("Dias depois, a obra está na rua", "Com material comprado em outra loja.")], 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 80px">Orçamento sem retorno é venda que a loja entregou de graça. <b>Se você se viu aqui, chame no direct.</b></p>''', 120, 1.3)


# ================= FEED 22:30 — TODA LOJA PRECISA TER =================
def toda_loja():
    return feed(f'''{kicker("TODA LOJA PRECISA TER")}
  {titulo(["O CADASTRO DO", "CLIENTE DE OBRA"], 96)}
  {sub("Obra compra por <b>meses</b>. Quem sabe em que fase ela está, sabe o que oferecer.", 29, 100)}
  {lista([("Nome e WhatsApp", "Para falar com o cliente sem depender do vendedor."),
          ("Endereço da obra", "Ajuda na entrega e mostra a região onde a loja vende."),
          ("Fase da obra", "Fundação, alvenaria, instalações ou acabamento."),
          ("Profissional responsável", "Pedreiro, eletricista, encanador: quem decide junto.")], 31, 23)}
  <p class="cta k" style="font-size:29px;padding:0 80px">Sua loja já tem? <b>Diagnóstico sem custo no direct.</b></p>''', 96, 1.3)


# ================= STORY 12:00 — MERCADO: PMC SETEMBRO =================
def story_pmc():
    tab = tabela([("Material de construção", "−1,3%"), ("Varejo (restrito)", "+0,2%"),
                  ("Varejo ampliado", "+0,2%")], 32, destaque=(0,))
    return story(f'''{kicker("MERCADO MATCON · IBGE", 26)}
  {titulo(["VENDAS DE MATERIAL", "RECUAM 1,3%"], 88, 900)}
  {sub("Setembro contra agosto, na Pesquisa Mensal de Comércio.", 28, 90)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Mercado parado pede <b>loja afinada: estoque, preço e atendimento.</b></p>''',
      'Fonte: IBGE, PMC set/2026 · via InfoMoney e Brasil em Folhas', 80)


# ================= STORY 18:00 — PRODUTO: CERÂMICA x PORCELANATO =================
def story_porcelanato():
    tab = tabela([("<span class='h'>PLACA</span>", "<span class='h'>ABSORÇÃO DE ÁGUA</span>"),
                  ("Porcelanato técnico", "até 0,1%"), ("Porcelanato esmaltado", "até 0,5%"),
                  ("Grés", "0,5% a 3%"), ("Semigrés", "3% a 6%"), ("Semiporoso", "6% a 10%"), ("Poroso", "acima de 10%")], 24)
    return story(f'''{kicker("ENTENDA A DIFERENÇA", 26)}
  {titulo(["CERÂMICA OU", "PORCELANATO?"], 84, 900)}
  {sub("A diferença está em <b>quanta água a placa absorve.</b> Vendedor que explica isso <b>vende a placa certa.</b>", 28, 90)}
  {card(tab)}''',
      'Fonte: ABNT NBR 15463 e NBR 13818 · Incepa · Sienge', 70)


# ================= STORY 21:00 — FORTÍS FLOW: METAS INTELIGENTES =================
def story_flow():
    esq = lista([("Meta do mês e realizado", "Cada vendedor vê onde está."),
                 ("Meta diária necessária", "Quanto falta vender por dia útil."),
                 ("Projeção de fechamento", "Se o ritmo atual bate a meta.")], 30, 22, w=470)
    cel = f'''<div style="display:flex;flex-direction:column;align-items:center;gap:44px">
      <div class="k" style="width:280px;height:440px;border-radius:40px;border:8px solid #0b1424;outline:3px solid rgba(217,181,121,.85);box-shadow:0 0 40px rgba(217,181,121,.25);overflow:hidden;background:#0E1F39">
        <img src="{A}/telas/metas.png" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block"></div>
      <div class="k" style="font-weight:600;letter-spacing:4px;color:#D9B579;font-size:16px">TELA REAL · DADOS FICTÍCIOS</div></div>'''
    return story(f'''{kicker("FORTÍS FLOW", 28)}
  {titulo(["META QUE O", "VENDEDOR ENXERGA"], 84, 900)}
  {row(esq, cel)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Quer ver na sua loja? <b>Chame no direct.</b></p>''', None, 90)


# ================= STORY 06:00 (22/11) — BOM DIA, LOJISTA =================
def story_bomdia():
    return story(f'''<div class="kicker k" style="font-size:28px;margin-bottom:12px">BOM DIA, LOJISTA</div>
  {titulo(["15 MINUTOS", "PARA A SEMANA"], 104, 900)}
  {sub("Antes de abrir na segunda, reúna a equipe: <b>entregas da semana, folgas de cada dia e a meta de cada vendedor.</b>", 38, 90)}
  <p class="cta k" style="font-size:36px;padding:0 80px">Semana combinada no começo tem menos correria no meio.</p>''', None, 170)


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



itens = [(n, c, (W, H)) for n, c in balcao()]
itens += [("1530-conta-giro", conta_giro(), (W, H)), ("1930-espelho-orcamento-sumido", espelho(), (W, H)),
          ("2230-toda-loja-cadastro-obra", toda_loja(), (W, H))]
itens += [("story-1200-pmc-setembro", story_pmc(), (SW, SH)), ("story-1800-ceramica-porcelanato", story_porcelanato(), (SW, SH)),
          ("story-2100-flow-metas", story_flow(), (SW, SH)), ("story-0600-22-11-bom-dia", story_bomdia(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-21-11')
asyncio.run(renderizar(itens, saida))
